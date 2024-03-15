'''
File: check_solution.py
Project: Job Orchestration
Description:
-----------
utils for the job orchestration, such as plt tools
-----------
Author: 626
Created Date: 2023-0719
'''
def check_solution(solution_t, tasks, tasks_dependency):
    """
        check the solution is feasible or not
    """
    def calculate_pre_tasks_list(task_num, tasks_dependency):
        """
        a 2D list for each tasks's pre_tasks
        """
        pre_tasks_list = [] # 所有任务的前置任务list
        for i in range(task_num):
            each_pre_tasks_list = [] # 每个任务的前置任务list
            for j in range(task_num):
                if tasks_dependency[j][i] == 1: # j是i的前置任务
                    each_pre_tasks_list.append(j)
            pre_tasks_list.append(each_pre_tasks_list)
            # print("calculate the pre_tasks:", "task num =", i, "pre_tasks:", each_pre_tasks_list)
        
        return pre_tasks_list
    # check the start time is feasible or not
    i1 = 0
    for i in range(len(solution_t)):
        if solution_t[i] < tasks[i]["earliest_time"]:
            i1 += 1
            print("start time mistakes:", False, i1)
    print("solution check: start time is feasible")
    # check the end time is feasible or not
    j = 0
    for i in range(len(solution_t)):
        if solution_t[i] + tasks[i]["execution_time"] > tasks[i]["latest_time"]:
            j += 1
            print ("task", i, "end time mistakes:", False, j , "complete time:", solution_t[i], "+", tasks[i]["execution_time"],"=",solution_t[i]+tasks[i]["execution_time"], "latset_time:", tasks[i]["latest_time"])
    print("solution check: end time is feasible")
    # check the pre_task is feasible or not
    k = 0
    pre_tasks_list = calculate_pre_tasks_list(len(solution_t), tasks_dependency)
    for i in range(len(solution_t)):
        for j in range(len(pre_tasks_list[i])):
            if solution_t[i] < solution_t[pre_tasks_list[i][j]] + tasks[pre_tasks_list[i][j]]["execution_time"]:
                k += 1
                print ("pre_task mistakes:", False, k)
    print("solution check: pre_task is feasible")
                
