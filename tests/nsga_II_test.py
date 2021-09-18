""" Tests related to Pareto """
import os
import pytest

from src.heuristics.game import nsga_II
from tests.instance import Instance

GET_SOLUTIONS_FILES = [f for f in os.listdir('tests/nsga_II_tests/non_dominated_sorting/inputs')
                       if os.path.isfile(os.path.join('tests/nsga_II_tests/non_dominated_sorting/inputs', f))]

class TestClass(object):
    """
        Class with all tests for nsga_II
    """
    @staticmethod
    @pytest.mark.parametrize('instance', GET_SOLUTIONS_FILES)
    def test_get_solutions_fitness(instance):
        
        instance = Instance('tests/nsga_II_tests/non_dominated_sorting/',
                            instance)
        frontier = nsga_II.non_dominated_sorting(instance.input['Fitness'])
        
        assert frontier == instance.output['Frontier']