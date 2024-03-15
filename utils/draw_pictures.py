'''
File: draw_pictures.py
Project: Job Orchestration
Description:
-----------
Three mapping tools for Job Orchestration, including Gantt charts, resource load charts, and task parallelism charts.
-----------
Author: 626
Created Date: 2023-0823
'''
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import networkx as nx
import matplotlib.pyplot as plt
import math
import pandas as pd  

def draw_resource_load_chart(solution_t, tasks):
    """
    绘制调度结果的资源负载图
    input:
        solution_t: 调度结果的开始时间
        tasks: 任务的信息
    output:
        每个时刻的资源负载
    """
    # 处理任务资源负载
    resource_list = []
    for i in range(1440):
        cur_resource = 0
        for j in range(len(solution_t)):
            if solution_t[j] <= i and (solution_t[j] + tasks[j]["execution_time"]) > i:
                cur_resource += tasks[j]["resource_load"]
        resource_list.append(cur_resource)
    print(max(resource_list))
    # 创建子图
    fig, ax = plt.subplots(figsize=(12, 6))
    # 生成x轴刻度标签
    x_labels = range(len(resource_list))
    # 减少数据点的显示数量，使用每隔一定间隔的数据点
    interval = max(len(resource_list) // 20, 1)
    x_labels_sampled = x_labels[::interval]
    data_sampled = resource_list[::interval]
    # 绘制折线图，使用平滑的线条
    x_smooth = np.linspace(min(x_labels), max(x_labels), 300)
    data_smooth = np.interp(x_smooth, x_labels, resource_list)
    ax.plot(x_smooth, data_smooth, color='b', linewidth=2, label='Resource Load')
    # 设置图形标题和轴标签
    ax.set_title('Line Chart - Resource Load')
    ax.set_xlabel('Time')
    ax.set_ylabel('Resource Load')
    ax.set_ylim(0, 1)
    # 设置x轴刻度标签
    ax.set_xticks(x_labels_sampled)
    ax.set_xticklabels(x_labels_sampled)
    # 设置y轴刻度标签
    y_labels = [i/5 for i in range(6)]
    ax.set_yticks(y_labels)
    ax.set_yticklabels(y_labels)
    # 添加网格线
    ax.grid(True, which='both', linestyle='--', linewidth = 0.5)
    # 添加图例
    ax.legend()
    # 显示图形
    plt.tight_layout()
    plt.show()

def draw_tasks_parallelism_chart(solution_t, tasks):
    """
    绘制调度结果并行任务图
    input:
        solution: 任务并行度数据
    output:
        每个时刻的任务并行度
    """
    parallelism_list = []
    for i in range(1440):
        cur_parallelism = 0
        for j in range(len(solution_t)):
            if solution_t[j] <= i and (solution_t[j] + tasks[j]["execution_time"]) > i:
                cur_parallelism += 1
        parallelism_list.append(cur_parallelism)
    # 生成x轴刻度标签
    x_labels = range(len(parallelism_list))
    # 减少数据点的显示数量，使用每隔一定间隔的数据点
    interval = max(len(parallelism_list) // 20, 1)
    x_labels_sampled = x_labels[::interval]
    data_sampled = parallelism_list[::interval]
    # 绘制折线图，使用平滑的线条
    x_smooth = np.linspace(min(x_labels), max(x_labels), 300)
    data_smooth = np.interp(x_smooth, x_labels, parallelism_list)
    
    # 创建图形并设置美化参数
    plt.figure(figsize=(12, 6))
    plt.plot(x_smooth, data_smooth, color='r', linewidth=2, label='Job Parallelism')
    # 设置图形标题和轴标签
    plt.title('Line Chart - Job Parallelism')
    plt.xlabel('Time')
    plt.ylabel('Job Parallelism')
    plt.ylim(0, 100)  # 将y轴上限设置为任务数量的最大值加上一些空间
    # 设置x轴刻度标签
    plt.xticks(x_labels_sampled)  # 旋转x轴刻度标签，以避免重叠
    # 添加网格线
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    # 添加图例
    plt.legend()
    # 显示图形
    plt.tight_layout()  # 调整布局，以确保图形各元素不重叠
    plt.show()

def draw_gantt_chart(solution_t, tasks):
    """
    绘制调度结果的甘特图
    input:
        solution_t: 调度结果的开始时间
        tasks: 每个任务的信息
        task_nodes: 任务节点
    output:
        甘特图
    """
    task_nodes = [i for i in range(len(solution_t))]
    execution_time = []
    for i in range(len(solution_t)):
        execution_time.append(tasks[i]["execution_time"])
    # 确定任务数量
    num_tasks = len(solution_t)
    # 设置图形大小
    fig_height = min(num_tasks * 0.3, 10)
    fig, ax = plt.subplots(figsize=(10, fig_height))
    # 设置y轴刻度标签和任务名称（折叠显示）
    step = max(1, num_tasks // 50)  # 控制每隔多少任务显示一个名称
    visible_task_names = task_nodes[::step]
    visible_ticks = np.arange(0, num_tasks, step)
    ax.set_yticks(visible_ticks)
    ax.set_yticklabels(visible_task_names, fontsize=12)
    # 确定时间范围，限制显示前200个时间步
    max_time = min(max(solution_t) + max(execution_time), 1440)
    ax.set_xlim(0, max_time)
    # 使用viridis颜色映射
    cmap = plt.get_cmap('viridis', num_tasks)
    # 遍历每个任务
    for i in range(num_tasks):
        start_time = solution_t[i]
        duration = execution_time[i]
        end_time = start_time + duration
        # 限制在时间范围内绘制甘特图线段
        if start_time < max_time:
            y_val = i
            ax.hlines(y=y_val, xmin=start_time, xmax=min(end_time, max_time), colors=cmap(i), linewidth=3)
    # 设置图形标题和轴标签
    ax.set_title('gantt chart', fontsize=18, fontweight='bold')
    ax.set_xlabel('time', fontsize=14)
    ax.set_ylabel('task', fontsize=14)
    # 隐藏y轴刻度线
    ax.yaxis.set_ticks_position('none')
    # 移除上方和右侧的边框
    sns.despine(top=True, right=True)
    # 添加网格线
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)
    # 设置背景颜色
    plt.gca().set_facecolor('#f0f0f0')
    # 显示图形
    plt.tight_layout()
    plt.show()

def draw_link_chart(solution_t, tasks, tasks_dependency):
    '''
    绘制调度结果的有向无环图
    input:
        solution_t: 调度结果的开始时间
        tasks: 每个任务的信息
        tasks_dependency: 任务的依赖关系
    output:
        有向无环图
    '''
    names = []
    for i in range(len(tasks)):
        name = tasks[i]['task_name'] + " : " + str(solution_t[i])
        names.append(name)
    G = nx.DiGraph()
    num_nodes = len(tasks_dependency)
    G.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(num_nodes):
            if tasks_dependency[i][j] == 1:
                G.add_edge(i, j)
    
    # Determine the ranges based on start times in S
    min_start_time = min(solution_t)
    max_start_time = max(solution_t)
    range_count = math.ceil((max_start_time - min_start_time + 1) / 50)
    ranges = [(min_start_time + i * 50, min_start_time + (i + 1) * 50) for i in range(range_count)]
    
    # Group nodes based on start times and ranges
    groups = {r: [] for r in ranges}
    for node, start_time in enumerate(solution_t):
        for r in ranges:
            if r[0] <= start_time < r[1]:
                groups[r].append(node)
    
    # Assign layers based on groups
    layers = []
    for r in ranges:
        layers.append(groups[r])
    
    pos = nx.shell_layout(G, nlist=layers)
    node_colors = '#66c2a5'
    edge_colors = '#8da0cb'
    arrow_color = '#1f78b4'
    text_color = '#333333'
    node_sizes = 1200
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes)
    
    for group, nodes in groups.items():
        for node in nodes:
            nx.draw_networkx_labels(G, {node: pos[node] + [0, 0.05]}, labels={node: names[node]}, font_size=8, font_color=text_color)
            plt.text(pos[node][0], pos[node][1], f"{node}", horizontalalignment='center', verticalalignment='center', fontsize=12, color=text_color)
    
    for edge in G.edges:
        if tasks_dependency[edge[0]][edge[1]] == 1:
            nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color=edge_colors, width=2.0, alpha=0.7, arrows=False)
            arrow_pos = ((pos[edge[0]][0] + pos[edge[1]][0]) / 2, (pos[edge[0]][1] + pos[edge[1]][1]) / 2)
            plt.annotate("",
                         xy=pos[edge[1]], xycoords='data',
                         xytext=arrow_pos, textcoords='data',
                         arrowprops=dict(arrowstyle="->", color=arrow_color, linewidth=2))
    
    plt.title("Directed Acyclic Graph (DAG)", fontsize=16, color=text_color)
    plt.gca().xaxis.set_visible(False)
    plt.gca().yaxis.set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.grid(False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # check ZKD's result
    pass

