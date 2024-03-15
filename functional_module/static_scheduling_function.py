'''
File: static_scheduling_function.py
Project: Job Orchestration
Description:
-----------
static scheduling function for job orchestration problem
-----------
Author: 626
Created Date: 2023-0828
'''

import sys
sys.path.append("..")
from utils import create_instance
from utils import read_data
from heuristic_algorithm import heuristic_OLB
from utils import export_results

def static_scheduling_function(tasks_file_path, tasks_dependency_file_path):
    '''
    Args:
        tasks_file_path (str): the path of the tasks file
        tasks_dependency_file_path (str): the path of the tasks dependency file
    Returns:
        solution (list): the solution of the static scheduling function
    '''
    # read data
    tasks, tasks_dependency = read_data.read_data(tasks_file_path, tasks_dependency_file_path)
    # create instance
    instance = create_instance.Instance(tasks, tasks_dependency)
    # create heuristic OLB
    algorithm_tool = heuristic_OLB.heuristic_OLB(instance)
    # run heuristic OLB
    solution, resource_cap = algorithm_tool.iter_optimization()
    # export results
    export_results.export_results_to_csv(solution, tasks, "static_scheduling_function")

    return solution

if __name__ == "__main__":
    solution  = static_scheduling_function(tasks_file_path='tasks.csv', tasks_dependency_file_path='tasks_dependency.csv')