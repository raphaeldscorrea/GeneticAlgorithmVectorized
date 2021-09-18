""" Tests related to Perm Mutation """
import os
import pytest

from src.heuristics.game.operators.perm.mutation import PermMutation
from tests.instance import Instance

MUTATION_FILES = [f for f in os.listdir('tests/mutation_tests/mutation/inputs')
                       if os.path.isfile(os.path.join('tests/mutation_tests/mutation/inputs', f))]

class TestClass(object):
    """
        Class with all tests for permutation mutation
    """
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_swap_len(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.swap(instance.input['Individual'])
        
        assert len(individual_mutated) == len(instance.input['Individual'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_swap_duplicates(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.swap(instance.input['Individual'])
        
        assert len(individual_mutated) == len(set(individual_mutated))
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_swap_changes(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.swap(instance.input['Individual'])
        
        assert (individual_mutated.tolist() != instance.input['Individual'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_insert_len(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.insert(instance.input['Individual'])
        
        assert len(individual_mutated) == len(instance.input['Individual'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_insert_duplicates(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.insert(instance.input['Individual'])
        
        assert len(individual_mutated) == len(set(individual_mutated))
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_insert_changes(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.insert(instance.input['Individual'])
        
        assert (individual_mutated.tolist() != instance.input['Individual'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_scramble_len(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.scramble(instance.input['Individual'])
        
        assert len(individual_mutated) == len(instance.input['Individual'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_scramble_duplicates(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.scramble(instance.input['Individual'])
        
        assert len(individual_mutated) == len(set(individual_mutated))
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_scramble_changes(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.scramble(instance.input['Individual'])
        
        assert (individual_mutated.tolist() != instance.input['Individual'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_inversion_len(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.inversion(instance.input['Individual'])
        
        assert len(individual_mutated) == len(instance.input['Individual'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_inversion_duplicates(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.inversion(instance.input['Individual'])
        
        assert len(individual_mutated) == len(set(individual_mutated))
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_inversion_changes(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.inversion(instance.input['Individual'])
        
        assert (individual_mutated.tolist() != instance.input['Individual'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_displacement_len(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.displacement(instance.input['Individual'])
        
        assert len(individual_mutated) == len(instance.input['Individual'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_displacement_duplicates(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.displacement(instance.input['Individual'])
        
        assert len(individual_mutated) == len(set(individual_mutated))
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_displacement_changes(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.displacement(instance.input['Individual'])
        
        assert (individual_mutated.tolist() != instance.input['Individual'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_reverse_len(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.reverse(instance.input['Individual'])
        
        assert len(individual_mutated) == len(instance.input['Individual'])
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_reverse_duplicates(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.reverse(instance.input['Individual'])
        
        assert len(individual_mutated) == len(set(individual_mutated))
        
    @staticmethod
    @pytest.mark.parametrize('instance', MUTATION_FILES)
    def test_reverse_changes(instance):
        
        instance = Instance('tests/mutation_tests/mutation/',
                            instance)
        individual_mutated = PermMutation.reverse(instance.input['Individual'])
        
        assert (individual_mutated != instance.input['Individual'])
        
    