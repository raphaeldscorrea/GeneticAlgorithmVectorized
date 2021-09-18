'''Import Modules'''
import random
import math
import time
from functools import wraps

class SimAnneal():
    '''Simulated Annealing class'''
    
    def results_sa(method):
        @wraps(method)
        def wrapper(self, *method_args, **method_kwargs):
            print("Starting SA calculation.")
            start = time.process_time()
            result = method(self, *method_args, **method_kwargs)
            end = time.process_time() - start
            print("Best fitness: ", round(self.best_fitness))
            print("Current fitness: ", round(self.cur_fitness))
            print("SA: ", end)
            return result 
        return wrapper
    
    def results_aceptance(method):
        @wraps(method)
        def wrapper(self, *method_args, **method_kwargs):
            result = method(self, *method_args, **method_kwargs)
            print("Current temp: ", round(method_args[2],3))         
            print("Current fitness: ", round(self.cur_fitness))
            return result 
        return wrapper
    
    def __init__(self, individual, fitness, N=-1, temp=-1, alpha=0.995,
                 stopping_temperature=1e-8, stopping_iter=100000, prob=0.2):

        self.N = len(individual) if N == -1 else N
        self.temp = math.sqrt(self.N) if temp == -1 else temp
        self.alpha = alpha
        self.stopping_temperature = stopping_temperature
        self.stopping_iter = stopping_iter
        self.prob = prob
        self.cur_solution = individual
        self.cur_fitness = fitness
        self.best_solution = individual
        self.best_fitness = fitness
        self._best_solutions = []

    def get_best_solutions(self):
        ''' Return best solutions '''
        return self._best_solutions

    def update_individual(self, individual, fitness_class):
        '''Update current solition and fitness'''
        self.cur_solution = individual
        self.cur_fitness = fitness_class.calculate(self.cur_solution)

    def get_accept_factor(self, candidate_fitness):
        '''Return a factor based on a candidate'''
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.temp)

    def check_acceptance(self, candidate, fitness_class):
        '''
        Check if candidate will be accepted based on your fitness value and current fitness
        '''
        candidate_fitness = fitness_class.calculate(candidate)
        if candidate_fitness > self.cur_fitness:
            self.cur_fitness, self.cur_solution = candidate_fitness, candidate
            if candidate_fitness > self.best_fitness:
                self.best_fitness, self.best_solution = candidate_fitness, candidate
                self._best_solutions.append(candidate)
        else:
            if random.random() < self.get_accept_factor(candidate_fitness):
                self.cur_fitness, self.cur_solution = candidate_fitness, candidate

    @results_sa
    def calculate(self, fitness_class):
        '''Iterative calls of the Simulated Anealling
           output: the best individual and fitness
        '''
        iteration = 1
        self.temp = math.sqrt(self.N)

        while self.temp >= self.stopping_temperature and iteration < self.stopping_iter:
            candidate = list(self.cur_solution)
            j = random.randint(2, self.N - 1)
            i = random.randint(0, self.N - j)
            candidate[i : (i + j)] = reversed(candidate[i : (i + j)])
            self.check_acceptance(candidate, fitness_class)
            self.temp *= self.alpha
            iteration += 1

        return self.best_fitness, self.best_solution
