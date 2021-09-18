'''Import modules'''
import random
import numpy as np

class BinCrossover():
    '''Binary Crossover class'''

    @staticmethod
    def single_point(parent_1, parent_2):
        '''
        single_point operator
        A point on both parents' chromosomes is picked randomly.
        Bits to the right of that point are swapped between the two parent chromosomes.
        '''
        change_position = random.randint(1, len(parent_1)-1)
        child_1 = np.hstack([parent_1[:change_position], parent_2[change_position:]])
        child_2 = np.hstack([parent_2[:change_position], parent_1[change_position:]])

        return child_1, child_2

    @staticmethod
    def uniform(parent_1, parent_2):
        '''
        uniform operator
        Each bit is chosen from either parent with equal probability.
        '''
        random_vector = np.random.choice([0, 1], size=(len(parent_1),))
        def create_child(p1, p2, rv):
            if rv > 0:
                return p1
            else:
                return p2
        vfunc = np.vectorize(create_child)
        child_1 = vfunc(parent_1, parent_2, random_vector)
        child_2 = vfunc(parent_2, parent_1, random_vector)

        return child_1, child_2
