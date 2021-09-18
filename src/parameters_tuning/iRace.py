"""
I-Race is a method for offline configuration of parameterized algorithms
"""

import numpy as np
import pandas as pd
import logging
from math import log, ceil
from scipy.stats import friedmanchisquare
import scikit_posthocs as sp
import multiprocessing

from configuration import Configuration
from instanceGenerator import Instance
from gaParameters import MyPool

class Racing():
    
    def __init__(self, param_obj,
                 num_parameters,
                 num_experiments,
                 t_first = None,
                 t_each = None):
                
        # It depends on GA or SA parameters 
        self._param_obj = param_obj
        self._num_parameters = num_parameters 
        self._parameters_test_limit = param_obj.get_parameters_test_limit()
        
        # iRace Parameters
        # Number of instances that should be tested before the first statistical test
        if t_first is None:
            self._t_first = 6
        else :
            self._t_first = t_first
         
        # Number of instances that sould be tested between two statistical tests
        if t_each is None:
            self._t_each = 1
        else :
            self._t_each = t_each
        
        # Maximum number of races that will be executed in iRace
        self._num_races = 2 #TODO ceil(2 + log(self._num_parameters,2)) 
        
        # Number of instances that sould be tested between two statistical tests
        if num_experiments is None:
            self._num_experiments = 2000
        else :
            self._num_experiments = num_experiments
            
        self._budget = self._num_experiments/self._num_races
        self._budget_used = 0
                   
        # Number of initial candidate configurations to be chosen
        self._num_candidate_config = int(self._budget/(self._t_first+self._t_each*5))
        
        # Solution Size Parameters
        self._N_config_elite = 3
        
        # Statistical Test Parameters 
        self._p_value = 0.05
        self._min_measurements = 3
        
        # Solution Data
        self.result_data = [[] for n in range(self._num_races)]
        self.config_data = self._param_obj.createConfigData()
        self.elite_data = [[] for x in range(self._num_races)]
    
    def get_parameters_limit (self):
        parameters_limit = []    
        for i in range(len(self._parameters_test_limit)): 
            parameters_limit.append({'ConfigParameters': list(self._parameters_test_limit)[i],
                                     "NumExclusão": list(self._parameters_test_limit.values())[i]})
            
        return parameters_limit
    
    def get_config_data (self):
        return self.config_data.to_dict()
    
    def get_config_elite_data (self):
        config_elite_data = []    
        for i in range(len(self.elite_data)): 
            config_elite_data.append({'Race': i+1, "ConfigElite": self.elite_data[i]})
        
        return config_elite_data
    
    def get_racing_data (self):
        racing_data = []    
        for i in range(len(self.result_data)): 
            racing_data.append({'Race': i+1, "Data": self.result_data[i].to_dict()})
        
        return racing_data
          
#-----------------------------------------------------------------------------------#
# MAIN FUNCTION
#-----------------------------------------------------------------------------------#  
        
    def iterated_racing(self):
        
        # Parallel call
        pool = MyPool(multiprocessing.cpu_count())
        logging.info("Parallel mode active with " + str(multiprocessing.cpu_count())+ " cores.")
        
        logging.info(" -------- iRace General Parameters -----------")
        logging.info(" num experiments: " +  str(self._num_experiments))
        logging.info(" num races: " +  str(self._num_races))
        logging.info(" num initial config: " +  str(self._num_candidate_config))
        logging.info(" -------- Stopping Criteria -----------")
        logging.info(" race budget: " +  str(self._budget))
        logging.info(" num elite config: " +  str(self._N_config_elite))
        logging.info(" -------------------------------------")
        logging.info(" ... ")
                
        # Define finite set of initial candidate configurations
        it = 1
        logging.info(str(it) + " race parameters: ")
        param_distribution = self._param_obj.get_parameters_uniforme_distribution()
        config_list = self.sample_uniform (param_distribution)
        config_elite, solution_data = self.race (config_list, pool)
        self.result_data[0] = solution_data
        self.elite_data[0] = [id(config_elite[n]) for n in range(len(config_elite))]        
        
        while self._budget_used < self._num_experiments :
            logging.info(str(it) + "|" + str(self._budget_used) + "|" +  str(self._num_experiments))
            it += 1
            logging.info(str(it) + " race parameters: ")
            
            self._budget = (self._num_experiments-self._budget_used)/(self._num_races-it+1) 
            new_config_list = self.sample_updated(config_elite, it) # Generate new candidates
            config_elite, solution_data = self.race (new_config_list, pool) # Call race
            self.result_data[it-1] = solution_data
            self.elite_data[it-1] = [id(config_elite[n]) for n in range(len(config_elite))]
            
            if len(config_elite)==1:
                break
        pool.close()
        pool.join()
            
        return config_elite
        
