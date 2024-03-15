'''
File: real-time_scheduling_function.py
Project: Job Orchestration
Description:
-----------
Solving Real-Time Scheduling Problems with Hot and Cold Start Haircuts for Job Orchestration Problem
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
import numpy as np

def realtime_scheduling_function(realtime_scheduling_info):
    '''
    The function of solving Real-Time Scheduling Problems with Hot and Cold Start Haircuts for Job Orchestration Problem
    Args:
        realtime_scheduling_info (dict): the information of real-time scheduling
    Returns:
        realtime_scheduling_info (dict): the information of real-time scheduling
    '''
    # fix tasks and tasks_dependency function
    def remove_rows_columns(tasks_dependency, scheduled_tasks):
        """
        Remove specified rows and columns from the tasks_dependency.
        Args:
            tasks_dependency (np.array): the tasks_dependency matrix
            scheduled_tasks (list): the list of scheduled tasks
        Returns:
            new_tasks_dependency (np.array): the new tasks_dependency matrix
        """
        # Convert the input tasks_dependency to a NumPy array if it's not already
        tasks_dependency = np.array(tasks_dependency)
        # Create a boolean mask to select the rows and columns to keep
        keep_rows = np.ones(tasks_dependency.shape[0], dtype=bool)
        keep_rows[scheduled_tasks] = False
        keep_cols = keep_rows
        # Create the resulting tasks_dependency by selecting the specified rows and columns
        new_tasks_dependency = tasks_dependency[keep_rows][:, keep_cols]
        
        return new_tasks_dependency

    # fix tasks and tasks_dependency
    new_tasks_dependency = remove_rows_columns(realtime_scheduling_info["tasks_dependency"], realtime_scheduling_info["scheduled_tasks"])
    new_tasks = [realtime_scheduling_info["tasks"][i] for i in range(len(realtime_scheduling_info["tasks"])) if i not in realtime_scheduling_info["scheduled_tasks"]]
    # realtime_scheduling_info["new_tasks"] = new_tasks
    # realtime_scheduling_info["new_tasks_dependency"] = new_tasks_dependency
    # Special handling of the execution time of scheduling_tasks
    for i in range(len(new_tasks)):
        if new_tasks[i]["task_No"] in realtime_scheduling_info["scheduling_tasks"]:
            new_tasks[i]["execution_time"] = new_tasks[i]["execution_time"] - (realtime_scheduling_info["time_now"] - realtime_scheduling_info["solution"][new_tasks[i]["task_No"]])
    # create instance
    new_instance = create_instance.Instance(new_tasks, new_tasks_dependency, start_time=realtime_scheduling_info["time_now"])
    # solve the problem
    algorithm_tool = heuristic_OLB.heuristic_OLB(new_instance)
    new_solution, new_resource_cap = algorithm_tool.iter_optimization()
    # update the solution
    realtime_scheduling_info["new_solution"] = new_solution
    for i in range(len(new_solution)):
        if new_tasks[i]["task_No"] in realtime_scheduling_info["unscheduled_tasks"]:
            realtime_scheduling_info["solution"][new_tasks[i]["task_No"]] = new_solution[i]
    # print(new_solution)
    return realtime_scheduling_info

if __name__ == "__main__":
    # test
    pass

    
