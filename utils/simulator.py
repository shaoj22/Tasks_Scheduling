'''
File: simulator.py
Project: Job Orchestration
Description:
-----------
Simulation to model the uncertainty of the forecasting effort, including execution time and resource loading
-----------
Author: 626
Created Date: 2023-0829
'''
import sys
sys.path.append("..")
from functional_module import realtime_scheduling_function
import read_data
import create_instance
from heuristic_algorithm import heuristic_OLB
from utils import draw_pictures
import numpy as np

def simulator(instance, solution, hot_launch_interval=1440):
    """
    Simulation to model the uncertainty of the forecasting effort, including execution time and resource loading
    Args:
        instance (Instance): the instance of the problem
        solution (list): the solution of the problem
        hot_launch_interval: the interval time of the hot launch
    Returns:
        realtime_scheduling_info
    """
    # init data
    final_solution = [0 for i in range(len(instance.tasks))]
    realtime_scheduling_info = {
        "time_now": 0,
        "tasks": instance.tasks,
        "tasks_dependency": instance.tasks_dependency,
        "solution": solution,
        "scheduled_tasks": [],
        "unscheduled_tasks": [],
        "scheduling_tasks": [],
        "new_tasks": [],
        "new_tasks_dependency": [],
        "new_solution": [],
    }
    # update real data about the execution_time and resource_load
    def generate_random_change_time(mean, std_dev, max_change):
        change = np.random.normal(0, std_dev)  # 从均值为0的正态分布生成变化值
        change = np.clip(change, -max_change, max_change)  # 限制改变幅度在[-max_change, max_change]范围内
        result = mean + change
        result = max(result, 1)  # 确保结果不小于1

        return result
    def generate_random_change_resource(mean, std_dev, max_change):
        change = np.random.normal(0, std_dev)  # 从均值为0的正态分布生成变化值
        change = np.clip(change, -max_change, max_change)  # 限制改变幅度在[-max_change, max_change]范围内
        result = mean + change
        result = max(result, 0)  # 确保结果不小于0
        # print(result)
        return result
    for i in range(len(realtime_scheduling_info["tasks"])):
        max_change_time = int(realtime_scheduling_info["tasks"][i]["execution_time"]*0.1)
        max_change_resource = int(realtime_scheduling_info["tasks"][i]["resource_load"]*0.1)
        num = np.random.randint(0, 50)
        if num <= 30:
            instance.tasks[i]["execution_time"] = int(generate_random_change_time(realtime_scheduling_info["tasks"][i]["execution_time"], 3, max_change_time))
        if num >= 20:
            realtime_scheduling_info["tasks"][i]["resource_load"] = generate_random_change_resource(realtime_scheduling_info["tasks"][i]["resource_load"], 0.01, max_change_resource)
    resource_load_list = []
    tasks_parallelism_list = []
    # simulator each time
    for time in range(instance.time_cap):
        resource_load = 0
        tasks_parallelism = 0
        scheduled_tasks = []
        unscheduled_tasks = []
        scheduling_tasks = []
        # update scheduling, scheduled and unscheduled tasks
        for i in range(len(realtime_scheduling_info["solution"])):
            if realtime_scheduling_info["solution"][i] <= time and time < realtime_scheduling_info["solution"][i] + instance.tasks[i]['execution_time']:
                scheduling_tasks.append(i)
                # update resource load
                resource_load += instance.tasks[i]['resource_load']
                tasks_parallelism += 1
            if time >= realtime_scheduling_info["solution"][i] + instance.tasks[i]['execution_time']:
                scheduled_tasks.append(i)
            if time < realtime_scheduling_info["solution"][i]:
                unscheduled_tasks.append(i)
        resource_load_list.append(resource_load)
        tasks_parallelism_list.append(tasks_parallelism)
        # update realtime_scheduling_info
        realtime_scheduling_info["time_now"] = time
        realtime_scheduling_info["scheduled_tasks"] = scheduled_tasks
        realtime_scheduling_info["unscheduled_tasks"] = unscheduled_tasks
        realtime_scheduling_info["scheduling_tasks"] = scheduling_tasks
        # print("time now =", time, "resource_now =", round(resource_load,4), "scheduling_task_num =", len(scheduling_tasks), "scheduled_task_num =", len(scheduled_tasks), "unscheduled_task_num =", len(unscheduled_tasks))
        # Hot launch
        # each hot_launch_interval launch once
        if time%hot_launch_interval == 0 and time != 0:
            print("-----------------------------------------------------------------------------------------------------------")
            print('hot launch', time)
            print("-----------------------------------------------------------------------------------------------------------")
            realtime_scheduling_info = realtime_scheduling_function.realtime_scheduling_function(realtime_scheduling_info)

    # resource_list = []
    # for i in range(1440):
    #     cur_resource = 0
    #     for j in range(len(realtime_scheduling_info["solution"])):
    #         if realtime_scheduling_info["solution"][j] <= i and (realtime_scheduling_info["solution"][j] + realtime_scheduling_info["tasks"][j]["execution_time"]) > i:
    #             cur_resource += realtime_scheduling_info["tasks"][j]["resource_load"]
    #     resource_list.append(cur_resource)
    # for i in range(len(resource_load_list)):
    #     print(i, " ", resource_load_list[i], " ", resource_list[i], " ", tasks_parallelism_list[i])

    return final_solution, realtime_scheduling_info

if __name__ == "__main__":
    # get static scheduling solution
    tasks, tasks_dependency = read_data.read_data("tasks.csv", "tasks_dependency.csv")
    instance = create_instance.Instance(tasks, tasks_dependency)
    algorithm_tool = heuristic_OLB.heuristic_OLB(instance)
    solution, resource_cap = algorithm_tool.iter_optimization()
    # run simulator
    final_solution, realtime_scheduling_info = simulator(instance, solution, 1500)
    # draw the resource load
    draw_pictures.draw_resource_load_chart(realtime_scheduling_info["solution"], realtime_scheduling_info["tasks"])

    # print(realtime_scheduling_info["solution"])

           
        
    
