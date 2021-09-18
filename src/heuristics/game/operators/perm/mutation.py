'''Import Modules'''
import random
import numpy as np

class PermMutation():
    '''Permutation - Mutation class'''

    @staticmethod
    def swap(offspring):
        """Swap mutation approach

        Args:
            offspring (list): Offspring to be mutated

        Returns:
            new_offspring[numpy.array]: Mutated offspring
        """
        lb = random.randint(0, int(len(offspring)/2))
        ub = random.randint(lb+1, len(offspring)-1)
        new_offspring = offspring.copy()
        new_offspring[lb] = offspring[ub]
        new_offspring[ub] = offspring[lb]

        offspring = np.array(new_offspring)

        return offspring

    @staticmethod
    def insert(offspring):
        """Insert mutation approach

        Args:
            offspring (list): Offspring to be mutated

        Returns:
            new_offspring[numpy.array]: Mutated offspring
        """
        lb = random.randint(0, int(len(offspring)/2))
        ub = random.randint(lb+1, len(offspring)-1)
        new_offspring = np.hstack([offspring[:lb], offspring[ub],
                                    offspring[lb:ub],
                                    offspring[ub+1:len(offspring)]])

        offspring = new_offspring

        return offspring

    @staticmethod
    def scramble(offspring):
        """Scramble mutation approach

        Args:
            offspring (list): Offspring to be mutated

        Returns:
            new_offspring[numpy.array]: Mutated offspring
        """
        lb = random.randint(0,len(offspring)-4)
        ub = random.randint(lb+3, len(offspring)-1)
        shuffled_positions = offspring[lb:ub]
        random.shuffle(shuffled_positions)
        if (shuffled_positions.tolist() == offspring[lb:ub].tolist()):
            random.shuffle(shuffled_positions)
        new_offspring = np.hstack([offspring[:lb], shuffled_positions,
                                    offspring[ub:len(offspring)]])

        offspring = new_offspring

        return offspring

    @staticmethod
    def inversion(offspring):
        """Inversion mutation approach

        Args:
            offspring (list): Offspring to be mutated

        Returns:
            new_offspring[numpy.array]: Mutated offspring
        """
        lb = random.randint(0, int(len(offspring)/2))
        ub = random.randint(lb+1, len(offspring)-1)
        positions_to_invert = offspring[lb:ub]
        inverted_positions = positions_to_invert[::-1]
        new_offspring = np.hstack([offspring[:lb], inverted_positions,
                                    offspring[ub:len(offspring)]])

        offspring = new_offspring

        return offspring

    @staticmethod
    def displacement(offspring):
        """Displacement mutation approach

        Args:
            offspring (list): Offspring to be mutated

        Returns:
            new_offspring[numpy.array]: Mutated offspring
        """
        lb = random.randint(1, int(len(offspring)/2))
        ub = random.randint(lb+1, len(offspring)-1)
        position = random.randint(0, lb-1)
        new_offspring = np.hstack([offspring[:position], offspring[lb:ub],
                                    offspring[position:lb],
                                    offspring[ub:len(offspring)]])
        offspring = new_offspring

        return offspring

    @staticmethod
    def reverse(offspring):
        """Reverse mutation approach

        Args:
            offspring (list): Offspring to be mutated

        Returns:
            new_offspring[numpy.array]: Mutated offspring
        """
        offspring_copy = offspring.copy()
        l = random.randint(2, len(offspring)- 1)
        i = random.randint(0, len(offspring) - l)
        offspring_copy[i : (i + l)] = reversed(offspring[i : (i + l)])
        return offspring_copy

