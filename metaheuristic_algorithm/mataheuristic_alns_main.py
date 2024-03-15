'''
File: mataheuristic_alns_framework.py
Project: Job Orchestration
Description:
-----------
mataheuristic ALNS algorithem main for job orchestration problem
-----------
Author: 626
Created Date: 2023-0712
'''
import metaheuristic_alns_framework


class ALNS_main(metaheuristic_alns_framework.ALNS_framework):
    """
    ALNS algorithm main for job orchestration problem
    input: ALNS_framework & instance & iter_num
    """
    def __init__(self, instance, iter_num):
        super().__init__(iter_num)
        self.instance = instance
        self.set_operators_list()
    
    def a(self):
        pass

if __name__ == "__main__":
    pass
