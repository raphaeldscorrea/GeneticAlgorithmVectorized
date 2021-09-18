
"""
Each SA parameter has associated a sampling distribution:
	a truncated normal distribution for numerical parameters
	a discrete distribution for categorical parameters.
"""

import sys
import os
import time
import numpy as np
import pandas as pd
import itertools
from instanceGenerator import Instance

from src.heuristics.simulated_anealling.simulatedAneallingII import SimAneal

class SAParameters():
    
    def __init__(self):
        
        # Parameters Vectors
        self.alpha = [0.96, 0.98, 0.99, 0.995, 0.997, 0.998]      
        self.initial_temperature = [10]
        self.neighbourhood_operator = ["reverse", "swap", "insert", "scramble", "inversion", "displacement"]
        self.num_iteration = [3, 4, 5]
        self.stopping_temperature = [1e-5]
        
        #self.alpha = [0.95, 0.96]
        #self.neighbourhood_operator = ["reverse", "swap", "scramble"]
        #self.num_iteration = [3,4]

#-----------------------------------------------------------------------------------#    
# Each parameter has associated a sampling distribution (discrete)
#-----------------------------------------------------------------------------------#
        
    def get_parameters_uniforme_distribution (self):
        parameters_list = [{"values":self.alpha, "prob":[(1/len(self.alpha))]*len(self.alpha)},
                          {"values":self.initial_temperature, "prob":[(1/len(self.initial_temperature))]*len(self.initial_temperature)},
                          {"values":self.neighbourhood_operator, "prob":[(1/len(self.neighbourhood_operator))]*len(self.neighbourhood_operator)},
                          {"values":self.num_iteration, "prob":[(1/len(self.num_iteration))]*len(self.num_iteration)},                        
                          {"values":self.stopping_temperature, "prob":[(1/len(self.stopping_temperature))]*len(self.stopping_temperature)}]
        
        return parameters_list
    
    def get_parameters_test_limit (self):
        parameters_configurations = list(itertools.product(self.alpha,self.initial_temperature,self.neighbourhood_operator,self.num_iteration,self.stopping_temperature))
        parameters_test_limit = {x: 0 for x in parameters_configurations}
        
        return parameters_test_limit

    def call_optimization (self, fitness_class, parameters_list, solution_size, instance): 
        first_solution = SAParameters.generate_random_solution(solution_size)
        first_fitness = fitness_class.generic_fitness(first_solution) 
        sa_obj = SimAneal(individual = first_solution,
                          fitness = first_fitness,
                          alpha = float(parameters_list[0]),
                          initial_temperature = float(parameters_list[1]),
                          neighbourhood_operator = str(parameters_list[2]),
                          num_iteration = int(parameters_list[3]),
                          stopping_temperature = float(parameters_list[4]))

        start = time.time()
        sa_fitness, sa_solution = sa_obj.calculate(fitness_class)
        end = time.time()
        #print( end-start )
        #print( sa_fitness )
        return sa_fitness, sa_solution
    
    @staticmethod  
    def generate_random_solution (size):
        solution = np.random.permutation(np.arange(size))
        solution = solution.astype(int)
        return solution
    
    @staticmethod
    def createConfigData (config_obj_list=None):
        data = {}
        data['alpha'] = []
        data['initial_temperature'] = []
        data['neighbourhood_operator'] = []
        data['num_iteration'] = []
        data['stopping_temperature'] =[]
        
        if config_obj_list is not None:
            for n in range(len(config_obj_list)):
                data['alpha'].append(config_obj_list[n].parameters[0])
                data['initial_temperature'].append(config_obj_list[n].parameters[1])
                data['neighbourhood_operator'].append(str(config_obj_list[n].parameters[2]))
                data['num_iteration'].append(config_obj_list[n].parameters[3])
                data['stopping_temperature'].append(config_obj_list[n].parameters[4])
        df = pd.DataFrame(data)
        
        return df 
    
    @staticmethod
    def getConfigData (config_elite):
        data = {'alpha': config_elite.parameters[0] ,'initial_temperature':config_elite.parameters[1], 'neighbourhood_operator':config_elite.parameters[2], 'num_iteration':config_elite.parameters[3], 'stopping_temperature':config_elite.parameters[4]}
        return data
    
    @staticmethod
    def generate_initial_solutions(num_sol, parameters_list):
        instance_list, instance_name = Instance.select_instances(Instance.num_total_instances)
        fitness_class_list = [Instance.create_fitness_obj(i) for i in instance_list]
        first_solution = [SAParameters.generate_random_solution(fitness_class_list[i][1]) for i in range(len(instance_list))]
        first_fitness = [fitness_class_list[i][0].generic_fitness(first_solution[i]) for i in range(len(instance_list))]
        sa_solutions_dict = {i: [] for i in instance_name}
        
        for i in range(len(instance_name)):
            sa_class = SimAneal(individual = first_solution[i],
                                fitness = first_fitness[i],
                                alpha = float(parameters_list[0]),
                                initial_temperature = float(parameters_list[1]),
                                neighbourhood_operator = str(parameters_list[2]),
                                num_iteration = int(parameters_list[3]),
                                stopping_temperature = float(parameters_list[4]))
            
            sa_fit, sa_solution = sa_class.calculate(fitness_class_list[i][0])
            sa_population = sa_solution
                                 
            for n in range(1,num_sol):
                sa_class.update_individual(sa_solution, fitness_class_list[i][0])
                sa_fit, sa_solution = sa_class.calculate(fitness_class_list[i][0])
                sa_population = np.vstack((sa_population,sa_solution))
            
            sa_solutions_dict[instance_name[i]] = sa_population
        
        return sa_solutions_dict
        
                