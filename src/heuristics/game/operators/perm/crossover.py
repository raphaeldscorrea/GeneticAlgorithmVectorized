'''Import Modules'''
import random
import copy
from math import floor
import numpy as np

class PermCrossover():
    '''Permutation Crossover class'''
    @staticmethod
    def pmx(parent_1, parent_2):
        '''
        pmx operator
        '''
        lb = random.randint(0, len(parent_1)-1)
        ub = random.randint(lb, len(parent_1)-1)

        #offspring 1
        part_1_offspring_1 = parent_1[lb:ub]
        part_2_offspring_1 = np.hstack([parent_2[:lb], parent_2[ub:len(parent_2)]])
        repeated_elements = np.isin(part_2_offspring_1, part_1_offspring_1)

        part_1_offspring_2 = parent_2[lb:ub]
        repeat_elements_parts_1 = np.isin(part_1_offspring_2, part_1_offspring_1, invert=True)
        repeated_values_part_1 = part_1_offspring_2[repeat_elements_parts_1]

        np.place(part_2_offspring_1, repeated_elements, repeated_values_part_1)
        final_value_1 = np.hstack([part_2_offspring_1[:lb], part_1_offspring_1,
                                   part_2_offspring_1[lb:len(part_2_offspring_1)]])

        #offspring 2
        part_1_offspring_2 = parent_2[lb:ub]
        part_2_offspring_2 = np.hstack([parent_1[:lb], parent_1[ub:len(parent_2)]])
        repeated_elements = np.isin(part_2_offspring_2, part_1_offspring_2)

        part_1_offspring_1 = parent_1[lb:ub]
        repeat_elements_parts_1 = np.isin(part_1_offspring_1, part_1_offspring_2, invert=True)
        repeated_values_part_1 = part_1_offspring_1[repeat_elements_parts_1]

        np.place(part_2_offspring_2, repeated_elements, repeated_values_part_1)

        final_value_2 = np.hstack([part_2_offspring_2[:lb], part_1_offspring_2,
                                   part_2_offspring_2[lb:len(part_2_offspring_2)]])

        return final_value_1, final_value_2

    @staticmethod
    def pmx_2(parent_1, parent_2):
        """Partially-Mapped crossover approach

        Args:
            parent_1 (list): First parent selected for crossover
            parent_2 (list): Second parent selected for crossover

        Returns:
            offspring_1 (list): First children created by Partially-Mapped crossover
            offspring_1 (list): Second children created by Partially-Mapped crossover
        """
        lb = random.randint(0,len(parent_1)-1)
        ub = random.randint(lb,len(parent_1)-1)
        
        #offspring 1
        offspring_1 = [-1 for i in range(len(parent_1))]
        parent_1_offspring_1 = parent_1[lb:ub]
        offspring_1[lb:ub] = parent_1_offspring_1
        
        for i in range(len(parent_1)):
            if parent_2[i] not in offspring_1 and offspring_1[i] == -1:
                offspring_1[i] = parent_2[i]
            elif parent_2[i] in offspring_1 and offspring_1[i] == -1:
                free_space = False
                index_search = i
                while free_space == False:
                    selected = parent_2[list(parent_1).index(parent_2[index_search])]
                    if selected not in offspring_1:
                        free_space = True
                    else:
                        index_search = list(parent_2).index(selected)
                offspring_1[i] = selected 
                    
        #offspring 2
        offspring_2 = [-1 for i in range(len(parent_1))]
        parent_2_offspring_2 = parent_2[lb:ub]
        offspring_2[lb:ub] = parent_2_offspring_2
        
        for i in range(len(parent_1)):
            if parent_1[i] not in offspring_2 and offspring_2[i] == -1:
                offspring_2[i] = parent_1[i]
            elif parent_1[i] in offspring_2 and offspring_2[i] == -1:
                free_space = False
                index_search = i
                while free_space == False:
                    selected = parent_1[list(parent_2).index(parent_1[index_search])]
                    if selected not in offspring_2:
                        free_space = True
                    else:
                        index_search = list(parent_1).index(selected)
                offspring_2[i] = selected 
                
        return (offspring_1, offspring_2)

    @staticmethod
    def ox(parent_1, parent_2):
        """Order crossover approach

        Args:
            parent_1 (list): First parent selected for crossover
            parent_2 (list): Second parent selected for crossover

        Returns:
            offspring_1 (list): First children created by order crossover
            offspring_1 (list): Second children created by order crossover
        """
        lb = random.randint(0, len(parent_1)-1)
        ub = random.randint(lb, len(parent_1)-1)

        parent_1_np = np.array(parent_1)
        parent_2_np = np.array(parent_2)

        new_offspring_1 = np.full(len(parent_1), -1,  dtype=int)
        new_offspring_1[lb:ub] = parent_1[lb:ub]
        
        new_offspring_1[np.where(new_offspring_1 == -1)[0]] = parent_2_np[np.isin(parent_2,
                                                                                 parent_1[lb:ub],
                                                                                 invert=True)]

        new_offspring_2 = np.full(len(parent_2), -1, dtype=int)
        new_offspring_2[lb:ub] = parent_2[lb:ub]
        new_offspring_2[np.where(new_offspring_2 == -1)[0]] = parent_1_np[np.isin(parent_1,
                                                                                 parent_2[lb:ub],
                                                                                 invert=True)]

        return list(new_offspring_1), list(new_offspring_2)

    @staticmethod
    def obx(parent_1, parent_2, num_changes=None):
        """Order based crossover approach

        Args:
            parent_1 (list): First parent selected for crossover
            parent_2 (list): Second parent selected for crossover
            num_changes (int, optional): Number of changes in each individual. Defaults to None.

        Returns:
            offspring_1 (list): First children created by order based crossover
            offspring_1 (list): Second children created by order based crossover
        """
        if num_changes is None:
            num_changes = floor(len(parent_1)/2)

        offspring_1 = parent_1.copy()
        offspring_2 = parent_2.copy()

        index_values = np.array(sorted(np.random.choice(np.arange(len(parent_1)),
                                                        num_changes,
                                                        replace=False)))

        offspring_1[index_values] = parent_2[np.isin(parent_2, parent_1[index_values])]
        offspring_2[index_values] = parent_1[np.isin(parent_1, parent_2[index_values])]

        return offspring_1, offspring_2

    @staticmethod
    def ox_2(parent_1, parent_2, num_changes=None):
        """Order crossover new approach

        Args:
            parent_1 (list): First parent selected for crossover
            parent_2 (list): Second parent selected for crossover
            num_changes (int, optional): Number of changes in each individual. Defaults to None.

        Returns:
            offspring_1 (list): First children created by order crossover
            offspring_1 (list): Second children created by order crossover
        """
        if num_changes is None:
            num_changes = floor(len(parent_1)/2)

        offspring_1 = parent_1.copy()
        offspring_2 = parent_2.copy()

        element_values = np.random.choice(parent_1, num_changes, replace=False)

        offspring_1[np.isin(offspring_1, element_values)] = parent_2[np.isin(parent_2, element_values)]
        offspring_2[np.isin(offspring_2, element_values)] = parent_1[np.isin(parent_1, element_values)]

        return offspring_1, offspring_2

    @staticmethod
    def cycle(parent_1, parent_2):
        """Cycle crossover approach

        Args:
            parent_1 (list): First parent selected for crossover
            parent_2 (list): Second parent selected for crossover

        Returns:
            offspring_1 (list): First children created by cycle crossover
            offspring_1 (list): Second children created by cycle crossover
        """
        idx_1 = []
        n = 1
        idx = 0
        parent_1 = np.array(parent_1)
        parent_2 = np.array(parent_2)
        indexes = np.array(range(len(parent_1)))

        def find_element(vector, x):
            idx = np.where(np.array(vector) == x)[0][0]
            return idx

        def cross_recursion(parent_1, parent_2, n, idx, idx_1):
            if find_element(parent_2, parent_1[idx]) == 0:
                idx_1.append(0)
                return idx_1
            idx = find_element(parent_2, parent_1[idx])
            idx_1.append(idx)
            return cross_recursion(parent_1, parent_2, n, idx, idx_1)

        changes = np.delete(indexes, cross_recursion(parent_1, parent_2, n, idx, idx_1))

        child_1 = copy.copy(parent_1)
        child_2 = copy.copy(parent_2)
        child_1[changes] = copy.copy(parent_2[changes])
        child_2[changes] = copy.copy(parent_1[changes])

        return child_1, child_2