#-----------------------------------------------------------------------------------#
# Sampling new configurations according to a particular distribution
#-----------------------------------------------------------------------------------#  
        
    def sample_uniform (self, param_distribution):
        config_list = []
        for i in range(self._num_candidate_config):
            #while True:
            param_list = [np.random.choice(x['values'], 1, x['prob'])[0] for x in param_distribution]    
                #if not any(x.parameters == param_list for x in config_list): 
                #    break
                
            config_list.append(Configuration(param_distribution, param_list) ) 
             
        return config_list               
  
#-----------------------------------------------------------------------------------#
# Updating the sampling distribution in order to bias the sampling towards the 
# best configurations.
#-----------------------------------------------------------------------------------#

    def sample_updated (self, elite_config_list, it):
        N_elite = len(elite_config_list) 
        
        # updating elite sampling distribution
        elite_config_list = Configuration.update_elite_probability (elite_config_list, it, self._num_races)
       
        # parent selection probability
        self._num_candidate_config = max(ceil(self._budget/(self._t_first+self._t_each*5)), self._min_measurements)
        new_candidates = self._num_candidate_config - N_elite
        
        list_parent_probability = [x.get_parent_probability(N_elite) for x in elite_config_list]
        list_parent_index = [np.random.choice( list(range(N_elite)), 1, list_parent_probability)[0] for i in range(new_candidates)]              
        
        new_config_list = elite_config_list        
        for i in range(new_candidates):
            param_distribution = elite_config_list[list_parent_index[i]].parameters_distribution
            
            #while True:
            param_list = [np.random.choice(x['values'], 1, x['prob'])[0] for x in param_distribution]
            #if not any(x.parameters == param_list for x in new_config_list):
                #    break
            #self._parameters_test_limit[tuple(param_list)]  
            new_config_list.append(Configuration(param_distribution, param_list) )            

        return new_config_list        
    
