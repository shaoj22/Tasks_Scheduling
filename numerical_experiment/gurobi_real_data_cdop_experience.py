'''
File: gurobi_real_data_cdop_experience.py
Project: Job Orchestration
Description:
-----------
using the gurobi algorithem to solve the cdop job orchestration problem
-----------
Author: 626
Created Date: 2023-0825
'''

import sys
sys.path.append("..")
import pandas as pd
from utils import create_instance
from gurobi_algorithm import gurobi_model
from heuristic_algorithm import heuristic_OLB
from utils import export_results
from utils import draw_pictures

# create data
tasks_df = pd.read_csv("Job_Scheduling_Cdop.csv")
tasks_dependency_df = pd.read_csv("Tasks_Dependency_Cdop.csv")
tasks_matrix = tasks_df.values.tolist()
tasks_dependency = tasks_dependency_df.values.tolist()
tasks = []
task_num = len(tasks_df)
for i in range(len(tasks_matrix)):
    node = tasks_matrix[i][0]
    task_name = tasks_matrix[i][1]
    execution_time = tasks_matrix[i][2]
    resource_load = tasks_matrix[i][3]
    earliest_time = tasks_matrix[i][4]
    latest_time = tasks_matrix[i][5]
    task = {
                "task_No":node, # 任务编号
                "task_name": task_name,
                "earliest_time":earliest_time, # 任务最早完成时间
                "latest_time":latest_time, # 任务最晚完成时间
                "execution_time":execution_time, # 任务的持续时间
                "resource_load":resource_load, # 任务的资源负载
                "latest_start_time":latest_time-execution_time, # 任务的最晚开始时间
            }
    tasks.append(task)
# create instance
instance = create_instance.Instance(tasks, tasks_dependency)
# create heuristic algorithm
heuristic_algorithm_tool = heuristic_OLB.heuristic_OLB(instance)
# get heuristic solution
solution_t, resource = heuristic_algorithm_tool.iter_optimization()
# create gurobi model
gurobi_algorithm = gurobi_model.gurobi_model(instance, time_limit=30)
# run gurobi model
result_info = gurobi_algorithm.run_model(solution_t)
# draw chart
draw_pictures.draw_resource_load_chart(result_info["task_start_time"], tasks)
# export the results of gurobi algorithm into csv file
export_results.export_results_to_csv(result_info["task_start_time"], tasks, "cdop_gurobi")

