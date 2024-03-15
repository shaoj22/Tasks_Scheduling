'''
File: read_data.py
Project: Job Orchestration
Description:
-----------
Read normalized job data: tasks and tasks_dependency
-----------
Author: 626
Created Date: 2023-0823
'''
import pandas as pd

def read_data(file_path_1, file_path_2):
    """
    Args:
        file_path_1: tasks data path
        file_path_2: tasks_dependency data path
    Returns:
        tasks: tasks data
        tasks_dependency: tasks_dependency data
    """
    tasks_dataframe = pd.read_csv(file_path_1)
    tasks_dependency_dataframe = pd.read_csv(file_path_2)
    tasks_matrix = tasks_dataframe.values.tolist()
    tasks_dependency_matrix = tasks_dependency_dataframe.values.tolist()
    tasks = [] # information of tasks
    for i in range(len(tasks_matrix)):
        task = {
                    "task_No": tasks_matrix[i][0], # 任务编号
                    "task_name": tasks_matrix[i][1], # 任务名称
                    "execution_time": tasks_matrix[i][2], # 任务执行时间
                    "resource_load": tasks_matrix[i][3], # 任务的资源负载
                    "earliest_time": tasks_matrix[i][4], # 任务最早完成时间
                    "latest_time": tasks_matrix[i][5], # 任务最晚完成时间
                    "latest_start_time": tasks_matrix[i][5] - tasks_matrix[i][2], # 任务的最晚开始时间
                }
        tasks.append(task)
    
    return tasks, tasks_dependency_matrix

if __name__ == "__main__":
    tasks, tasks_dependency = read_data("C:\\Users\\93561\\Desktop\\code\\Tasks_Scheduling\\tasks.csv", "C:\\Users\\93561\\Desktop\\code\\Tasks_Scheduling\\tasks_denpendency.csv")
    print(tasks[0])