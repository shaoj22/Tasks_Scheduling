'''
File: data.py
Project: Job Orchestration
Description:
-----------
read data from csv
-----------
Author: 626
Created Date: 2023-0721
'''
import pandas as pd
import numpy as np
import math

class Data():
    def __init__(self,
                tasks_execution_time_file_path
                ):
        self.tasks_execution_time_file_path = tasks_execution_time_file_path
    
    def read_data(self):
        """
        read_data 读取数据
        Args:
            tasks_execution_time_file_path (str): 任务执行时间文件路径
        Returns:
            list: 任务列表 (node, earliest_time, latest_time, execution_time, resource_load)
        """
        # 读取数据
        df = pd.read_csv(self.tasks_execution_time_file_path, quotechar='"')
        column_names = df.columns.tolist()
        jobs_dict = {} # 任务字典
        jobs_denpendency_dict = {} # 任务依赖关系字典
        job_name_list = [] # 任务列表
        denpendency_job_name_list = [] # 前置任务列表
        for index, row in df.iterrows():
            # 处理执行时间
            job_name = row[column_names[0]]
            job_name = job_name[:-1]
            # 统计任务数量
            if job_name not in job_name_list:
                job_name_list.append(job_name)
            duration = row[column_names[-2]]
            duration = str(duration)
            duration = duration[1:-1]
            try :
                duration = int(duration)
            except ValueError:
                continue
            if job_name in jobs_dict:
                jobs_dict[job_name].append(duration)
            else:
                jobs_dict[job_name] = [duration]
            # 处理任务依赖关系
            jobs_denpendency_name = row[column_names[-1]]
            jobs_denpendency_name = str(jobs_denpendency_name)
            jobs_denpendency_name = jobs_denpendency_name[1:]
            # 统计前置任务数量
            if jobs_denpendency_name not in denpendency_job_name_list and jobs_denpendency_name != '':
                denpendency_job_name_list.append(jobs_denpendency_name)
            if job_name in jobs_denpendency_dict and jobs_denpendency_name not in jobs_denpendency_dict[job_name] and jobs_denpendency_name != '':
                jobs_denpendency_dict[job_name].append(jobs_denpendency_name)
            else:
                jobs_denpendency_dict[job_name] = [jobs_denpendency_name]
        # 处理不存在的任务
        for key in jobs_denpendency_dict:
            for i in range(len(jobs_denpendency_dict[key])):
                if jobs_denpendency_dict[key][i] not in job_name_list:
                    jobs_denpendency_dict[key][i] = ''
        # 去掉每一个空字符
        new_jobs_denpendency_dict = {}
        for key in jobs_denpendency_dict:
            new_jobs_denpendency_dict[key] = []
            for i in range(len(jobs_denpendency_dict[key])):
                if jobs_denpendency_dict[key][i] != '':
                    new_jobs_denpendency_dict[key].append(jobs_denpendency_dict[key][i])
        # 存储数据
        i = 0 # 任务编号
        tasks = [] # 任务列表
        for key in jobs_dict:
            # 读取任务编号
            node = i
            # 读取任务名称
            task_name = key
            # 读取任务的持续时间
            execution_time = np.mean(jobs_dict[key])
            if execution_time < 1:
                execution_time = 1
            else:
                execution_time = math.ceil(execution_time)
            # 读取任务的资源负载
            resource_load = np.random.randint(30,80)/1000
            # 读取任务的最早完成时间
            earliest_time = np.random.randint(0,800)
            # 读取任务的最晚完成时间
            latest_time = np.random.randint(1439, 1440)
            # 读取任务的最晚开始时间
            lastest_start_time = latest_time-execution_time
            # add task
            task = {
                "task No.":node, # 任务编号
                "task_name":task_name, # 任务名称
                "execution_time":execution_time, # 任务的持续时间
                "resource_load":resource_load, # 任务的资源负载
                "earliest_time":earliest_time, # 任务最早完成时间
                "latest_time":latest_time, # 任务最晚完成时间
                "lastest_start_time":lastest_start_time, # 任务的最晚开始时间
            }
            tasks.append(task)
            i += 1
            # print("Information on task", i, "being processed", task)
        # 理任务依赖关系矩阵
        jobs_denpendency_matrix = np.zeros((len(job_name_list), len(job_name_list)))
        for i in range(len(job_name_list)):
            for j in range(len(new_jobs_denpendency_dict[job_name_list[i]])):
                for k in range(len(tasks)):
                    if tasks[k]["task_name"] == new_jobs_denpendency_dict[job_name_list[i]][j]:
                        forward_node = tasks[k]["task No."]
                        if forward_node != i:
                            jobs_denpendency_matrix[forward_node][i] = 1
        cycels = self.find_cycles(jobs_denpendency_matrix)
        for i in range(len(cycels)):
            jobs_denpendency_matrix[cycels[i][-1]][cycels[i][0]] = 0
        cycels = self.find_cycles(jobs_denpendency_matrix)
        self.print_cycles(cycels)

        # jobs_denpendency_matrix = self.boolean_reachable_matrix(jobs_denpendency_matrix, 100)

        return tasks, jobs_denpendency_matrix
    
    def handle_data(self, tasks, tasks_denpendency):
        # 计算每个任务的前置任务
        pretasks_list = [] # 所有任务的前置任务list
        for i in range(len(tasks)):
            each_pretasks_list = [] # 每个任务的前置任务list
            for j in range(len(tasks)):
                if tasks_denpendency[j][i] == 1: # j是i的前置任务
                    each_pretasks_list.append(j)
            pretasks_list.append(each_pretasks_list)
        # 计算起点任务
        start_tasks = []
        start_tasks_info = {}
        for i in range(len(pretasks_list)):
            if len(pretasks_list[i]) == 0:
                start_tasks_info = {
                    "task No.":i,
                    "task_name":tasks[i]["task_name"]
                }
                start_tasks.append(start_tasks_info)
        # 计算终点任务
        end_tasks = []
        end_tasks_info = {}
        is_end_task = True
        for i in range(len(tasks)):
            for j in range(len(pretasks_list)):
                if tasks[i]["task No."] in pretasks_list[j]:
                    is_end_task = False
                    break
            if is_end_task:
                end_tasks_info = {
                    "task No.":i,
                    "task_name":tasks[i]["task_name"]
                }
                end_tasks.append(end_tasks_info)
        # 计算既是起点又是终点的任务
        start_end_tasks = []
        for i in range(len(start_tasks)):
            for j in range(len(end_tasks)):
                if start_tasks[i]["task No."] == end_tasks[j]["task No."]:
                    start_end_tasks.append(start_tasks[i])
        return start_tasks, end_tasks, start_end_tasks

    def data_to_csv(self, tasks, tasks_denpendency):
        # init the information of tasks
        tasks_node = []
        tasks_name = []
        tasks_execution_time = []
        tasks_resource_load = []
        tasks_eraliest_time = []
        tasks_latest_time = []
        # get the information of tasks
        for i in range(len(tasks)):
            tasks_node.append(tasks[i]["task No."])
            tasks_name.append(tasks[i]["task_name"])
            tasks_execution_time.append(tasks[i]["execution_time"])
            tasks_resource_load.append(tasks[i]["resource_load"])
            tasks_eraliest_time.append(tasks[i]["earliest_time"])
            tasks_latest_time.append(tasks[i]["latest_time"])
        tasks_result_info = {
            "task No.":tasks_node,
            "task_name":tasks_name,
            "execution_time":tasks_execution_time,
            "resource_load":tasks_resource_load,
            "earliest_time":tasks_eraliest_time,
            "latest_time":tasks_latest_time,
        }
        user_input = {
            "task No.":tasks_node,
            "task_name":tasks_name,
            "earliest_time":tasks_eraliest_time,
            "latest_time":tasks_latest_time,
        }
        tasks_result_info = pd.DataFrame(tasks_result_info)
        tasks_result_info.to_csv("Appendix_3_Job_Scheduling.csv", index=False)
        tasks_denpendency = pd.DataFrame(tasks_denpendency)
        tasks_denpendency.to_csv("Appendix_2_Tasks_Denpendency.csv", index=False)
        user_input = pd.DataFrame(user_input)
        user_input.to_csv("Appendix_1_User_Input.csv", index=False)

    def handle_data_to_csv(self, start_tasks, end_tasks):
        start_tasks_node = []
        start_tasks_name = []
        end_tasks_node = []
        end_tasks_name = []
        for i in range(len(start_tasks)):
            start_tasks_node.append(start_tasks[i]["task No."])
            start_tasks_name.append(start_tasks[i]["task_name"])
        for i in range(len(end_tasks)):
            end_tasks_node.append(end_tasks[i]["task No."])
            end_tasks_name.append(end_tasks[i]["task_name"])
        start_tasks_info = {
            "task No.":start_tasks_node,
            "task_name":start_tasks_name,
        }
        end_tasks_info = {
            "task No.":end_tasks_node,
            "task_name":end_tasks_name,
        }
        start_tasks_info = pd.DataFrame(start_tasks_info)
        start_tasks_info.to_csv("Start_Tasks.csv", index=False)
        end_tasks_info = pd.DataFrame(end_tasks_info)
        end_tasks_info.to_csv("End_Tasks.csv", index=False)

    def find_cycles(self, A):
        """
        find_cycles 寻找环
        Args:
            A (list): 任务依赖关系矩阵
        Returns:
            list: 环列表
        """
        def dfs(node, path, visited):
                path.append(node)
                visited[node] = 1
                for neighbor in range(len(A[node])):
                    if A[node][neighbor] == 1:
                        if neighbor in path:
                            cycle_start = path.index(neighbor)
                            cycle = path[cycle_start:]
                            if len(cycle) > 1:  # Ignore cycles of length 1
                                cycles.append(cycle)
                        elif visited[neighbor] == 0:
                            dfs(neighbor, path, visited)
                path.pop()
                visited[node] = 2
        n = len(A)
        cycles = []
        visited = [0] * n

        for i in range(n):
            if visited[i] == 0:
                dfs(i, [], visited)
                print("check task No.", i, "being processed")

        return cycles

    def print_cycles(self, cycles):
        """
        print_cycles 打印环
        Args:
            cycles (list): 环列表
        """
        for idx, cycle in enumerate(cycles, start=1):
            print(f"Cycle {idx}: {cycle}")

    def boolean_reachable_matrix(self, adj_matrix, max_steps):
        reachable = np.copy(adj_matrix)
        for _ in range(max_steps - 1):
            reachable = (np.dot(reachable, adj_matrix) > 0).astype(int)
    
        return reachable.astype(int)


if  __name__ == '__main__':
    data = Data(tasks_execution_time_file_path='C:\\Users\\93561\\Desktop\\code\\Job_Orchestration\\utils\\new_data.csv')
    tasks, tasks_denpendency = data.read_data()
    print(len(tasks))
    print(len(tasks_denpendency))
    data.data_to_csv(tasks, tasks_denpendency)