#-----------------------------------------------------------------------------------#
# Selecting the best configurations from the newly sampled ones by means of racing
#   @input : a finite set of candidate configurations.
#   @input  
#-----------------------------------------------------------------------------------#
    
    def race (self, config_list, pool):
        budget_used = 0
        logging.info(" budget available: " + str(self._budget))
        logging.info(" num candidates: " + str(self._num_candidate_config))               
        
        #########################################################################
        # Evaluate all initial candidates in t_first instances
        #########################################################################
        
        config_set = [[] for i in range(self._t_first)] 
        
        # Selecting instances
        instance_list, instance_name = Instance.select_instances(self._t_first)
        fitness_class_list = [Instance.create_fitness_obj(x) for x in instance_list]
        
        for i in range(self._t_first):
            solution_size = fitness_class_list[i][1]           
            fitness_class = fitness_class_list[i][0]

            parameters_list = []
            for n in range(self._num_candidate_config): 
                parameters_list.append((fitness_class, config_list[n].parameters, solution_size, instance_name[i]))
            
            for sa_fitness, sa_solution in pool.starmap(self._param_obj.call_optimization, parameters_list):
                config_set[i].append(sa_fitness)  
        

        data = np.array(config_set)
        
        # Solution info
        solution_df = pd.DataFrame(config_set)
        solution_df.columns = [id(config_list[n]) for n in range(self._num_candidate_config)]
        solution_df.index = instance_name
        
        new_df = self._param_obj.createConfigData(config_list)
        new_df.index = [id(config_list[n]) for n in range(self._num_candidate_config)]
        self.config_data = pd.concat([self.config_data, new_df]).drop_duplicates() 
            
        # Statistical Test - Friedman
        # Configurations that perform statistically worse than at least another one are discarded
        stat, p = friedmanchisquare(*data.T)
        
        if p <= self._p_value:
            # pairwise comparisons are performed between the best configuration and each other one
            index_best_config = Racing.get_rank(data)[0]
            
            # Post hoc conover
            matrix_post_hoc = sp.posthoc_conover_friedman(data)
            pairwise_comp = matrix_post_hoc[index_best_config]
            index_config_to_remove = np.where(abs(pairwise_comp)<= self._p_value)[0]
            
            for i in index_config_to_remove:
                self._parameters_test_limit[tuple(config_list[i].parameters)] += 1
                
            config_list = np.delete(config_list, index_config_to_remove)
            data = np.delete(data, index_config_to_remove, axis=1)
                  
        budget_used = self._t_first * self._num_candidate_config
       
        #########################################################################
        # Evaluate all initial candidates on a single instance            
        #########################################################################
        
        self._num_candidate_config = max(self._min_measurements, len(config_list))
        
        while budget_used <= self._budget :            
            config_set = [[] for i in range(self._t_each)] 
            
            # Selecting instances
            instance_list, instance_name = Instance.select_instances(self._t_each)
            fitness_class_list = [Instance.create_fitness_obj(x) for x in instance_list]                                   
            
            for i in range(self._t_each):
                solution_size = fitness_class_list[i][1]           
                fitness_class = fitness_class_list[i][0]

                parameters_list = []
                for n in range(self._num_candidate_config): 
                    parameters_list.append((fitness_class, config_list[n].parameters, solution_size, instance_name[i]))
            
                for sa_fitness, sa_solution in pool.starmap(self._param_obj.call_optimization, parameters_list):
                    config_set[i].append(sa_fitness)               
            
            data = np.concatenate((data,config_set ))
            
            # Solution Data
            new_df = pd.DataFrame(config_set)
            new_df.columns = [id(config_list[n]) for n in range(self._num_candidate_config)]
            new_df.index = instance_name                      
            solution_df = pd.concat([solution_df, new_df], axis=0, join='outer')
            
            new_df = self._param_obj.createConfigData(config_list)
            new_df.index = [id(config_list[n]) for n in range(self._num_candidate_config)]
            self.config_data = pd.concat([self.config_data, new_df]).drop_duplicates() 
            
            # Statistical Test - Friedman
            stat, p = friedmanchisquare(*data.T)
                
            if p < self._p_value:

                # pairwise comparisons are performed between the best configuration and each other one
                index_best_config = Racing.get_rank(data)[0]
                
                # Post hoc conover
                matrix_post_hoc = sp.posthoc_conover_friedman(data)
                pairwise_comp = matrix_post_hoc[index_best_config]                
                index_config_to_remove = np.where(abs(pairwise_comp)<= self._p_value)[0]                          
                
                for i in index_config_to_remove:
                    self._parameters_test_limit[tuple(config_list[i].parameters)] += 1
                
                config_list = np.delete(config_list, index_config_to_remove)
                data = np.delete(data, index_config_to_remove, axis=1)
            
            budget_used += (self._t_each * self._num_candidate_config)            
            self._num_candidate_config = max(self._min_measurements, len(config_list))
            
            logging.info(" num candidates:" + str(self._num_candidate_config))

            if len(config_list) <= self._N_config_elite:
                break
                   
        self._budget_used += budget_used
                
        # Ranking
        if len(config_list) < self._N_config_elite:
            index_elite_config = Racing.get_rank(data, len(config_list))      
        else:
            index_elite_config = Racing.get_rank(data, self._N_config_elite) 

        for i, n in enumerate(index_elite_config): config_list[n].set_rank(i)
        elite_config_list = [config_list[i] for i in index_elite_config]         

        return elite_config_list, solution_df
     
    @staticmethod
    def get_rank (data, n=1):
        rank_list = list(map(lambda x : x.argsort().argsort(), -data))            
        rank_sum_list = np.argsort(list(map(sum, np.array(rank_list).T)))[:n] 
        return rank_sum_list