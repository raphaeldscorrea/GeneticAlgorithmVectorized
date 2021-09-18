'''Import Modules'''
import numpy as np
from math import ceil
from src.heuristics.game.nsga_II import non_dominated_sorting, crowding_dist
import operator

class SurvivorSelection():
    '''Survivor Selection class'''

    @staticmethod
    def age_based(parents,
                  children,
                  fitness_parents,
                  fitness_children,
                  population_age,
                  perc_replacement,
                  *args,
                  **kwargs):
        '''
        age_based operator
        It is based on the premise that each individual is allowed in the population for a
        finite generation where it is allowed to reproduce, after that, it is kicked out of
        the population no matter how good its fitness is.
        '''
        sa_1_fit = kwargs.get('sa_1_fit', None)
        sa_1_sol = kwargs.get('sa_1_sol', None)
        sa_2_fit = kwargs.get('sa_2_fit', None)
        sa_2_sol = kwargs.get('sa_2_sol', None)

        num_individuals_to_replace = ceil(len(parents) * perc_replacement)
        num_individuals_to_keep = len(parents)-num_individuals_to_replace
        
        parents_age = population_age.copy()

        if sa_1_fit is not None:
            parents_age = np.append(parents_age, (0, 0))
            fitness_parents = np.append(fitness_parents, (sa_1_fit, sa_2_fit))
            parents = np.vstack((parents, sa_1_sol, sa_2_sol))

        # selecting new generation -> first in first out
        sorted_index_parents = np.array(sorted(range(len(parents_age)),
                                               key=parents_age.__getitem__,
                                               reverse=False))

        sorted_index_children = np.array(sorted(range(len(fitness_children)),
                                                key=fitness_children.__getitem__,
                                                reverse=True))

        keeped_children_index = sorted_index_children[0:num_individuals_to_replace,]
        keeped_parents_index = sorted_index_parents[0:num_individuals_to_keep,]
        children_selected = children[keeped_children_index,]
        parents_selected = parents[keeped_parents_index,]

        new_generation = np.vstack((parents_selected, children_selected))
        fitness_new_generation = np.append(fitness_parents[keeped_parents_index,],
                                           fitness_children[keeped_children_index,]) 
        age_new_generation = np.append(parents_age[keeped_parents_index,],
                                       np.zeros(num_individuals_to_replace))
                
        return(new_generation, fitness_new_generation, age_new_generation)
        
    @staticmethod
    def fitness_based(parents,
                      children,
                      fitness_parents,
                      fitness_children,
                      *args,
                      **kwargs):
        '''
        fitness_based operator
        In this fitness based selection, the children tend to replace the least fit individuals
        in the population. The selection of the least fit individuals may be done using a variation
        of any of the selection policies
        '''
        sa_1_fit = kwargs.get('sa_1_fit', None)
        sa_1_sol = kwargs.get('sa_1_sol', None)
        sa_2_fit = kwargs.get('sa_2_fit', None)
        sa_2_sol = kwargs.get('sa_2_sol', None)
        force_unique = kwargs.get('force_unique', False)
                
        fitness_parents_array = (np.array(fitness_parents)).flatten()
        fitness_children_array = (np.array(fitness_children)).flatten()
        
        total_fitness = np.append(fitness_parents_array,fitness_children_array)
        total_population = np.vstack((parents,children))
        
        if force_unique == True:
            unique_individuals, unique_individuals_indexes = np.unique(total_population, return_index=True, axis=0)
            total_population = unique_individuals
            total_fitness = total_fitness[unique_individuals_indexes]
        
        if sa_1_fit is not None:
            total_fitness = np.append(total_fitness, (sa_1_fit, sa_2_fit))
            total_population = np.vstack((total_population, sa_1_sol, sa_2_sol))

        sorted_index = np.array(sorted(range(len(total_fitness)),
                                       key=total_fitness.__getitem__,
                                       reverse=True))

        selected_individuals = sorted_index[0:len(parents),]

        new_generation = total_population[selected_individuals,]
        fitness_new_generation = total_fitness[selected_individuals,]
        
        return(new_generation, fitness_new_generation, 0)
    
    @staticmethod
    def nsgaII(parents,
               children,
               fitness_parents,
               fitness_children,
               *args,
               **kwargs):
        '''
        nsgaII - Multi Objective optimization operator 
        NSGA-II simultaneously optimizes each objective without being dominated by any other solution.
        '''
        total_population = np.vstack((parents, children))
        total_population = total_population.tolist()
        total_fitness = fitness_parents + fitness_children
        pareto_fronts = non_dominated_sorting(total_fitness)

        selected_individuals = []
        selected_fitness = []
        fitness_frontier = []
        individuals_frontier = []
        first_front_solutions = []

        if len(pareto_fronts[0]) > len(parents):
            first_front_fit = operator.itemgetter(*pareto_fronts[0])(total_fitness)
            fitness_total = [list(x) for x in set(tuple(x) for x in first_front_fit)]
            index_list = []
            for i in fitness_total:
                index_list.append(total_fitness.index(i))

            list_solution = operator.itemgetter(*index_list)(total_population)

        begin_front = 0
        end_front = len(pareto_fronts[0])

        while end_front <= len(parents):
            for i in pareto_fronts[begin_front]:
                selected_individuals.append(total_population[i])
                selected_fitness.append(total_fitness[i])
            begin_front += 1
            end_front += len(pareto_fronts[begin_front])

        for i in pareto_fronts[begin_front]:
            fitness_frontier.append(total_fitness[i])
            individuals_frontier.append([i])

        list_distances = crowding_dist(fitness_frontier)

        solutions = []
        for i in range(len(list_distances)):
            new_sol = {}
            new_sol['fit'] = fitness_frontier[i]
            new_sol['ind'] = individuals_frontier[i]
            new_sol['dist'] = list_distances[i]
            new_sol['sol'] = total_population[individuals_frontier[i][0]]
            solutions.append(new_sol)

        order_solutions = sorted(solutions, key=lambda i: i['dist'], reverse=True)

        if len(first_front_solutions) > 0:
            selected_fitness = fitness_total
            selected_individuals = list_solution

        for i in range(0, len(parents)-len(selected_fitness)):
            selected_fitness.append(order_solutions[i]['fit'])
            selected_individuals.append(order_solutions[i]['sol'])

        new_fitness_generation = np.array(selected_fitness)
        new_generation = np.array(selected_individuals)

        return new_generation, new_fitness_generation, 0
