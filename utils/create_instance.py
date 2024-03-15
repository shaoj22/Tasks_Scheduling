'''
File: create_instance.py
Project: Job Orchestration
Description:
-----------
Store all job information, including tasks and tasks_dependency, into instance
-----------
Author: 626
Created Date: 2023-0823
'''

class Instance():
    def __init__(self, tasks, tasks_dependency, start_time=0):
        """
        Args:
            task_num (int): 任务的数量
            tasks: 任务的信息
                tasks[i]['task_No'] (int): 任务编号
                tasks[i]['task_name'] (str): 任务名称
                tasks[i]['execution_time'] (int): 完成每个任务需要的执行时间
                tasks[i]['resource_load'] (int)：完成每个任务需要的资源负载
                tasks[i]['earliest_time'] (int): 每个任务的最早完成时间
                tasks[i]['latest_time'] (int): 每个任务的最晚完成时间
                tasks[i]['latest_start_time'] (int): 每个任务的最晚开始时间
            tasks_dependency (0-1): 二维列表：任务之间是否存在依赖关系
            start_time (int): 作业开始时间
            time_cap (int): 一天的分钟数
            resource_cap (int): 一天的资源上限
            resource_gap (float): 用于控制资源负载的波动情况
            accept_resource_gap (float): 用于控制资源负载的精度
            pre_tasks_list (list): 作业任务的前置任务列表
            resource_lower_bound (float): 资源负载的下界
        """
        self.task_num = len(tasks)
        self.tasks = tasks
        self.tasks_dependency = tasks_dependency
        self.start_time = start_time
        self.time_cap = 1440 # 一天的分钟数
        self.resource_cap = 1 # 一天的资源上限
        self.resource_gap = 1.2 # 用于控制资源负载的波动情况
        self.accept_resource_gap = 0.0001 # 用于控制资源负载的精度
        self.pre_tasks_list = self.get_pre_tasks_list() # 作业任务的前置任务列表
        self.resource_lower_bound = self.calculate_resource_lower_bound(self.time_cap - self.start_time) # 资源负载的下界

    def get_pre_tasks_list(self):  
        """
        calculate all tasks's pre_tasks_list
        """
        pre_tasks_list = [] # 所有作业任务的前置任务list
        for i in range(self.task_num):
            each_pre_tasks_list = [] # 每个任务的前置任务list
            for j in range(self.task_num):
                if self.tasks_dependency[j][i] == 1: # j是i的前置任务
                    each_pre_tasks_list.append(j)
            pre_tasks_list.append(each_pre_tasks_list)

        return pre_tasks_list

    def calculate_resource_lower_bound(self, time_across):
        """
        calculate resource lower bound
        """
        resource_sum = 0
        for i in range(self.task_num):
            resource_sum += self.tasks[i]["resource_load"] * self.tasks[i]["execution_time"]

        return resource_sum/time_across
