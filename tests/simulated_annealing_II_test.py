""" Tests related to Simulated Annealing II """
import os
import pytest
import numpy as np

from src.heuristics.simulated_annealing.simulated_annealing_II import SimAnneal
from src.functions.objective_function import ObjectiveFunction
from tests.instance import Instance

CALCULATE_FILES = [f for f in os.listdir('tests/simulated_annealing_II_tests/calculate/inputs')
                       if os.path.isfile(os.path.join('tests/simulated_annealing_II_tests/calculate/inputs', f))]

SOL_SIZE = 10
OBJECTIVE_WEIGHT = np.random.randint(5, size=(SOL_SIZE, SOL_SIZE))
TYPE_OBJ = 'multi'

class TestClass(object):
    """
        Class with all tests for Simulated Annealing II
    """
    @staticmethod
    @pytest.mark.parametrize('instance', CALCULATE_FILES)
    def test_calculate_fitness_value(instance):
        
        instance = Instance('tests/simulated_annealing_II_tests/calculate/',
                            instance)
        sim_anneal_obj = SimAnneal(instance.input['Individual'],
                                   instance.input['Fitness'])
        fitness_class_obj = ObjectiveFunction(TYPE_OBJ,
                                              weigths=OBJECTIVE_WEIGHT)
        
        fitness, solution = sim_anneal_obj.calculate(fitness_class_obj)
        
        assert fitness > 0
        
    @staticmethod
    @pytest.mark.parametrize('instance', CALCULATE_FILES)
    def test_calculate_solution_len(instance):
        
        instance = Instance('tests/simulated_annealing_II_tests/calculate/',
                            instance)
        sim_anneal_obj = SimAnneal(instance.input['Individual'],
                                   instance.input['Fitness'])
        fitness_class_obj = ObjectiveFunction(TYPE_OBJ,
                                              weigths=OBJECTIVE_WEIGHT)
        
        fitness, solution = sim_anneal_obj.calculate(fitness_class_obj)
        
        assert len(solution) == len(instance.input['Individual'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', CALCULATE_FILES)
    def test_calculate_solution_duplicates(instance):
        
        instance = Instance('tests/simulated_annealing_II_tests/calculate/',
                            instance)
        sim_anneal_obj = SimAnneal(instance.input['Individual'],
                                   instance.input['Fitness'])
        fitness_class_obj = ObjectiveFunction(TYPE_OBJ,
                                              weigths=OBJECTIVE_WEIGHT)
        
        fitness, solution = sim_anneal_obj.calculate(fitness_class_obj)
        
        assert len(solution) == len(set(solution))