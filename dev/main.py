''''Import Modules'''
import time
import numpy as np

from src.heuristics.game.ga import GA
from src.heuristics.game.pareto import get_solutions
from src.functions.objective_function import ObjectiveFunction

POP_SIZE = 200
SOL_SIZE = 30
OBJECTIVE_WEIGHT = np.random.randint(5, size=(SOL_SIZE, SOL_SIZE))

def single_test():
    '''
    Single test function
    '''
    type_obj = 'mono'
    fitness_class = ObjectiveFunction(type_obj,
                                      weigths=OBJECTIVE_WEIGHT)

    ga_class = GA("perm", fitness_class, POP_SIZE, SOL_SIZE, ls_call=False,
                  max_iteration=10, mating_operator="ranking",
                  mutation_operator='scramble', crossover_operator='ox',
                  survivor_operator='fitness_based', run=10,
                  parallel_call=False)

    start = time.time()
    ga_class.generations()
    end = time.time()
    print(end-start)

    solutions = ga_class.get_population()
    if type_obj == 'multi':
        fit_1, fit_2 = ga_class.get_fitness()
        final_fitness, final_solutions = get_solutions(5, fit_1, fit_2, solutions)
    else:
        fit_1 = ga_class.get_fitness()

    print(ga_class.get_best_fitness())
    print(ga_class.get_best_individual()[0])

    if type_obj == 'multi':
        return final_fitness, final_solutions

def testing_operators_mono():
    '''
    Function to test operators - Mono objective
    '''
    # Ox e Ox2 estão com problema
    mutation_op = ['swap', 'insert', 'scramble', 'inversion', 'displacement']
    #crossover_op = ['pmx', 'ox', 'ox_2', 'obx', 'cycle']
    #crossover_op = ['ox', 'ox_2', 'obx', 'cycle']
    #crossover_op = ['ox_2', 'obx', 'cycle']
    #crossover_op = ['obx', 'cycle']
    crossover_op = ['pmx', 'obx', 'cycle']
    survivor_op = ['age_based', 'fitness_based']
    mating_op = ['roulette_wheel', 'ranking']
    type_obj = 'mono'

    fitness_class = ObjectiveFunction(type_obj,
                                      weigths=OBJECTIVE_WEIGHT)

    for mut in mutation_op:
        for cross in crossover_op:
            for surv in survivor_op:
                for mat in mating_op:
                    ga_class = None
                    print("operators:", mut, cross, surv, mat)
                    ga_class = GA("perm", fitness_class, POP_SIZE, SOL_SIZE,
                                  ls_call=True, max_iteration=3, crossover_operator=cross,
                                  mutation_operator=mut, mating_operator=mat,
                                  survivor_operator=surv)
                    start = time.time()
                    ga_class.generations()
                    end = time.time()
                    print(end-start)
                    print(ga_class.get_best_fitness())

def testing_operators_multi():
    '''
    Function to test operators - Multi objective
    '''
    mutation_op = ['swap', 'insert', 'scramble', 'inversion', 'displacement']
    #crossover_op = ['pmx', 'ox', 'ox_2', 'obx', 'cycle']
    crossover_op = ['pmx', 'obx', 'cycle']
    survivor_op = ['nsgaII']
    mating_op = ['roulette_wheel', 'ranking']
    type_obj = 'multi'

    fitness_class = ObjectiveFunction(type_obj,
                                      weigths=OBJECTIVE_WEIGHT)

    for mut in mutation_op:
        for cross in crossover_op:
            for surv in survivor_op:
                for mat in mating_op:
                    ga_class = None
                    print("operators:", mut, cross, surv, mat)
                    ga_class = GA("perm", fitness_class, POP_SIZE, SOL_SIZE,
                                  ls_call=True, max_iteration=3, crossover_operator=cross,
                                  mutation_operator=mut, mating_operator=mat,
                                  survivor_operator=surv)
                    start = time.time()
                    ga_class.generations()
                    end = time.time()
                    print(end-start)
                    print(ga_class.get_best_fitness())

if __name__ == '__main__':

    single_test()
    #testing_operators_mono()
    #testing_operators_multi()
