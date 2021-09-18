# Genetic Algorithm More Efficient - GAME
# Vallourec Soluções Tubulares do Brasil

"""
Import Modules
"""
import multiprocessing
import numpy as np
import random
import logging
import time
from functools import wraps
from src.heuristics.simulated_annealing.simulated_annealing import SimAnneal
from src.heuristics.game.operators.binary.crossover import BinCrossover
from src.heuristics.game.operators.binary.mutation import BinMutation
from src.heuristics.game.operators.perm.crossover import PermCrossover
from src.heuristics.game.operators.perm.mutation import PermMutation
from src.heuristics.game.operators.general.mating import MatingSelection
from src.heuristics.game.operators.general.survivor import SurvivorSelection

class GA():
    '''GA class'''
    
    def results(method):
        @wraps(method)
        def wrapper(self, *method_args, **method_kwargs):
            start = time.process_time()
            result = method(self, *method_args, **method_kwargs)
            end = time.process_time() - start        
            print("Iteration: ", method_args[0])
            if self.fitness_class_type == 'mono':
                print("Best fitness: ", round(self._fitness_1.max()))
            else:
                print("Best fitness 1: ", round(self.get_best_fitness()[0]))
                print("Best fitness 2: ", round(self.get_best_fitness()[1]))
            print("Unique individuals: ", len(np.unique(self._population, axis=0)))
            print("GA time: ", end)
            return result 
        return wrapper
    
    def __init__(self, problem_type, fitness_class, pop_size, num_variables, *args, **kwargs):

        self.problem_type = problem_type
        self.fitness_class = fitness_class
        self.pop_size = pop_size+1 if pop_size % 2 > 0 else pop_size
        self.sol_size = num_variables
        self.num_generations = kwargs.get('max_iteration', 10)
        self.suggestion_solutions = kwargs.get('suggestion_solutions', None)
        self.force_unique = kwargs.get('force_unique', False)
        self.population_age = np.zeros(self.pop_size)
        self.run_limit = kwargs.get('run', 70)
        self.run_count = 0
        self.run_current_best_1 = 0
        self.run_current_best_2 = 0
        self.fitness_class_type = fitness_class.type

        # Population inicialization
        self._population = kwargs.get('population', self.generate_population())

        if fitness_class.type == 'multi':
            self._fitness_1, self._fitness_2 = self.calculate_fitness_multi()
        else:
            self._fitness_1 = self.calculate_fitness()

        # Parallel call
        self.parallel_call = kwargs.get('parallel_call', False)

        # Local Search
        self.ls_call = kwargs.get('ls_call', False)
        if self.ls_call:
            self.sa_obj = SimAnneal(self._population[0], self._fitness_1[0])
            self.upgrade_population()

        # Keep best solutions
        self.keep_best = kwargs.get('keep_best', False)
        if self.keep_best:
            self._best_solutions = self.get_best_individual()[0]
            self._best_fitness_list = []
            self._mean_fitness_list = []

        crossover_operator = kwargs.get('crossover_operator', None)
        mutation_operator = kwargs.get('mutation_operator', None)
        mating_operator = kwargs.get('mating_operator', None)
        survivor_operator = kwargs.get('survivor_operator', None)

        # Mutation Operator
        if self.problem_type == "perm":
            if mutation_operator is None or mutation_operator not in dir(PermMutation):
                self.mutation_operator = getattr(PermMutation, "displacement")
            else:
                self.mutation_operator = getattr(PermMutation, mutation_operator)

            if crossover_operator is None or crossover_operator not in dir(PermCrossover):
                self.crossover_operator = getattr(PermCrossover, "obx")
            else:
                self.crossover_operator = getattr(PermCrossover, crossover_operator)
        else:
            if mutation_operator is None or mutation_operator not in dir(BinMutation):
                self.mutation_operator = getattr(BinMutation, "bit_inversion")
            else:
                self.mutation_operator = getattr(BinMutation, mutation_operator)

            if crossover_operator is None or crossover_operator not in dir(BinCrossover):
                self.crossover_operator = getattr(BinCrossover, "single_point")
            else:
                self.crossover_operator = getattr(BinCrossover, crossover_operator)

        #Mating Operator
        if mating_operator is None or mating_operator not in dir(MatingSelection):
            self.mating_operator = getattr(MatingSelection, "roulette_wheel")
        else:
            self.mating_operator = getattr(MatingSelection, mating_operator)
        self.probability_array = np.random.uniform(0, 1, self.pop_size)

        # Survivor Operator
        if survivor_operator is None or survivor_operator not in dir(SurvivorSelection):
            self.survivor_operator = getattr(SurvivorSelection, "fitness_based")
        else:
            if fitness_class.type == 'mono' and survivor_operator == 'nsgaII':
                self.survivor_operator = getattr(SurvivorSelection, "fitness_based")
                logging.info('It is not possible call nsgaII survivor to mono objective problem')
            else:
                self.survivor_operator = getattr(SurvivorSelection, survivor_operator)

        self.perc_replacement = 0.1

        # Parameters
        self.prob_crossover = kwargs.get('prob_crossover', 0.8)
        self.prob_mutation = kwargs.get('prob_mutation', 0.1)
        self.prob_elitism = kwargs.get('prob_elitism', 0)

    def generate_population(self):
        '''Generate population'''
        population = np.zeros((self.pop_size, self.sol_size))
        if self.problem_type == "perm":
            for i in range(self.pop_size):
                population[i, :] = np.random.permutation(np.arange(population.shape[1]))[:population.shape[1]]

        else:
            for i in range(self.pop_size):
                population[i, :] = np.random.randint(0, 2, population.shape[1])[:population.shape[1]]
        population = population.astype(int)

        if self.suggestion_solutions is not None:
            population[:len(self.suggestion_solutions)] = self.suggestion_solutions

        return population
        
    def calculate_fitness (self):
        '''Mono objective fitness calculation'''
        pop_tuple = tuple(map(tuple, self._population))
        return (np.array([self.fitness_class.calculate_f1(tuple(x)) for x in pop_tuple]).reshape((self.pop_size,)))
    
    def calculate_fitness_multi (self):
        '''Multi objective fitness calculation'''
        pop_tuple = tuple(map(tuple, self._population))
        f1 = np.array(
            [self.fitness_class.calculate_f1(tuple(x)) for x in pop_tuple]
            ).reshape((self.pop_size,))
        f2 = np.array(
            [self.fitness_class.calculate_f2(tuple(x)) for x in pop_tuple]
            ).reshape((self.pop_size,))
        return f1,f2

    def upgrade_population(self):
        '''Upgrade population'''
        sa_result = self.local_search(self._population, self._fitness_1)
        sa_population = self.sa_obj.get_best_solutions()
        upgrade_size = min(len(sa_population), self.pop_size)
        self._population[-upgrade_size:] = np.array(sa_population[-upgrade_size:])

    def get_population(self):
        '''Return current population'''
        return self._population

    def get_fitness(self):
        '''Return fitness value'''
        if self.fitness_class.type == 'multi':
            return self._fitness_1, self._fitness_2
        else:
            return self._fitness_1

    def get_best_fitness(self):
        '''Return best fitness value'''
        if self.fitness_class.type == 'multi':
            return self._fitness_1.max(), self._fitness_2.max()
        else:
            return self._fitness_1.max()

    def get_best_individual(self):
        '''Return best individual'''
        index_best = np.where(self._fitness_1 == self._fitness_1.max())
        return self._population[index_best,]

    def get_best_solutions(self):
        '''Return a list of best solutions'''
        return self._best_solutions

    def get_best_fitness_list(self):
        '''Return a list of fitness values'''
        return self._best_fitness_list

    def get_mean_fitness_list(self):
        '''Get mean fitness list'''
        return self._mean_fitness_list

    def generations(self):
        '''Iterative calls of the Genetic Algorithm
           @output: the best individual and fitness
        '''
        if self.fitness_class.type == "multi":
            if self.parallel_call:
                pool = multiprocessing.Pool(multiprocessing.cpu_count() - 4)
                for i in range(self.num_generations):
                    run_candidate_1, run_candidate_2 = self.get_best_fitness()
                    if run_candidate_1 <= self.run_current_best_1 and run_candidate_2 <= self.run_current_best_2:
                        self.run_count += 1
                    else:
                        self.run_count = 0
                        self.run_current_best_1 = max(self.run_current_best_1, run_candidate_1)
                        self.run_current_best_2 = max(self.run_current_best_2, run_candidate_2)
                    if self.run_count > self.run_limit:
                        break
                    else:
                        self.fitness_class.increase_current_generation()
                        self.evaluation_multi(i, pool)
                pool.close()
                pool.join()
            else:
                for i in range(self.num_generations):
                    run_candidate_1, run_candidate_2 = self.get_best_fitness()
                    if run_candidate_1 <= self.run_current_best_1 and run_candidate_2 <= self.run_current_best_2:
                        self.run_count += 1
                    else:
                        self.run_count = 0
                        self.run_current_best_1 = max(self.run_current_best_1, run_candidate_1)
                        self.run_current_best_2 = max(self.run_current_best_2, run_candidate_2)
                    if self.run_count > self.run_limit:
                        break
                    else:
                        self.fitness_class.increase_current_generation()
                        self.evaluation_multi(i)
        else:
            if self.parallel_call:
                pool = multiprocessing.Pool(multiprocessing.cpu_count() - 4)
                for i in range(self.num_generations):
                    run_candidate = self.get_best_fitness()
                    if run_candidate <= self.run_current_best_1:
                        self.run_count += 1
                    else:
                        self.run_count = 0
                        self.run_current_best_1 = run_candidate
                    if self.run_count > self.run_limit:
                        break
                    else:
                        self.fitness_class.increase_current_generation()
                        self.evaluation(i, pool)
                pool.close()
                pool.join()
            else:
                for i in range(self.num_generations):
                    run_candidate = self.get_best_fitness()
                    if run_candidate <= self.run_current_best_1:
                        self.run_count += 1
                    else:
                        self.run_count = 0
                        self.run_current_best_1 = run_candidate
                    if self.run_count > self.run_limit:
                        break
                    else:
                        self.fitness_class.increase_current_generation()
                        self.evaluation(i)
                                        
