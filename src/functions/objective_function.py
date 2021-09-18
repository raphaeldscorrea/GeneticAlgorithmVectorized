"""
ObjectiveFunction: customize for each model
Authors: Raphael Corrêa, Lara Cota, Anderson Tzitas, Gabriela Girundi

"""
from src.functions.decorators import check_fitness_type, convert_list
from functools import lru_cache
import numpy as np
import time

class ObjectiveFunction():
    """
    ObjectiveFunction class for Genetic Algorithm
    """
    def __init__(self, type_obj, **kwargs):
        self.type = type_obj
        self.current_generation = 0
        self.weigth_f1 = kwargs.get('weight_f1', 10)
        self.weight_f2 = kwargs.get('weight_f2', 10)
        self.weight_violation = kwargs.get('weight_violation', 999)

    @property
    def type(self):
        ''''
        Return type of objective function - mono or multi objective
        '''
        return self.__type

    @type.setter
    @check_fitness_type
    def type(self, var):
        self.__type = var

    @property
    def current_generation(self):
        ''''
        Generation control
        '''
        return self.__current_generation

    @current_generation.setter
    def current_generation(self, var):
        self.__current_generation = var

    @property
    def weigth_f1(self):
        ''''
        Get fitness 1 weigths for mono objective case
        '''
        return self.__weigth_f1

    @weigth_f1.setter
    def weigth_f1(self, var):
        self.__weigth_f1 = var

    @property
    def weigth_f2(self):
        ''''
        Get fitness 2 weigths for mono objective case
        '''
        return self.__weigth_f2

    @weigth_f2.setter
    def weigth_f2(self, var):
        self.__weigth_f2 = var

    @property
    def weight_violation(self):
        ''''
        Weight used for constraint violation
        '''
        return self.__weight_violation

    @weight_violation.setter
    def weight_violation(self, var):
        self.__weight_violation = var

    def increase_current_generation(self):
        """
        Update current generation
        """
        self.current_generation += 1

    @lru_cache(maxsize=None)
    def calculate(self, individual_tup):
        """
        Calculate objective function considering weights for two differente objectives.
        Params:
            individual = solution to be evaluated
        """
        time.sleep(0.01)
        individual = np.array(individual_tup)
        hours_delayed = (individual[0]+individual[1]+individual[4]+individual[3]-individual[5])
        setups = (individual[3]+individual[1]+individual[4]+individual[2]-individual[5])
        total_cost = hours_delayed*self.weigth_f1 + setups
        return -total_cost

    @lru_cache(maxsize=None)
    def calculate_f1(self, individual_tup):
        """
        Calculate objective function considering primor first objective
        Params:
            individual = solution to be evaluated
        """
        time.sleep(0.005)
        individual = np.array(individual_tup)
        hours_delayed = (individual[0]+individual[1]+individual[4]+individual[3]-individual[5])
        setups = (individual[3]+individual[1]+individual[4]+individual[2]-individual[5])
        total_cost = hours_delayed*self.weight_violation + setups
        return -total_cost

    @lru_cache(maxsize=None)
    def calculate_f2(self, individual_tup):
        """
        Calculate objective function considering primor second objective
        Params:
            individual = solution to be evaluated
        """
        time.sleep(0.005)
        individual = np.array(individual_tup)
        hours_delayed = (individual[0]+individual[1]+individual[4]+individual[3]-individual[5])
        setups = (individual[3]+individual[1]+individual[4]+individual[2]-individual[5])
        total_cost = hours_delayed + setups*self.weight_violation
        return -total_cost
