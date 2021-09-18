""" Tests related to Pareto """
import os
import pytest

from src.heuristics.game import pareto
from tests.instance import Instance

GET_SOLUTIONS_FILES = [f for f in os.listdir('tests/pareto_tests/get_solutions/inputs')
                       if os.path.isfile(os.path.join('tests/pareto_tests/get_solutions/inputs', f))]

class TestClass(object):
    """
        Class with all tests for pareto
    """
    @staticmethod
    @pytest.mark.parametrize('instance', GET_SOLUTIONS_FILES)
    def test_get_solutions_fitness(instance):
        
        instance = Instance('tests/pareto_tests/get_solutions/',
                            instance)
        response_fitness, response_solutions = pareto.get_solutions(instance.input['Num_solutions'],
                                                                    instance.input['Fit_1'],
                                                                    instance.input['Fit_2'],
                                                                    instance.input['Solutions'])
        
        assert sorted(response_fitness) == sorted(tuple(instance.output['Response_fitness']))
        
    @staticmethod
    @pytest.mark.parametrize('instance', GET_SOLUTIONS_FILES)
    def test_get_solutions_solutions(instance):
        
        instance = Instance('tests/pareto_tests/get_solutions/',
                            instance)
        response_fitness, response_solutions = pareto.get_solutions(instance.input['Num_solutions'],
                                                                    instance.input['Fit_1'],
                                                                    instance.input['Fit_2'],
                                                                    instance.input['Solutions'])
        
        assert sorted(response_solutions) == sorted(instance.output['Response_solutions'])