# =============================================================================
#   Evaluation Process:
#    Step 1 : Generation of the offspring 
#    Step 2 : Fitness calculatin of the offspring
#    Step 3 : Calculation of the survivor population and its fitness        
# =============================================================================
    
    @results
    def evaluation(self, i, pool=None):   
        children = self.generate_offspring()
        children_tuple = tuple(map(tuple, children))
        
        if(self.parallel_call):
            fitness_children = np.array(
                [pool.map(self.fitness_class.calculate, children_tuple)]
                ).reshape((self.pop_size,))
        else:
            fitness_children = np.array(
                [self.fitness_class.calculate(tuple(x)) for x in children_tuple]
                ).reshape((self.pop_size,))  
                   
        if self.ls_call and (random.random() < self.sa_obj.prob):
            sa_1_fit, sa_1_sol, sa_2_fit, sa_2_sol = self.local_search(children, fitness_children)
            new_generation, new_fitness, new_age = self.survivor_operator(self._population,
                                                                          children,
                                                                          self._fitness_1,
                                                                          fitness_children,
                                                                          self.population_age,
                                                                          self.perc_replacement,
                                                                          force_unique=self.force_unique,
                                                                          sa_1_fit=sa_1_fit,
                                                                          sa_1_sol=sa_1_sol,
                                                                          sa_2_fit=sa_2_fit,
                                                                          sa_2_sol=sa_2_sol)
        else:
            new_generation, new_fitness, new_age = self.survivor_operator(self._population, children,
                                                                          self._fitness_1,
                                                                          fitness_children,
                                                                          self.population_age,
                                                                          self.perc_replacement,
                                                                          force_unique=self.force_unique)

        self.population_age = np.add(new_age, 1)
        self._population = new_generation
        self._fitness_1 = new_fitness

        if self.keep_best:
            self._best_solutions = np.vstack((self._best_solutions, self.get_best_individual()[0]))
            self._best_fitness_list.append(self.get_best_fitness())
            self._mean_fitness_list.append(sum(new_fitness) / len(new_fitness))
        #print(self.get_best_fitness())
            
    def parallel_f1(self, children):
        children_tuple = tuple(map(tuple, children))
        result = list(map(self.fitness_class.calculate_f1, children_tuple))
        return result
        
    def parallel_f2(self, children):
        children_tuple = tuple(map(tuple, children))
        result = list(map(self.fitness_class.calculate_f2, children_tuple))
        return result
    
    def chunkIt(self,seq, num):
            avg = len(seq) / float(num)
            out = []
            last = 0.0

            while last < len(seq):
                out.append(seq[int(last):int(last + avg)])
                last += avg

            return out
            
    @results
    def evaluation_multi(self, i, pool=None):
        '''Evaluation Process:
                1- Generation of the offspring
                2- Fitness calculatin of the offspring
                3- Calculation of the survivor population and its fitness
        '''
        
        children = self.generate_offspring()
        children_to_parallel = self.chunkIt(children, multiprocessing.cpu_count())
        children_tuple = tuple(map(tuple, children))
                
        if(self.parallel_call):
            #start = time.time()
            fitness_children_1_per_chunk = pool.map(self.parallel_f1, children_to_parallel)
            fitness_children_1 = np.array([val for sublist in fitness_children_1_per_chunk for val in sublist])
            fitness_children_2_per_chunk = pool.map(self.parallel_f2, children_to_parallel)
            fitness_children_2 = np.array([val for sublist in fitness_children_2_per_chunk for val in sublist])
            #end = time.time()
            #total_time = end-start
            #print("time",total_time)
            
        else:
            #start = time.time()
            fitness_children_1 = np.array([self.fitness_class.calculate_f1(tuple(x)) for x in children_tuple]).reshape((self.pop_size,))
            fitness_children_2 = np.array([self.fitness_class.calculate_f2(tuple(x)) for x in children_tuple]).reshape((self.pop_size,))
            #end = time.time()
            #total_time = end-start
            #print("time",total_time)
            
        fitness_children = []
        for i, j in zip(fitness_children_1, fitness_children_2):
            fitness_children.append([i, j])

        fitness_parents = []
        for i,j in zip(self._fitness_1,self._fitness_2):
            fitness_parents.append([i,j])
        
        #start = time.time()
        new_generation, new_fitness, new_age = self.survivor_operator(self._population,
                                                                      children,
                                                                      fitness_parents,
                                                                      fitness_children,
                                                                      self.population_age,
                                                                      self.perc_replacement)
        #end = time.time()
        #total_time = end-start
        #print("time",total_time)
        self.population_age = np.add(new_age, 1)
        self._population = new_generation
        self._fitness_1 = new_fitness[:,0]
        self._fitness_2 = new_fitness[:,1]
        
        #print(max(self._fitness_1),max(self._fitness_2))
    
        if self.keep_best:
            self._best_solutions = np.vstack((self._best_solutions,
                                              self.get_best_individual()[0]))

    def generate_offspring(self):
        '''
        Generation of the offspring:
            1- Parent selection
            2- Crossover
            3- Mutation
        '''
        parent_1, parent_2 = self.mating_operator(self._fitness_1,
                                                  self.pop_size,
                                                  self.probability_array)
        prob_crossover_vector = np.full((self.pop_size,), self.prob_crossover)
        children = np.array(
            [self.get_children(x,y,z) for x,y,z in zip(parent_1, parent_2, prob_crossover_vector)]
            ).reshape((self.pop_size, self.sol_size))
        
        prob_mutation_vector = np.full((self.pop_size,),self.prob_mutation)
        children_mutated = np.array(
            [self.get_children_mutated(x,y) for x,y in zip(children, prob_mutation_vector)]
            ).reshape((self.pop_size, self.sol_size))

        return children_mutated
    
    def get_children(self, p1, p2, pc):
        '''
        Get children
        '''
        random_value = np.random.uniform(0,1,1)
        if random_value <= pc:
            ch1, ch2 = self.crossover_operator(self._population[p1,],
                                               self._population[p2,])
            return ch1, ch2
        else:
            return self._population[p1,], self._population[p2,]
        
    def get_children_mutated(self, individual, pm):
        random_value = np.random.uniform(0,1,1)
        if random_value <= pm:
            ch1 = self.mutation_operator(individual)
            return ch1
        else:
            return individual

