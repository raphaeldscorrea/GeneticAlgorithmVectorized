'''Import Modules'''
import numpy as np

class BinMutation():
    '''Binary - Mutation class'''
    @staticmethod
    def bit_inversion(individual, prob_mutation):
        '''
        bit_inversion operator
        Select a subset of genes like in scramble mutation, but instead of shuffling the subset,
        we merely invert the entire string in the subset.
        '''
        random_vector = np.random.uniform(0, 1, len(individual))

        def mutate_individual(ind, vec_prob, prob_mutation):
            if vec_prob < prob_mutation:
                ind = 1-ind
            return ind

        vfunc = np.vectorize(mutate_individual)
        new_individual = vfunc(individual, random_vector, prob_mutation)

        return new_individual
