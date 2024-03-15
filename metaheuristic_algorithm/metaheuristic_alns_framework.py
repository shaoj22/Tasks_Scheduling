'''
File: mataheuristic_alns_framework.py
Project: Job Orchestration
Description:
-----------
mataheuristic ALNS algorithem framework for job orchestration problem
-----------
Author: 626
Created Date: 2023-0712
'''
import numpy as np
import matplotlib.pyplot as plt
import math
import utils
import time
import tqdm

class ALNS_framework:
    """
    Base framework class of ALNS algorithm
        ALNS算法的通用框架,实际使用时,需要继承该类,并实现以下方法：
            1. get_operators_list: 返回一个operator的list,每个operator都是一个类,实现了get方法 
            2. solution_init: 返回一个初始解
            3. cal_objective: 计算解的目标函数值
    """
    def __init__(self, iter_num):
       # set iteration number
       self.iter_num = iter_num
       # set params
       ## 1. ALNS params
       self.adaptive_period = 10000
       self.sigma1 = 2
       self.sigma2 = 1
       self.sigma3 = 0.1
       ## 2. SA params
       self.max_temp = 1
       self.min_temp = 0
       self.cooling_rate = 0.98
       self.cooling_period = 10000

    # to be implemented in subclass
    def set_operators_list(self):
        self.operators_list = []
        raise NotImplementedError

    # to be implemented in subclass
    def solution_init(self):
        raise NotImplementedError
    
    # to be implemented in subclass
    def cal_objective(self):
        raise NotImplementedError 

    def reset(self):
        self.operators_scores = np.ones(len(self.operators_list))
        self.operators_steps = np.ones(len(self.operators_list))
        self.obj_iter_process = []
    
    def SA_accept(self, detaC, temperature):
        return math.exp(-detaC / temperature)

    def temperature_update(self, temperature, step):
        if step % self.cooling_period == 0: # update temperature by static steps
            temperature *= self.cooling_rate
        temperature = max(self.min_temp, temperature)
        return temperature

    def choose_operator(self):
        weights = self.operators_scores / self.operators_steps
        prob = weights / sum(weights)
        return np.random.choice(range(len(self.operators_list)), p=prob)
    
    def get_neighbour(self, solution, operator):
        return operator.get(solution)

    def show_process(self):
        y = self.process
        x = np.arange(len(y))
        plt.plot(x, y)
        plt.title("Iteration Process of ALNS")
        plt.xlabel("Iteration")
        plt.ylabel("Objective")
        plt.show()

    def run(self):
        cur_solution = self.solution_init() 
        cur_obj = self.cal_objective(cur_solution)
        self.best_solution = cur_solution
        self.best_obj = cur_obj
        temperature = self.max_temp
        for step in tqdm.trange(self.iter_num, desc="ALNS Iteration"):
            opt_i = self.choose_operator()
            new_solution = self.get_neighbour(cur_solution, self.operators_list[opt_i])
            new_obj = self.cal_objective(new_solution)
            # obj: minimize
            if new_obj < self.best_obj:
                self.best_solution = new_solution
                self.best_obj = new_obj
                cur_solution = new_solution
                cur_obj = new_obj
                self.operators_scores[opt_i] += self.sigma1
                self.operators_steps[opt_i] += 1
            elif new_obj < cur_obj: 
                cur_solution = new_solution
                cur_obj = new_obj
                self.operators_scores[opt_i] += self.sigma2
                self.operators_steps[opt_i] += 1
            elif np.random.random() < self.SA_accept((new_obj-cur_obj)/cur_obj, temperature):
                cur_solution = new_solution
                cur_obj = new_obj
                self.operators_scores[opt_i] += self.sigma3
                self.operators_steps[opt_i] += 1
            # reset operators weights
            if step % self.adaptive_period == 0: 
                self.operators_scores = np.ones(len(self.operators_list))
                self.operators_steps = np.ones(len(self.operators_list))
            # update SA temperature
            temperature = self.temperature_update(temperature, step)
            # record
            self.obj_iter_process.append(cur_obj)
            tqdm.set_postfix({
                "best_obj" : self.best_obj, 
                "cur_obj" : cur_obj, 
                "temperature" : temperature
            })
        return self.best_solution, self.best_obj