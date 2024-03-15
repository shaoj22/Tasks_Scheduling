'''
File: heuristic_OLB_random_data_experience.py
Project: Job Orchestration
Description:
-----------
using the OLB heuristic algorithm to do some random data experience for the job orchestration problem
-----------
Author: 626
Created Date: 2023-0718
'''
import sys
sys.path.append("..")
from utils import create_instance
from utils import export_results
from heuristic_algorithm import heuristic_OLB
import time
import pandas as pd

Instances_results = []
for num in range(1,16):
    # create data
    tasks_df = pd.read_csv("C:\\Users\\93561\\Desktop\\code\\Tasks_Scheduling\\utils\\Instances\\Job_Scheduling_Table_{}.csv".format(num))
    tasks_dependency_df = pd.read_csv("C:\\Users\\93561\\Desktop\\code\\Tasks_Scheduling\\utils\\Instances\\Task_Dependency_Table_{}.csv".format(num))
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
                    "task No.":node, # 任务编号
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
    # create OLB heuristic algorithm
    heuristic_algorithm_tool = heuristic_OLB.heuristic_OLB(instance)
    # run OLB heuristic algorithm
    start_time = time.time()
    solution_t, resource = heuristic_algorithm_tool.iter_optimization()
    end_time = time.time()
    # export results
    export_results.export_results_to_csv(solution_t, instance.tasks, num)
    Instances_results_one = []
    Instances_results_one.append(num)
    Instances_results_one.append(task_num)
    Instances_results_one.append(round(end_time-start_time, 4))
    Instances_results_one.append(round(resource, 4))    
    Instances_results.append(Instances_results_one)

columns = ["Instance No.", "task_num", "Total time", "Total resource"]
instances_df = pd.DataFrame(Instances_results, columns=columns)
instances_df.to_csv("C:\\Users\\93561\\Desktop\\code\\Tasks_Scheduling\\utils\\Instances_results.csv", index=False)
