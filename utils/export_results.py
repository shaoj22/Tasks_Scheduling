'''
File: heuristic_OLB_experience.py
Project: Job Orchestration
Description:
-----------
putting the results of OLB heuristic algorithm into csv file 
-----------
Author: 626
Created Date: 2023-0720
'''
import pandas as pd

def export_results_to_csv(solution_t, tasks, file_name):
    '''
    Description:
    -----------
    export the results of OLB heuristic algorithm into csv file
    -----------
    Parameters:
    -----------
    Returns:
    -----------
    '''
    # init the information of tasks
    tasks_node = []
    tasks_name = []
    tasks_start_time = []
    tasks_end_time = []
    tasks_execution_time = []
    tasks_earliest_time = []
    tasks_latest_time = []
    tasks_resource_load = []
    # get the information of tasks
    for tasks_num in range(len(tasks)):
        tasks_node.append(tasks[tasks_num]["task_No"])
        tasks_name.append(tasks[tasks_num]["task_name"])
        tasks_start_time.append(solution_t[tasks_num])
        tasks_end_time.append(solution_t[tasks_num] + tasks[tasks_num]["execution_time"])
        tasks_execution_time.append(tasks[tasks_num]["execution_time"])
        tasks_earliest_time.append(tasks[tasks_num]["earliest_time"])
        tasks_latest_time.append(tasks[tasks_num]["latest_time"])
        tasks_resource_load.append(tasks[tasks_num]["resource_load"])
    result_info = {
        "task No.":tasks_node,
        "task_name": tasks_name,
        "start_time":tasks_start_time,
        "end_time":tasks_end_time,
        "execution_time":tasks_execution_time,
        "earliest_time":tasks_earliest_time,
        "latest_time":tasks_latest_time,
        "resource_load":tasks_resource_load,
    }
    # export the results of OLB heuristic algorithm into csv file
    result_info = pd.DataFrame(result_info)
    result_info.to_csv("C:\\Users\\93561\\Desktop\\code\\Tasks_Scheduling\\utils\\Instances_results\\Job_Scheduling_Results_Table_{}.csv".format(file_name), index=False)


