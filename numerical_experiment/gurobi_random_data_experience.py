'''
File: gurobi_random_data_experience.py
Project: Job Orchestration
Description:
-----------
using the gurobi algorithm to do some experience for the job orchestration problem
-----------
Author: 626
Created Date: 2023-0825
'''


from utils import create_random_data
from utils import create_instance
from gurobi_algorithm import gurobi_model
from heuristic_algorithm import heuristic_OLB
import time 
import xlwt
# 构造表格的格式
book = xlwt.Workbook(encoding='utf-8')
sheet = book.add_sheet("solution")
# 构建表格的表头
sheet.write(0, 0, "算例编号")
sheet.write(0, 1, "任务规模")
sheet.write(0, 2, "Gurobi_upper_bound")
sheet.write(0, 3, "Gurobi_lower_bound")
sheet.write(0, 4, "Gurobi_gap")
sheet.write(0, 5, "Gurobi_time")
sheet.write(0, 6, "Heuristic")
sheet.write(0, 7, "Heuristic_time")
sheet.write(0, 8, "Gap")
# 产生每个算例
for exp_num in range(0, 21):
    # set experiment tasks number
    exp_tasks_num = (exp_num + 1) * 100
    # create data
    exp_data = create_random_data.random_data(exp_tasks_num)
    # create instance
    exp_instance = create_instance.Instance(exp_data.tasks, exp_data.tasks_dependency)
    # create gurobi
    exp_gurobi_tool = gurobi_model.gurobi_model(exp_instance, time_limit=900)
    # create heuristic
    exp_heuristic_tool = heuristic_OLB.heuristic_OLB(exp_instance)
    # run heuristic
    start_time1 = time.time()
    solution_t, resource = exp_heuristic_tool.iter_optimization()
    end_time1 = time.time()
    # run gurobi
    start_time2 = time.time()
    exp_gurobi_result = exp_gurobi_tool.run_model(solution_t)
    end_time2 = time.time()
    # write data to excel
    sheet.write(exp_num + 1, 0, exp_num + 1)
    sheet.write(exp_num + 1, 1, exp_tasks_num)
    sheet.write(exp_num + 1, 2, round(exp_gurobi_result['best_obj'],4))
    sheet.write(exp_num + 1, 3, round(exp_gurobi_result['upper_bound'],4))
    sheet.write(exp_num + 1, 4, round((exp_gurobi_result['best_obj'] - exp_gurobi_result['upper_bound'])/exp_gurobi_result['upper_bound'],4))
    sheet.write(exp_num + 1, 5, round(end_time2 - start_time2,4))
    sheet.write(exp_num + 1, 6, round(resource,4))
    sheet.write(exp_num + 1, 7, round(end_time1 - start_time1,4))
    sheet.write(exp_num + 1, 8, round((resource - exp_gurobi_result['best_obj'])/resource,4))
    save_path = "C:\\Users\\93561\\Desktop\\code\\Tasks_Scheduling\\numerical_experiment\\gurobi_numerical_experiment.xls"
    book.save(save_path)