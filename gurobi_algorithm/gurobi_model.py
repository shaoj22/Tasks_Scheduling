'''
File: gurobi_model.py
Project: Job Orchestration
Description:
-----------
gurobi model for job orchestration problem
-----------
Author: 626
Created Date: 2023-0823
'''

import sys
sys.path.append("..")
import numpy as np
import gurobipy as gp
from gurobipy import GRB
import time
from utils import create_instance
from utils import create_random_data
from heuristic_algorithm import heuristic_OLB

class gurobi_model():
    def __init__(self, instance, time_limit = 360):
        """
        instance: 任务算例
        time_limit: 求解时间上限
        """
        self.A = instance.task_num # 任务的数量
        self.tasks = instance.tasks # 任务的信息
        self.y = instance.tasks_dependency # 任务的依赖关系
        self.time_limit = time_limit # 限制最大的求解时间
        self.K = 1440 # 一天的分钟数
        self.lower_bound = instance.resource_lower_bound # 资源的下界
    
    def build_model(self, model):
        """
        build objective, variables and constraints in job orchestration problem    
        """
        M = 1500
        # create vars
        x_list = [(i,k) for i in range(self.A) for k in range(self.K)]           # create vars x[i][j]
        x = model.addVars(x_list, vtype=GRB.BINARY, name="x")
        z_list = [(i,k) for i in range(self.A) for k in range(self.K)]           # create vars z[i][j]
        z = model.addVars(z_list, vtype=GRB.BINARY, name="z")
        t_list = [i for i in range(self.A)]                                      # create vars t[i]
        t = model.addVars(t_list, vtype=GRB.CONTINUOUS, name="t")
        u = model.addVar(vtype=GRB.CONTINUOUS, name="u")                         # create vars u
        # create objective
        model.modelSense = GRB.MINIMIZE
        model.setObjective(u) # 最小化资源负载
        # create constraints
        model.addConstrs( t[j] - t[i] - self.tasks[i]['execution_time'] >= M * (self.y[i][j] - 1) for i in range(self.A) for j in range(self.A) if i != j)  # 依赖任务时间约束
        model.addConstrs( t[i] + self.tasks[i]['execution_time'] <= self.tasks[i]['latest_time'] for i in range(self.A)) # 最晚完成时间约束
        model.addConstrs( t[i] >= self.tasks[i]['earliest_time'] for i in range(self.A)) # 最早完成时间约束
        model.addConstrs( t[i] - k >= (-M) * x[i,k] for i in range(self.A) for k in range(self.K)) # 决策变量与时间之间的关系
        model.addConstrs( k - t[i] - self.tasks[i]['execution_time'] >= (-M) * z[i,k] for i in range(self.A) for k in range(self.K)) # 决策变量与时间之间的关系
        model.addConstrs( gp.quicksum( self.tasks[i]['resource_load'] * (x[i,k] + z[i,k] - 1) for i in range(self.A)) <= u for k in range(self.K)) # 最大资源负载约束
        model.addConstr( u >= self.lower_bound) # 资源下界约束
        # 可以尝试把所有时刻的资源负载都累加起来
        model.update()
        info = {
            "u" : u,
            "t" : t,
        }

        return info

    def set_init_solution(self, Model, solution_t):
        """
        set initial solution for the model
        """
        for i in range(len(solution_t)):
            Model.getVarByName(f"t[{i}]").start = solution_t[i]
        x_val = np.zeros((len(solution_t), len(solution_t)))
        z_val = np.zeros((len(solution_t), len(solution_t)))
        for i in range(len(solution_t)):
            for j in range(len(solution_t)):
                if solution_t[j] <= solution_t[i] and solution_t[i] <= solution_t[j] + self.tasks[j]["execution_time"]:
                    x_val[i][j] = 1
                else:
                    x_val[i][j] = 0
                if solution_t[i] <= solution_t[j] + self.tasks[j]["execution_time"]:
                    z_val[i][j] = 1
                else:
                    z_val[i][j] = 0
        # for i in range(len(solution_t)):
        #     for j in range(len(solution_t)):
        #         Model.getVarByName("x[{},{}]".format(i,j)).start = x_val[i][j]
        #         Model.getVarByName("z[{},{}]".format(i,j)).start = z_val[i][j]
        Model.update()

    def run_model(self, solution_t = None):
        """
        run the gurobi model
        """
        start_time = time.time() # 记录模型开始计算的时间
        Model = gp.Model('gurobi_model')
        self.build_model(Model) # 创建模型
        if self.time_limit is not None:
            Model.setParam("TimeLimit", self.time_limit) # 设置求解时间上限
        # Model.setParam('OutputFlag', 0) # 是否打印求解过程信息
        if solution_t is not None:
            self.set_init_solution(Model, solution_t) # 设置初始解
        # Model.Params.Method = 1
        # # 设置节点文件
        # Model.setParam("NodeFileStart", 0.5)
        # # 设置预求解参数
        # Model.setParam("PreSparsify", 2)
        # # 设置线程数
        # Model.setParam("Threads", 8)
        Model.optimize() # 求解开始
        end_time = time.time()
        # 记录模型的求解结果
        result_info = {}
        result_info["timecost"] = end_time - start_time # 获取模型的求解时间
        solu_t = [] # 记录决策变量t
        for i in range(self.A):
            var_name = f"t[{i}]"
            t_i = Model.getVarByName(var_name).X
            solu_t.append(t_i)
        solu_x = [] # 记录决策变量x
        for i in range(self.A):
            solu_x_i = []
            for j in range(self.K):
                x_i_j = Model.getVarByName(f"x[{i},{j}]").X
                solu_x_i.append(x_i_j)
            solu_x.append(solu_x_i)
        solu_z = [] # 记录决策变量z
        for i in range(self.A):
            solu_z_i = []
            for j in range(self.K):
                z_i_j = Model.getVarByName(f"z[{i},{j}]").X
                solu_z_i.append(z_i_j)
            solu_z.append(solu_z_i)
        result_info["task_start_time"] = solu_t # 获取每个任务开始执行的时间
        result_info["x_i_j"] = solu_x # 获取决策变量x
        result_info["z_i_j"] = solu_z # 获取决策变量z
        result_info["best_obj"] = Model.ObjVal # 获取模型的最优值
        result_info["upper_bound"] = Model.objBound # 获取模型的最优界

        return result_info

if __name__ == "__main__":
    num = 100 # 任务的数量
    # create data
    test_data = create_random_data.random_data(num) 
    # create instance
    test_instance = create_instance.Instance(test_data.tasks, test_data.tasks_dependency)
    # create gurobi model
    test_model = gurobi_model(test_instance, time_limit=100)
    # set initial solution
    heuristic_algorithm_tool = heuristic_OLB.heuristic_OLB(test_instance)
    solution_t, resource = heuristic_algorithm_tool.iter_optimization()
    # run gurobi model
    result_info = test_model.run_model(solution_t)
    # print result_info
    print("最优解为:", result_info["best_obj"])
    print("上界:",result_info["upper_bound"])