'''
File: heuristic_OLB.py
Project: Job Orchestration
Description:
-----------
Body code of the OLB heuristic algorithm for job orchestration problem
    · __init__ : init the heuristic OLB
    · iter_optimization : run the heuristic OLB for many times to get the best solution
    · run_OLB : run the heuristic OLB for only once with the given resource cap
    · task_assignment : at the time of time_now, get the task list that can be inserted
    · calculate_pre_tasks : calculate whether all pre_tasks of task have been finished
    · calculate_pre_tasks_list : calculate the pre_tasks list of each task
    · calculate_resource_lower_bound : calculate the resource lower bound of the problem
-----------
Author: 626
Created Date: 2023-0823
'''

import copy
import time
import sys
sys.path.append("..")
from utils import create_instance
from utils import read_data
from utils import draw_pictures

class heuristic_OLB():
    def __init__(self, instance):
        """
        Args:
            task_num (int): 任务的数量
            tasks: 任务的信息
                tasks[i]['task_No'] (int): 任务编号
                tasks[i]['task_name'] (str): 任务名称
                tasks[i]['execution_time'] (int): 完成每个任务需要的执行时间
                tasks[i]['resource_load'] (int)：完成每个任务需要的资源负载
                tasks[i]['earliest_time'] (int): 每个任务的最早完成时间
                tasks[i]['latest_time'] (int): 每个任务的最晚完成时间
                tasks[i]['latest_start_time'] (int): 每个任务的最晚开始时间
            tasks_dependency (0-1): 二维列表：任务之间是否存在依赖关系
            start_time (int): 作业开始时间
            time_cap (int): 一天的分钟数
            resource_cap (int): 一天的资源上限
            resource_gap (float): 用于控制资源负载的波动情况
            accept_resource_gap (float): 用于控制资源负载的精度
            pre_tasks_list (list): 作业任务的前置任务列表
            resource_lower_bound (float): 资源负载的下界
        """
        self.task_num = instance.task_num
        self.tasks = instance.tasks
        self.tasks_dependency = instance.tasks_dependency
        self.start_time = instance.start_time
        self.time_cap = instance.time_cap
        self.resource_cap = instance.resource_cap
        self.resource_gap = instance.resource_gap
        self.accept_resource_gap = instance.accept_resource_gap
        self.pre_tasks_list = instance.pre_tasks_list
        self.resource_lower_bound = instance.resource_lower_bound

    def iter_optimization(self):
        """
        iter_optimization 迭代优化
        run the heuristic OLB for many times to get the best solution
        """
        iter_num = 1 # 迭代次数
        resource_gap = self.resource_gap # 当前迭代的资源负载的gap
        upper_bound = self.resource_cap # 当前迭代的资源负载的上界
        while resource_gap >= self.accept_resource_gap: # 当gap小于可接受误差时，停止迭代
            print("iter_num =", iter_num, "resource_gap =", resource_gap, "upper_bound =", upper_bound)
            if upper_bound > resource_gap and upper_bound - resource_gap > self.resource_lower_bound:
                solu_t, scheduling_tasks, end_time_mistake_num = self.run_OLB(upper_bound - resource_gap) # 运行OLB算法
                if len(scheduling_tasks) == 0 and end_time_mistake_num == 0:
                # if len(scheduling_tasks) == 0:
                    solution_t = solu_t # 更新最优解
                    upper_bound = upper_bound - resource_gap # 更新上界
                    end_bound = upper_bound # 更新最终解
                    if resource_gap != self.resource_gap:
                        resource_gap = resource_gap/2
                else:
                    resource_gap = resource_gap/2
            else:
                resource_gap = resource_gap/2
            iter_num += 1
        return solution_t, end_bound
                
    def run_OLB(self, resource_cap):
        """
        runner for OBL heuristic algorithm, just running for once   
        Args:
            resource_cap (float): 当前输入的资源负载的上限 
        """
        end_time_mistake_num = 0 # 任务结束时间误差的个数
        solu_t = [0 for i in range(len(self.tasks))] # 初始化每个任务的开始执行时间
        scheduled_tasks = [] # 已经执行过的任务
        scheduling_tasks = [] # 正在执行的任务
        unscheduled_tasks = [i for i in range(len(self.tasks))] # 未执行的任务
        resource_now = 0 # 当前的资源负载
        for time_now in range(self.start_time, self.time_cap): # 新的time_now到来，更新此时的scheduling_tasks和resource_now
            check_list = copy.copy(scheduling_tasks)
            for i in range(len(check_list)): # update scheduling_tasks
                if time_now >= solu_t[check_list[i]] + self.tasks[check_list[i]]["execution_time"]:
                    scheduling_tasks.remove(check_list[i])
                    scheduled_tasks.append(check_list[i])
                    resource_now -= self.tasks[check_list[i]]["resource_load"]
            # 获取time_now插入的任务列表
            insert_tasks_list, unscheduled_tasks = self.task_assignment(time_now, unscheduled_tasks, resource_now, resource_cap, scheduled_tasks)
            if time_now < self.time_cap - 1:
                for i in range(len(insert_tasks_list)): # 更新solu_t和unscheduled_tasks
                    solu_t[insert_tasks_list[i]] = time_now
                    if self.tasks[insert_tasks_list[i]]["latest_start_time"] < solu_t[insert_tasks_list[i]]:
                        end_time_mistake_num += 1
                    scheduling_tasks.append(insert_tasks_list[i])
                    resource_now += self.tasks[insert_tasks_list[i]]["resource_load"]
                # print("time now =", time_now, "resource_now =", resource_now, "scheduling_task_num =", len(scheduling_tasks), "scheduled_task_num =", len(scheduled_tasks), "unscheduled_task_num =", len(unscheduled_tasks), "resource_upper_bound =", resource_cap)
            # else:
            #     print("OLB_heuristic_finished")

        return solu_t, scheduling_tasks, end_time_mistake_num

    def task_assignment(self, time_now, unscheduled_tasks, resource_now, resource_cap, scheduled_tasks):
        """
        at the time of time_now, get the task list that can be inserted
        Args:
            time_now (int): 当前时间
            unscheduled_tasks (list): 未执行的任务
            resource_now (float): 当前的资源负载
            resource_cap (float): 当前输入的资源负载的上限
            scheduled_tasks (list): 已经执行过的任务
        """
        ready_list = [] # 可以开始执行的任务
        insert_tasks_list = [] # 可以插入的任务
        ready_task_latest_start_time_list = [] # 可以插入的任务的最晚开始时间列表
        for i in range(len(unscheduled_tasks)): # 获取ready_list
            if self.tasks[unscheduled_tasks[i]]["earliest_time"] <= time_now and self.calculate_pre_tasks(scheduled_tasks, unscheduled_tasks[i]) == 1:
                ready_list.append(unscheduled_tasks[i])
                ready_task_latest_start_time_list.append(self.tasks[unscheduled_tasks[i]]["latest_start_time"])
        # print(time_now, "-------", ready_list)
        while len(ready_list) != 0: # 获取insert_tasks_list
            ready_task_latest_start_time = min(ready_task_latest_start_time_list)
            ready_index = ready_task_latest_start_time_list.index(ready_task_latest_start_time)
            insert_task = ready_list[ready_index]
            resource_now += self.tasks[insert_task]["resource_load"]
            if resource_now >= resource_cap: # 若加入后资源会超过上限，则不加入
                break
            else: # 若加入后资源不会超过上限，则加入
                insert_tasks_list.append(insert_task)
                unscheduled_tasks.remove(insert_task)
                ready_list.remove(insert_task)
                ready_task_latest_start_time_list.remove(ready_task_latest_start_time)
            
        return insert_tasks_list, unscheduled_tasks

    def calculate_pre_tasks(self, scheduled_tasks, task):
        """
        calculate whether all pre_tasks of task have been finished
        Args:
            scheduled_tasks (list): 已经执行过的任务
            task (int): 当前任务
        """
        pre_tasks_finished_or_not = 1 # 任务所有的前置任务是否都已完成，若是则为1，否则为0
        for i in range(len(self.pre_tasks_list[task])):
            if self.pre_tasks_list[task][i] not in scheduled_tasks:
                pre_tasks_finished_or_not = 0
                break
        
        return pre_tasks_finished_or_not

if __name__ == "__main__":
    # read data
    tasks, tasks_dependency = read_data.read_data("C:\\Users\\93561\\Desktop\\code\\TASKS_SCHEDULING\\utils\\tasks.csv", "C:\\Users\\93561\\Desktop\\code\\TASKS_SCHEDULING\\utils\\tasks_dependency.csv")
    # create instance
    instance = create_instance.Instance(tasks, tasks_dependency)
    # create heuristic algorithm tool
    algorithm_tool = heuristic_OLB(instance)
    # run OLB heuristic algorithm
    start_time = time.time()
    solution_t, resource = algorithm_tool.iter_optimization()
    end_time = time.time()
    print("time_cost:", end_time - start_time)
    # draw pictures
    draw_pictures.draw_gantt_chart(solution_t, instance.tasks)
    draw_pictures.draw_resource_load_chart(solution_t, instance.tasks)
    draw_pictures.draw_tasks_parallelism_chart(solution_t, instance.tasks)
    # draw_pictures.draw_link_chart(solution_t, instance.tasks, instance.tasks_dependency)
    # check the solution
    # check_tools = solution_check_utils.solution_check_utils()
    # check_tools.solution_check(test_instance.tasks, solution_t, test_instance.tasks_dependency)
    

