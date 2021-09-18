""" Tests related to Mating """
import os
import pytest
import numpy as np

from src.heuristics.game.operators.general.mating import MatingSelection
from tests.instance import Instance

MATING_FILES = [f for f in os.listdir('tests/mating_tests/mating/inputs')
                       if os.path.isfile(os.path.join('tests/mating_tests/mating/inputs', f))]

class TestClass(object):
    """
        Class with all tests for mating selection
    """
    @staticmethod
    @pytest.mark.parametrize('instance', MATING_FILES)
    def test_roulette_wheel_len(instance):
        
        instance = Instance('tests/mating_tests/mating/',
                            instance)
        parent_1_vector, parent_2_vector = MatingSelection.roulette_wheel(np.array(instance.input['fitness']),
                                                                          instance.input['num_mating'],
                                                                          np.array(instance.input['random_vector']))
        
        assert len(parent_1_vector) == instance.input['num_mating']
        
    @staticmethod
    @pytest.mark.parametrize('instance', MATING_FILES)
    def test_roulette_wheel_range(instance):
        
        instance = Instance('tests/mating_tests/mating/',
                            instance)
        parent_1_vector, parent_2_vector = MatingSelection.roulette_wheel(np.array(instance.input['fitness']),
                                                                          instance.input['num_mating'],
                                                                          np.array(instance.input['random_vector']))
        
        assert (max(parent_1_vector) < len(instance.input['fitness']) and min(parent_1_vector) >= 0)
        
    @staticmethod
    @pytest.mark.parametrize('instance', MATING_FILES)
    def test_ranking_len(instance):
        
        instance = Instance('tests/mating_tests/mating/',
                            instance)
        parent_1_vector, parent_2_vector = MatingSelection.roulette_wheel(np.array(instance.input['fitness']),
                                                                          instance.input['num_mating'],
                                                                          np.array(instance.input['random_vector']))
        
        assert len(parent_1_vector) == instance.input['num_mating']
        
    @staticmethod
    @pytest.mark.parametrize('instance', MATING_FILES)
    def test_ranking_range(instance):
        
        instance = Instance('tests/mating_tests/mating/',
                            instance)
        parent_1_vector, parent_2_vector = MatingSelection.roulette_wheel(np.array(instance.input['fitness']),
                                                                          instance.input['num_mating'],
                                                                          np.array(instance.input['random_vector']))
        
        assert (max(parent_1_vector) < len(instance.input['fitness']) and min(parent_1_vector) >= 0)
        
    