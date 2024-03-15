'''
File: use_preview_function.py
Project: Job Orchestration
Description:
-----------
use preview function for job orchestration problem
-----------
Author: 626
Created Date: 2023-0828
'''

import sys
sys.path.append("..")
from utils import create_instance
from utils import read_data
from utils import draw_pictures
from heuristic_algorithm import heuristic_OLB
from utils import export_results

def user_preview_function(new_tasks, new_solution, old_tasks, old_solution):
    '''
    Args:
        new_tasks (list): the new tasks
        new_solution (list): the new solution
        old_tasks (list): the old tasks
        old_solution (list): the old solution
    Returns:
        final_tasks (list): the final tasks
        final_solution (list): the final solution
    '''
    # Removing information about new tasks from old tasks
    final_tasks = []
    final_solution = []
    for task in old_tasks:
        if task['task_name'] not in [new_task['task_name'] for new_task in new_tasks]:
            final_tasks.append(task)
            final_solution.append(old_solution[task['task_No']])
    # append new tasks to final tasks
    for i in range(len(new_tasks)):
        final_tasks.append(new_tasks[i])
        final_solution.append(new_solution[i])
    # fix the final_tasks' task_No
    for i in range(len(final_tasks)):
        final_tasks[i]['task_No'] = i
    # export results
    export_results.export_results_to_csv(final_solution, final_tasks, 'user_preview_function')

    return final_tasks, final_solution
    
if __name__ == "__main__":
    # ------------------------------------------------------------------------------------------------------------
    # set old data path
    old_tasks_file_path = 'tasks.csv'
    old_tasks_dependency_file_path = 'tasks_dependency.csv'
    # read old data
    old_tasks, old_tasks_dependency = read_data.read_data(old_tasks_file_path, old_tasks_dependency_file_path)
    # create instance
    old_instance = create_instance.Instance(old_tasks, old_tasks_dependency)
    # create heuristic OLB
    algorithm_tool = heuristic_OLB.heuristic_OLB(old_instance)
    # run heuristic OLB
    old_solution, old_resource_cap = algorithm_tool.iter_optimization()
    # ------------------------------------------------------------------------------------------------------------
    # set new data path
    new_tasks_file_path = 'Job_Scheduling_Cdop.csv'
    new_tasks_dependency_file_path = 'Tasks_Dependency_Cdop.csv'
    # read new data
    new_tasks, new_tasks_dependency = read_data.read_data(new_tasks_file_path, new_tasks_dependency_file_path)
    # create instance
    new_instance = create_instance.Instance(new_tasks, new_tasks_dependency)
    # create heuristic OLB
    algorithm_tool = heuristic_OLB.heuristic_OLB(new_instance)
    # run heuristic OLB
    new_solution, new_resource_cap = algorithm_tool.iter_optimization()
    # ------------------------------------------------------------------------------------------------------------
    final_tasks, final_solution = user_preview_function(new_tasks, new_solution, old_tasks, old_solution)
    # ------------------------------------------------------------------------------------------------------------
    # draw resource load chart
    draw_pictures.draw_resource_load_chart(old_solution, old_tasks)
    draw_pictures.draw_resource_load_chart(new_solution, new_tasks)
    draw_pictures.draw_resource_load_chart(final_solution, final_tasks)
    