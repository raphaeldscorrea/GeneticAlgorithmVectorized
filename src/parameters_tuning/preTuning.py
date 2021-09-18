# -*- coding: utf-8 -*-

import sys
import os

from instanceGenerator import Instance

from src.heuristics.game.ga import GA

'''
' Generate smaller ranges of possibilities for each GA parameter
'''
class PreTuning():
    
    def __init__(self, ga_parameters_obj, num_instances=1, num_repetitions=1):
        
        self.num_instances = num_instances
        self.num_repetitions = num_repetitions
        self.instances = Instance.select_instances(self.num_instances)
        self.ga_param = ga_parameters_obj  
    
    # Categorical Parameters
    def generating_operators_vector (self):
        
        # Determine a minimum fitness level by running GA for 150 iterations with default values
        fitness_class, num_variables = Instance.create_fitness_obj(self.instances[0])
        ga_class = GA("perm", 
                      fitness_class, 
                      self.ga_param.pop_size_default, 
                      num_variables, 
                      max_iteration=2,
                      crossover_operator = self.ga_param.crossover_op_default, 
                      mutation_operator = self.ga_param.mutation_op_default,
                      mating_operator = self.ga_param.mating_op_default, 
                      survivor_operator = self.ga_param.survivor_op_default,
                      prob_crossover = self.ga_param.crossover_prob_default, 
                      prob_mutation = self.ga_param.mutation_prob_default,
                      keep_best = True,
                      parallel_call = True,
                      ls_call=True)

        ga_class.generations()        
        min_fitness_level = ga_class.get_best_fitness()
        
        solution_list = []
        for i in range(self.num_instances): # For each input
            fitness_class, num_variables = Instance.create_fitness_obj(self.instances[i])
            # For each categorical parameter configuration
            for cross_op in self.ga_param.crossover_operators:
                for mut_op in self.ga_param.mutation_operators:
                    for mat_op in self.ga_param.mating_operators:
                        for rep in range(self.num_repetitions): # Number of GA repetitions for each parameter configuration
                            solution_info = {}
                            solution_info['instance_ref'] = i
                            solution_info['crossover_operator'] = cross_op
                            solution_info['mutation_operator'] = mut_op
                            solution_info['mating_operator'] = mat_op
                            solution_info['rep'] = rep
                            
                            # Numerical parameters are set as default values
                            ga_class = GA("perm", 
                                          fitness_class, 
                                          self.ga_param.pop_size_default, 
                                          num_variables, 
                                          max_iteration=10,
                                          crossover_operator = cross_op, 
                                          mutation_operator = mut_op,
                                          mating_operator = mat_op, 
                                          survivor_operator = self.ga_param.survivor_op_default,
                                          prob_crossover = self.ga_param.crossover_prob_default, 
                                          prob_mutation = self.ga_param.mutation_prob_default,
                                          keep_best = True,
                                          parallel_call = True,
                                          ls_call=True)
                            
                            ga_class.generations() 
                            
                            # 1) Save the best objective function
                            solution_info['best_fo'] = ga_class.get_best_fitness()
                            
                            # 2) Save the iteration that reached the first solution that was better than or equal to min_fitness_level
                            best_fitness_list = ga_class.get_best_fitness_list()
                            closest_fo_list = list(map(lambda x: x >= min_fitness_level, best_fitness_list))
                            solution_info['it_min_fitness_level'] = (closest_fo_list.index(True) if True in closest_fo_list else 0)
                            #solution_info['it_min_fitness_level'] = best_fitness_list.index(closest_fo)
                            
                            # 3) Save the iteration that first achieved best_fo
                            solution_info['it_best_fo'] = best_fitness_list.index(max(best_fitness_list))
                            
                            solution_list.append(solution_info)
                            
            solution_analysis = {}
            solution_analysis['Solution_Analysis'] = solution_list
            
            return solution_analysis

    # Operators Rate Parameters        
    def generating_rate_vector ():
        #     1- Fixa Valores: Tamanho de População, Num Iteração
        # 2- Seleciona M melhores parâmetros categóricos
        # 3- Roda n vezes as possibilidades de Probabilidade de Crossover e Mutação.
    
        return None
    
    # Pop Size Parameter
    def generating_pop_size_vector ():
        # 1 - Fixa Valores: Num Iteração
        # 2 - Seleciona M melhores parâmetros categóricos
        # 3- Seleciona M melhores parâmetros de probabilidade 
        # 4 - Roda n vezes as possibilidades de tamanho da população.
        return None
