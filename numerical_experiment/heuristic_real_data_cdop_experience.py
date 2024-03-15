'''
File: heuristic_real_data_cdop_experience.py
Project: Job Orchestration
Description:
-----------
use the heuristic algorithm to solve the real data of cdop
-----------
Author: 626
Created Date: 2023-0825
'''
import sys
sys.path.append("..")
import pandas as pd
import time
from utils import create_instance
from heuristic_algorithm import heuristic_OLB 
from utils import draw_pictures
from utils import export_results
from utils import check_solution

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
# create heuristic algorithm
heuristic_algorithm_tool = heuristic_OLB.heuristic_OLB(instance)
# get heuristic solution
start_time = time.time()
solution_t, resource = heuristic_algorithm_tool.iter_optimization()
end_time = time.time()
print("time_cost:", end_time - start_time)
print("resource:", resource)
# draw chart
# draw_pictures.draw_gantt_chart(solution_t, instance.tasks)
draw_pictures.draw_resource_load_chart(solution_t, instance.tasks)
# draw_pictures.draw_tasks_parallelism_chart(solution_t, instance.tasks)
# draw_pictures.draw_link_chart(solution_t, instance.tasks, instance.tasks_dependency)
# save solution
# export_results.export_results_to_csv(solution_t, instance.tasks, "cdop")
ZKD_result_cdop_df = pd.read_csv("result_CDOP_RUB=0.192.csv")
ZKD_result_cdop = ZKD_result_cdop_df.values.tolist()
ZKD_solution_t = []
for i in range(len(ZKD_result_cdop_df)):
    ZKD_solution_t.append(ZKD_result_cdop[i][2])
draw_pictures.draw_resource_load_chart(ZKD_solution_t, instance.tasks)
check_solution.check_solution(ZKD_solution_t, instance.tasks, instance.tasks_dependency)