'''
File: cdop_data.py
Project: Job Orchestration
Description:
-----------
read data from cdop_csv to get some real data: tasks, tasks_denpendency
-----------
Author: 626
Created Date: 2023-0822
'''
import pandas as pd
import numpy as np

# 读取数据
cdop_df_1 = pd.read_excel('cdop_dependency.xlsx', sheet_name='usp_relation')
cdop_df_workflow = pd.read_excel('cdop_workflow.xlsx', sheet_name='dependency')
df_1_colume_names = cdop_df_1.columns.values.tolist()
tasks_dict = {}
tasks_name_list = []
for row in cdop_df_1.iterrows():
    row_data = row[1]
    task_name = row_data['script_name']
    task_name = str(task_name)
    task_name = task_name.strip()
    if task_name not in tasks_name_list:
        tasks_name_list.append(task_name)

# 加入报表任务
cdop_df_workflow_1 = pd.read_excel('cdop_workflow.xlsx', sheet_name='object_parameter')
for row in cdop_df_workflow_1.iterrows():
    row_data = row[1]
    temp_name = row_data['Owning platform']
    task_name = str(task_name)
    task_name = task_name.strip()
    if temp_name == 'PBI_refresh':
        task_name = row_data['related_script_nm']
    if task_name not in tasks_name_list:
        tasks_name_list.append(task_name)

# 加入依赖任务
for row in cdop_df_workflow.iterrows():
    row_data = row[1]
    task_name = row_data['object_name']
    task_name = str(task_name)
    task_name = task_name.strip()
    task_dependency_name = row_data['dependency_obj_name']
    task_dependency_name = str(task_dependency_name)
    task_dependency_name = task_dependency_name.strip()
    if task_name in tasks_name_list and task_dependency_name not in tasks_name_list:
        tasks_name_list.append(task_dependency_name)

# 清理掉非字符串元素，并保留以指定前缀开头的任务
prefixes_to_keep = ['ods', 'cam', 'dwd', 'dwc', 'rdm', 'pl']
cleaned_tasks = [
    task_name
    for task_name in tasks_name_list
    if isinstance(task_name, str) and any(task_name.startswith(prefix) for prefix in prefixes_to_keep)
]

# -------------------------------------------------------------------------------------------------------
# 去掉dwc、dwd、cam中非ms的任务
i = 0
while i < len(cleaned_tasks):
    if (cleaned_tasks[i][:3] == 'dwc' or cleaned_tasks[i][:3] == 'dwd' or cleaned_tasks[i][:3] == 'cam') and cleaned_tasks[i][4:6] != 'ms':
        cleaned_tasks.pop(i)
    else:
        i += 1
# -------------------------------------------------------------------------------------------------------

# 保存任务名称到 CSV 文件
df = pd.DataFrame({'task_name': cleaned_tasks})
csv_file_path = 'tasks_cdop.csv'
# 将 DataFrame 写入到 CSV 文件
# df.to_csv(csv_file_path, index=True)

# 处理任务依赖关系
previous_tasks_dict = {}
for row in cdop_df_workflow.iterrows():
    row_data = row[1]
    previous_task_name = row_data['dependency_obj_name']
    current_task_name = row_data['object_name']
    if previous_task_name in cleaned_tasks and current_task_name in cleaned_tasks:
        if current_task_name not in previous_tasks_dict:
            previous_tasks_dict[current_task_name] = []
        previous_tasks_dict[current_task_name].append(previous_task_name)

# 获得依赖关系矩阵
jobs_denpendency_matrix = np.zeros((len(cleaned_tasks), len(cleaned_tasks)))
for key in previous_tasks_dict:
    for i in range(len(previous_tasks_dict[key])):
        current_task_name = key
        previous_task_name = previous_tasks_dict[key][i]
        current_task_index = cleaned_tasks.index(current_task_name)
        previous_task_index = cleaned_tasks.index(previous_task_name)
        jobs_denpendency_matrix[previous_task_index][current_task_index] = 1

# 随机产生时间
tasks = []
old_task_df = pd.read_csv("tasks.csv")
old_tasks_matrix = old_task_df.values.tolist()
for i in range(len(cleaned_tasks)):
    # 读取任务的名称
    task_name = cleaned_tasks[i]
    # 读取任务的持续时间
    task_row = old_task_df[old_task_df['task_name'].str.lower() == task_name.lower()]
    if task_row.empty:
        execution_time = np.random.randint(999999, 1000000)
    else:
        execution_time = task_row['execution_time'].values[0]
    # 读取任务的资源负载
    resource_load = np.random.randint(30,80)/1000
    # 读取任务的最早完成时间和最晚完成时间
    if task_name[:3] == 'ods' or task_name[:3] == 'dwd' or task_name[:3] == 'rdm':
        earliest_time = 2 * 60 + 30
        latest_time = 4 * 60
    elif task_name[:3] == 'dwc' or task_name[:3] == 'cam' or task_name[:2] == 'pl':
        earliest_time = 7 * 60
        latest_time = 9 * 60
    # 读取任务的最晚开始时间
    lastest_start_time = latest_time - execution_time
    task = {
        'task_No.': i,
        'task_name': cleaned_tasks[i],
        "execution_time":execution_time, # 任务的持续时间
        "resource_load":resource_load, # 任务的资源负载
        "earliest_time":earliest_time, # 任务最早完成时间
        "latest_time":latest_time, # 任务最晚完成时间
        "lastest_start_time":lastest_start_time, # 任务的最晚开始时间
    }
    tasks.append(task)

# data to csv
def data_to_csv(tasks, tasks_denpendency):
    # init the information of tasks
    tasks_node = []
    tasks_name = []
    tasks_execution_time = []
    tasks_resource_load = []
    tasks_eraliest_time = []
    tasks_latest_time = []
    # get the information of tasks
    for i in range(len(tasks)):
        tasks_node.append(tasks[i]["task_No."])
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
    tasks_result_info.to_csv("Job_Scheduling_CDOP.csv", index=False)
    tasks_denpendency = pd.DataFrame(tasks_denpendency)
    tasks_denpendency.to_csv("Tasks_Dependency_CDOP.csv", index=False)
    # user_input = pd.DataFrame(user_input)
    # user_input.to_csv("Appendix_1_User_Input.csv", index=False)
data_to_csv(tasks, jobs_denpendency_matrix)
