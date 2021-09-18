""" Tests related to Perm Crossover """
import os
import pytest
import numpy as np

from src.heuristics.game.operators.perm.crossover import PermCrossover
from tests.instance import Instance

CROSSOVER_FILES = [f for f in os.listdir('tests/crossover_tests/crossover/inputs')
                       if os.path.isfile(os.path.join('tests/crossover_tests/crossover/inputs', f))]

class TestClass(object):
    """
        Class with all tests for permutation crossover
    """
    @staticmethod
    @pytest.mark.parametrize('instance', CROSSOVER_FILES)
    def test_ox_len(instance):
        
        instance = Instance('tests/crossover_tests/crossover/',
                            instance)
        child_1, child_2 = PermCrossover.ox(np.array(instance.input['Parent_1']),
                                            np.array(instance.input['Parent_2']))
        
        assert len(child_1) == len(instance.input['Parent_1'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', CROSSOVER_FILES)
    def test_ox_duplicates(instance):
        
        instance = Instance('tests/crossover_tests/crossover/',
                            instance)
        child_1, child_2 = PermCrossover.ox(np.array(instance.input['Parent_1']),
                                            np.array(instance.input['Parent_2']))
        
        assert len(child_1) == len(set(child_1))
        
    @staticmethod
    @pytest.mark.parametrize('instance', CROSSOVER_FILES)
    def test_ox_2_len(instance):
        
        instance = Instance('tests/crossover_tests/crossover/',
                            instance)
        child_1, child_2 = PermCrossover.ox_2(np.array(instance.input['Parent_1']),
                                              np.array(instance.input['Parent_2']))
        
        assert len(child_1) == len(instance.input['Parent_1'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', CROSSOVER_FILES)
    def test_ox_2_duplicates(instance):
        
        instance = Instance('tests/crossover_tests/crossover/',
                            instance)
        child_1, child_2 = PermCrossover.ox_2(np.array(instance.input['Parent_1']),
                                              np.array(instance.input['Parent_2']))
        
        assert len(child_1) == len(set(child_1))
        
    @staticmethod
    @pytest.mark.parametrize('instance', CROSSOVER_FILES)
    def test_obx_len(instance):
        
        instance = Instance('tests/crossover_tests/crossover/',
                            instance)
        child_1, child_2 = PermCrossover.obx(np.array(instance.input['Parent_1']),
                                             np.array(instance.input['Parent_2']))
        
        assert len(child_1) == len(instance.input['Parent_1'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', CROSSOVER_FILES)
    def test_obx_duplicates(instance):
        
        instance = Instance('tests/crossover_tests/crossover/',
                            instance)
        child_1, child_2 = PermCrossover.obx(np.array(instance.input['Parent_1']),
                                             np.array(instance.input['Parent_2']))
        
        assert len(child_1) == len(set(child_1))
        
    @staticmethod
    @pytest.mark.parametrize('instance', CROSSOVER_FILES)
    def test_pmx_len(instance):
        
        instance = Instance('tests/crossover_tests/crossover/',
                            instance)
        child_1, child_2 = PermCrossover.pmx(np.array(instance.input['Parent_1']),
                                             np.array(instance.input['Parent_2']))
        
        assert len(child_1) == len(instance.input['Parent_1'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', CROSSOVER_FILES)
    def test_pmx_duplicates(instance):
        
        instance = Instance('tests/crossover_tests/crossover/',
                            instance)
        child_1, child_2 = PermCrossover.pmx(np.array(instance.input['Parent_1']),
                                             np.array(instance.input['Parent_2']))
        
        assert len(child_1) == len(set(child_1))

    @staticmethod
    @pytest.mark.parametrize('instance', CROSSOVER_FILES)
    def test_pmx_2_len(instance):
        
        instance = Instance('tests/crossover_tests/crossover/',
                            instance)
        child_1, child_2 = PermCrossover.pmx_2(np.array(instance.input['Parent_1']),
                                               np.array(instance.input['Parent_2']))
        
        assert len(child_1) == len(instance.input['Parent_1'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', CROSSOVER_FILES)
    def test_pmx_2_duplicates(instance):
        
        instance = Instance('tests/crossover_tests/crossover/',
                            instance)
        child_1, child_2 = PermCrossover.pmx_2(np.array(instance.input['Parent_1']),
                                               np.array(instance.input['Parent_2']))
        
        assert len(child_1) == len(set(child_1))
        
    @staticmethod
    @pytest.mark.parametrize('instance', CROSSOVER_FILES)
    def test_cycle_len(instance):
        
        instance = Instance('tests/crossover_tests/crossover/',
                            instance)
        child_1, child_2 = PermCrossover.cycle(np.array(instance.input['Parent_1']),
                                               np.array(instance.input['Parent_2']))
        
        assert len(child_1) == len(instance.input['Parent_1'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', CROSSOVER_FILES)
    def test_cycle_duplicates(instance):
        
        instance = Instance('tests/crossover_tests/crossover/',
                            instance)
        child_1, child_2 = PermCrossover.cycle(np.array(instance.input['Parent_1']),
                                               np.array(instance.input['Parent_2']))
        
        assert len(child_1) == len(set(child_1))



