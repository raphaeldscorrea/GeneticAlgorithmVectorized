""" Tests related to Survivor """
import os
import pytest
import numpy as np

from src.heuristics.game.operators.general.survivor import SurvivorSelection
from tests.instance import Instance

FITNESS_BASED_FILES = [f for f in os.listdir('tests/survivor_tests/fitness_based/inputs')
                       if os.path.isfile(os.path.join('tests/survivor_tests/fitness_based/inputs', f))]

AGE_BASED_FILES = [f for f in os.listdir('tests/survivor_tests/age_based/inputs')
                       if os.path.isfile(os.path.join('tests/survivor_tests/age_based/inputs', f))]

NSGAII_FILES = [f for f in os.listdir('tests/survivor_tests/nsgaII/inputs')
                       if os.path.isfile(os.path.join('tests/survivor_tests/nsgaII/inputs', f))]

class TestClass(object):
    """
        Class with all tests for survivor selection
    """
    @staticmethod
    @pytest.mark.parametrize('instance', FITNESS_BASED_FILES)
    def test_fitness_based_new_gen(instance):
        
        instance = Instance('tests/survivor_tests/fitness_based/',
                            instance)
        new_gen, fitness_new_gen, i = SurvivorSelection.fitness_based(instance.input['Parents'],
                                                                     instance.input['Children'],
                                                                     instance.input['Fitness_parents'],
                                                                     instance.input['Fitness_children'])
        
        assert new_gen.tolist() == instance.output['New_gen']
        
    @staticmethod
    @pytest.mark.parametrize('instance', FITNESS_BASED_FILES)
    def test_fitness_based_fitness_new_gen(instance):
        
        instance = Instance('tests/survivor_tests/fitness_based/',
                            instance)
        new_gen, fitness_new_gen, i = SurvivorSelection.fitness_based(instance.input['Parents'],
                                                                     instance.input['Children'],
                                                                     instance.input['Fitness_parents'],
                                                                     instance.input['Fitness_children'])
        
        assert fitness_new_gen.tolist() == instance.output['Fitness_new_gen']
        
    @staticmethod
    @pytest.mark.parametrize('instance', AGE_BASED_FILES)
    def test_age_based_new_gen(instance):
        
        instance = Instance('tests/survivor_tests/age_based/',
                            instance)
        new_gen, fitness_new_gen, age_new_gen = SurvivorSelection.age_based(np.array(instance.input['Parents']),
                                                                  np.array(instance.input['Children']),
                                                                  np.array(instance.input['Fitness_parents']),
                                                                  np.array(instance.input['Fitness_children']),
                                                                  np.array(instance.input['Pop_age']),
                                                                  instance.input['Perc_replace'])
        
        assert new_gen.tolist() == instance.output['New_gen']
        
    @staticmethod
    @pytest.mark.parametrize('instance', AGE_BASED_FILES)
    def test_age_based_fitness_new_gen(instance):
        
        instance = Instance('tests/survivor_tests/age_based/',
                            instance)
        new_gen, fitness_new_gen, age_new_gen = SurvivorSelection.age_based(np.array(instance.input['Parents']),
                                                                  np.array(instance.input['Children']),
                                                                  np.array(instance.input['Fitness_parents']),
                                                                  np.array(instance.input['Fitness_children']),
                                                                  np.array(instance.input['Pop_age']),
                                                                  instance.input['Perc_replace'])
        
        assert fitness_new_gen.tolist() == instance.output['Fitness_new_gen']
        
    @staticmethod
    @pytest.mark.parametrize('instance', AGE_BASED_FILES)
    def test_age_based_fitness_pop_age(instance):
        
        instance = Instance('tests/survivor_tests/age_based/',
                            instance)
        new_gen, fitness_new_gen, age_new_gen = SurvivorSelection.age_based(np.array(instance.input['Parents']),
                                                                  np.array(instance.input['Children']),
                                                                  np.array(instance.input['Fitness_parents']),
                                                                  np.array(instance.input['Fitness_children']),
                                                                  np.array(instance.input['Pop_age']),
                                                                  instance.input['Perc_replace'])
        
        assert age_new_gen.tolist() == instance.output['Age_new_gen']
        
    @staticmethod
    @pytest.mark.parametrize('instance', NSGAII_FILES)
    def test_nsgaII_new_gen(instance):
        
        instance = Instance('tests/survivor_tests/nsgaII/',
                            instance)
        new_gen, fitness_new_gen, i = SurvivorSelection.nsgaII(np.array(instance.input['Parents']),
                                                               np.array(instance.input['Children']),
                                                               instance.input['Fitness_parents'],
                                                               instance.input['Fitness_children'])
        
        assert new_gen.tolist() == instance.output['New_gen']
    
    @staticmethod
    @pytest.mark.parametrize('instance', NSGAII_FILES)
    def test_nsgaII_fitness_new_gen(instance):
        
        instance = Instance('tests/survivor_tests/nsgaII/',
                            instance)
        new_gen, fitness_new_gen, i = SurvivorSelection.nsgaII(np.array(instance.input['Parents']),
                                                               np.array(instance.input['Children']),
                                                               instance.input['Fitness_parents'],
                                                               instance.input['Fitness_children'])
        
        assert fitness_new_gen.tolist() == instance.output['Fitness_new_gen']