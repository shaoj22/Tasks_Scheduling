'''
File: random_create_data.py
Project: Job Orchestration
Description:
-----------
create random data for test gurobi model
-----------
Author: 626
Created Date: 2023-0704
'''
import numpy as np
import pandas as pd

class random_data():
    def __init__(self, task_num, seed=5):
        """
        init generate instance 生成算例
        Args:
            task_num (int): 任务的个数
            seed (int): 随机种子
        """
        self.task_num = task_num # 总任务数量
        self.tasks = self.generate_tasks(self.task_num, seed) # 任务详细信息
        self.tasks_dependency = self.generate_task_dependency(self.task_num, seed) # 任务依赖关系
        self.tasks_pretasks_list = self.calculate_pretasks_list() # 任务的前置任务列表

    def generate_tasks(self, task_num, seed):
        """
        generate_tasks 生成任务
        Args:
            task_num (int): 任务的个数
            seed (int): 随机种子
        Returns:
            list: 任务列表 (node, earliest_time, latest_time, execution_time, resource_load)
        """
        np.random.seed(seed)
        tasks = []
        for i in range(task_num):
            # generate_tasks
            node = i
            earliest_time = np.random.randint(0,1400)
            execution_time = np.random.randint(5,15)
            latest_time = np.random.randint(earliest_time + execution_time + 10, 1440)
            resource_load = np.random.randint(5,15)/1000
            # resource_load = 10/600
            # add task
            task = {
                "task No.":node, # 任务编号
                "task_name":"task_{}".format(node), # 任务名称
                "earliest_time":earliest_time, # 任务最早完成时间
                "latest_time":latest_time, # 任务最晚完成时间
                "execution_time":execution_time, # 任务的持续时间
                "resource_load":resource_load, # 任务的资源负载
                "latest_start_time":latest_time-execution_time, # 任务的最晚开始时间
            }
            tasks.append(task)

        return tasks
    
    def generate_task_dependency(self, task_num, seed):
        """
        generate_tasks 生成任务
        Args:
            task_num (int): 任务的个数
            seed (int): 随机种子
        Returns:
            list: 任务依赖关系列表
        """
        np.random.seed(seed)
        task_dependency = np.zeros((task_num, task_num)) # 所有任务与其它任务之间的依赖关系
        for i in range(task_num):
            dependency_num = np.random.randint(0,20) # 为每个任务产生依赖任务的个数
            for j in range(dependency_num):
                if_or_not = np.random.randint(1,10) # 是否会产生依赖关系
                if if_or_not <= 10:
                    dependency_who = np.random.randint(0,task_num)
                    if task_dependency[dependency_who,i] != 1 and self.tasks[i]["latest_time"] < self.tasks[dependency_who]["earliest_time"]:
                        task_dependency[i,dependency_who] = 1
        
        return task_dependency

    def random_data_to_csv(self, tasks, task_dependency, tasks_pretasks_list, file_name):
        """
        random_data_to_csv 将生成的数据写入csv文件
        Args:
            tasks (list): 任务列表
            task_dependency (list): 任务依赖关系列表
        """
        new_tasks = []
        for task in tasks:
            new_task = {
                "task No.":task["task No."],
                "task_name":task["task_name"],
                "execution_time":task["execution_time"],
                "resource_load":task["resource_load"],
                "earliest_time":task["earliest_time"],
                "latest_time":task["latest_time"],
            }
            new_tasks.append(new_task)
        new_tasks = pd.DataFrame(new_tasks)
        new_tasks.to_csv("Instances\\Job_Scheduling_Table_{}.csv".format(file_name), index=False)
        task_dependency = pd.DataFrame(task_dependency)
        task_dependency.to_csv("Instances\\Task_Dependency_Table_{}.csv".format(file_name), index=False)
        tasks_pretasks_list = pd.DataFrame(tasks_pretasks_list)
        tasks_pretasks_list.to_csv("Instances\\Tasks_Pretasks_List_Table_{}.csv".format(file_name), index=False)
    
    def calculate_pretasks_list(self):  
        """
        calculate all tasks's pretasks
        input tasks information
        output pretasks → a list  
        """
        pretasks_list = [] # 所有任务的前置任务list
        for i in range(self.task_num):
            each_pretasks_list = [] # 每个任务的前置任务list
            for j in range(self.task_num):
                if self.tasks_dependency[j][i] == 1: # j是i的前置任务
                    each_pretasks_list.append(j)
            pretasks_list.append(each_pretasks_list)
        
        return pretasks_list
                           
if __name__ == "__main__":
    # generate random data
    for num in range(1,16):
        task_num = num * 1000
        data = random_data(task_num)
        print("generate {} tasks".format(data.task_num))
        data.random_data_to_csv(data.tasks, data.tasks_dependency, data.tasks_pretasks_list, num)