# =============================================================================
#   Call Local Search - Simulated Annealing    
# =============================================================================
    
    def local_search (self, children, fitness_children):
        '''
        Call Local Search - Simmulated Annealing
        '''
        first_parent = np.array(
            sorted(range(self.pop_size),key= self._fitness_1.__getitem__, reverse = True)
            )
        first_child = np.array(
            sorted(range(self.pop_size), key=fitness_children.__getitem__, reverse = True)
            )
            
        self.sa_obj.update_individual(self._population[first_parent[0]],
                                      self.fitness_class)
        sa_1_fit, sa_1_sol = self.sa_obj.calculate(self.fitness_class)
        self.sa_obj.update_individual(children[first_child[0]],
                                      self.fitness_class)
        sa_2_fit, sa_2_sol = self.sa_obj.calculate(self.fitness_class)

        return sa_1_fit, sa_1_sol, sa_2_fit, sa_2_sol

    def set_crossover_operator(self, operator_name):
        '''
        Setting crossover operator
        '''
        if not isinstance(operator_name,str):
            logging.error("Operator name must be a string.")

        if self.problem_type == "perm":
            if operator_name not in dir(PermCrossover):
                logging.error(operator_name + "does not exist in PermCrossover class.")
            else:
                self.crossover_operator = getattr(PermCrossover, operator_name)
        else:
            if operator_name not in dir(BinCrossover):
                logging.error(operator_name + "does not exist in BinCrossover class.")
            else:
                self.crossover_operator = getattr(BinCrossover, operator_name)

    def set_mutation_operator(self, operator_name):
        '''
        Setting mutation operator
        '''
        if not isinstance(operator_name,str):
            logging.error("Operator name must be a string.")

        if self.problem_type == "perm":
            if operator_name not in dir(PermMutation):
                logging.error(operator_name + "does not exist in PermMutation class.")
            else:
                self.mutation_operator = getattr(PermMutation, operator_name)
        else:
            if operator_name not in dir(BinMutation):
                logging.error(operator_name + "does not exist in BinMutation class.")
            else:
                self.mutation_operator = getattr(BinMutation, operator_name)

    def set_mating_operator(self, operator_name):
        '''
        Setting mating operator
        '''
        if not isinstance(operator_name,str):
            logging.error("Operator name must be a string.")
        elif operator_name not in dir(MatingSelection):
            logging.error(operator_name + "does not exist in MatingSelection class.")
        else:
            self.mating_operator = getattr(MatingSelection, operator_name)

    def set_survivor_operator(self, operator_name, perc_replacement=0.1):
        '''
        Setting survivor operator
        '''
        if not isinstance(operator_name,str):
            logging.error("Operator name must be a string.")
        elif operator_name not in dir(SurvivorSelection):
            logging.error(operator_name + "does not exist in SurvivorSelection class.")
        else:
            self.survivor_operator = getattr(SurvivorSelection, operator_name)
            self.perc_replacement = perc_replacement
