'''Import Modules'''
import math
import random
from functools import wraps
import time
from src.heuristics.game.operators.perm.mutation import PermMutation

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

    def __init__(self, individual, fitness, alpha=0.997, initial_temperature=10,
                 neighbourhood_operator=None, num_iteration=3,
                 stopping_temperature=1e-5, prob=0.2):

        self.alpha = alpha
        self.stopping_temperature = stopping_temperature
        self.initial_temperature = initial_temperature
        self.num_iteration = num_iteration
        self.prob = prob

        if neighbourhood_operator is None or neighbourhood_operator not in dir(PermMutation):
            self.neighbour_operator = getattr(PermMutation, "reverse")
            self.neighbour_operator_str = "neighbourhood_operator"
        else:
            self.neighbour_operator = getattr(PermMutation, str(neighbourhood_operator))
            self.neighbour_operator_str = neighbourhood_operator

        self.cur_solution = individual
        self.cur_fitness = fitness
        self.best_solution = individual
        self.best_fitness = fitness
        self._best_solutions = []

    def get_best_solutions(self):
        '''Get best solutions'''
        return self._best_solutions

    def update_individual(self, individual, fitness_class):
        '''Update current solition and fitness'''
        self.cur_solution = individual
        self.cur_fitness = fitness_class.calculate(self.cur_solution)

    def get_accept_factor(self, candidate_fitness, cur_temperature):
        '''Return a factor based on a candidate'''
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / cur_temperature)

    def check_acceptance(self, candidate, fitness_class, cur_temperature):
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
            if random.random() < self.get_accept_factor(candidate_fitness, cur_temperature):
                self.cur_fitness, self.cur_solution = candidate_fitness, candidate

    @results_sa
    def calculate(self, fitness_class):
        '''Iterative calls of the Simulated Anealling
           output: the best individual and fitness
        '''
        iter_temperature = 1
        cur_temperature = self.initial_temperature

        while cur_temperature >= self.stopping_temperature:
            while iter_temperature < self.num_iteration:

                candidate = self.neighbour_operator(list(self.cur_solution))
                self.check_acceptance(candidate, fitness_class, cur_temperature)
                iter_temperature += 1

            cur_temperature *= self.alpha
            iter_temperature = 1

        return self.best_fitness, self.best_solution
