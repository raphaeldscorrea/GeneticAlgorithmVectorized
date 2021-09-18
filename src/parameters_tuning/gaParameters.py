# -*- coding: utf-8 -*-
"""

"""

import time
import sys
import os
import pandas as pd
import itertools
from saParameters import SAParameters
from math import ceil

from src.heuristics.game.ga import GA

import multiprocessing 
import multiprocessing.pool

class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)
    
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess

class GAParameters():
    
    def __init__(self):
        
        # Parameters Vectores     
        # self.mutation_operators = ["swap", "insert", "scramble", "inversion", "displacement"]
        # self.crossover_operators = ["pmx", "ox", "ox_2", "obx", "cycle"]
        # self.mating_operators = ["roulette_wheel", "ranking"]
        self.crossover_operators = ["ox"] 
        self.mutation_operators = ["scramble", "displacement"]
        self.mating_operators = ["roulette_wheel"]
        self.survivor_operators = ["fitness_based"] #
        
        # self.crossover_prob = [0.7, 0.75, 0.8, 0.85, 0.9]
        # self.mutation_prob = [0.20, 0.15, 0.10, 0.05]
        # self.population_size = [200, 280, 360, 440, 520, 600]
        
        self.crossover_prob = [0.85, 0.9]
        self.mutation_prob = [0.10] #, 0.05]
        self.population_size = [200] #, 280]
        
        # Default Values
        self.pop_size_default = 700
        self.mutation_prob_default = 0.1
        self.crossover_prob_default = 0.8
        self.survivor_op_default = "fitness_based"
        self.mating_op_default = "roulette_wheel"
        self.crossover_op_default = "obx"
        self.mutation_op_default = "displacement"
        
        # SA Default Values
        self._neighbourhood_operator_default = "reverse"
        self._initial_temperature_default = 10
        self._alpha_default = 0.997
        self._num_iteration_default = 5
        self._stopping_temperature_default = 1e-5
        
        sa_parameters_list = self.get_sa_parameters_list_default()
        self.rate = 0.005
        #self.sa_initial_solutions = SAParameters.generate_initial_solutions(ceil(max(self.population_size)*self.rate), sa_parameters_list)
#-----------------------------------------------------------------------------------#    
# Each parameter has associated a sampling distribution (discrete)
#-----------------------------------------------------------------------------------#
        
    def get_parameters_uniforme_distribution (self):
        parameters_list = [{"values":self.crossover_operators, "prob":[(1/len(self.crossover_operators))]*len(self.crossover_operators)},
                          {"values":self.crossover_prob, "prob":[(1/len(self.crossover_prob))]*len(self.crossover_prob)},
                          {"values":self.mating_operators, "prob":[(1/len(self.mating_operators))]*len(self.mating_operators)},
                          {"values":self.mutation_operators, "prob":[(1/len(self.mutation_operators))]*len(self.mutation_operators)},                        
                          {"values":self.mutation_prob, "prob":[(1/len(self.mutation_prob))]*len(self.mutation_prob)},
                          {"values":self.population_size, "prob":[(1/len(self.population_size))]*len(self.population_size)},
                          {"values":self.survivor_operators, "prob":[(1/len(self.survivor_operators))]*len(self.survivor_operators)}]
        
        return parameters_list
    
    def get_parameters_test_limit (self):
        parameters_configurations = list(itertools.product(self.crossover_operators,self.crossover_prob,self.mating_operators,self.mutation_operators,self.mutation_prob,self.population_size,self.survivor_operators))
        parameters_test_limit = {x: 0 for x in parameters_configurations}
        
        return parameters_test_limit
    
        
    def parallel_call (self, fitness_class, parameters_list, solution_size, instance):
       ga_fitness, ga_solution = self.call_optimization(fitness_class, parameters_list, solution_size, instance)
       return (ga_fitness, ga_solution)

    def call_optimization (self, fitness_class, parameters_list, solution_size, instance):  
        #first_solution = self.sa_initial_solutions[instance][:int(parameters_list[5]*self.rate)]
        ga_class = GA("perm", 
                      fitness_class, 
                      #suggestion_solutions = first_solution,
                      pop_size = int(parameters_list[5]), 
                      num_variables = solution_size, 
                      max_iteration = 200,
                      crossover_operator = str(parameters_list[0]), 
                      mutation_operator = str(parameters_list[3]),
                      mating_operator = str(parameters_list[2]), 
                      survivor_operator = str(parameters_list[6]),
                      prob_crossover = float(parameters_list[1]), 
                      prob_mutation = float(parameters_list[4]),
                      keep_best = True,
                      parallel_call = True,
                      ls_call = True)
        
        start = time.time()
        ga_class.generations()      
        ga_fitness = ga_class.get_best_fitness()
        ga_solution = ga_class.get_best_individual()
        end = time.time()
        
        return ga_fitness, ga_solution
    
    @staticmethod
    def createConfigData (config_obj_list=None):
        data = {}
        data['crossover_operators'] = []
        data['crossover_prob'] = []
        data['mating_operators'] = []
        data['mutation_operators'] = []
        data['mutation_prob'] =[]
        data['population_size'] =[]
        data['survivor_operators'] =[]
        
        if config_obj_list is not None:
            for n in range(len(config_obj_list)):
                data['crossover_operators'].append(config_obj_list[n].parameters[0])
                data['crossover_prob'].append(config_obj_list[n].parameters[1])
                data['mating_operators'].append(str(config_obj_list[n].parameters[2]))
                data['mutation_operators'].append(config_obj_list[n].parameters[3])
                data['mutation_prob'].append(config_obj_list[n].parameters[4])
                data['population_size'].append(config_obj_list[n].parameters[5])
                data['survivor_operators'].append(config_obj_list[n].parameters[6])
        df = pd.DataFrame(data)
 
        return df 
    
    @staticmethod
    def getConfigData (config_elite):
        data = {'crossover_operators': config_elite.parameters[0] ,
                'crossover_prob':config_elite.parameters[1], 
                'mating_operators':config_elite.parameters[2], 
                'mutation_operators':config_elite.parameters[3], 
                'mutation_prob':config_elite.parameters[4], 
                'population_size':config_elite.parameters[5], 
                'survivor_operators':config_elite.parameters[6]}
        
        return data
    
    def get_sa_parameters_list_default(self):
        return [self._alpha_default,self._initial_temperature_default,self._neighbourhood_operator_default,self._num_iteration_default,self._stopping_temperature_default]
    

