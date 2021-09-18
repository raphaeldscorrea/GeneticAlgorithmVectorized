'''Import Modules'''
import operator
from src.heuristics.game.nsga_II import non_dominated_sorting, crowding_dist

def get_solutions(num_solutions, fit_1, fit_2, solutions):
    '''
    Parameters
    ----------
    num_solutions : Number
        Number of solutions that will be returned
    fit_1 : Number
        Fitness value of objective function 1.
    fit_2 : Number
        Fitness value of objective function 2.
    solutions : List
        List of total solutions .

    Returns
    -------
    response_fitness : Tuple
        Values of fitness 1 and fitness 2.
    response_solutions : List
        List of solutions.

    '''
    agg_fitness_total = []
    for i, j in zip(fit_1, fit_2):
        agg_fitness_total.append([i, j])

    fitness_total = [list(x) for x in set(tuple(x) for x in agg_fitness_total)]

    index_list = []
    for i in fitness_total:
        index_list.append(agg_fitness_total.index(i))

    list_solution = operator.itemgetter(*index_list)(solutions)
    pareto_fronts = non_dominated_sorting(fitness_total)

    if len(pareto_fronts[0]) > num_solutions:

        fitness_frontier = []
        individuals_frontier = []

        for i in pareto_fronts[0]:
            fitness_frontier.append(fitness_total[i])
            individuals_frontier.append([i])

        list_distances = crowding_dist(fitness_frontier)

        solutions = []
        for i in range(len(list_distances)):
            new_sol = {}
            new_sol['fit'] = fitness_frontier[i]
            new_sol['ind'] = individuals_frontier[i]
            new_sol['dist'] = list_distances[i]
            new_sol['sol'] = list_solution[individuals_frontier[i][0]]
            solutions.append(new_sol)

        order_solutions = sorted(solutions, key=lambda i: i['dist'], reverse=True)

        fitness_ordered = [x['fit'] for x in order_solutions]
        individuals_ordered = [x['sol'] for x in order_solutions]
        response_fitness = fitness_ordered[0:num_solutions]
        response_solutions = individuals_ordered[0:num_solutions]

    else:
        response_fitness = operator.itemgetter(*pareto_fronts[0])(fitness_total)
        response_solutions = operator.itemgetter(*pareto_fronts[0])(list_solution)

    return response_fitness, response_solutions

def calculate_hypervolumn(pareto_fitness, max_f1, max_f2):
    '''
    Function to compare the quality of solutions
    '''
    sort_pareto_fitness = sorted(pareto_fitness, reverse=True)
    norm_pareto_fitness = [[abs(x[0])/max_f1, abs(x[1])/max_f2] for x in sort_pareto_fitness]
    total_vol = 0
    total_vol = norm_pareto_fitness[0][0]*norm_pareto_fitness[0][1]
    if len(norm_pareto_fitness) > 0:
        for i in range(1, len(norm_pareto_fitness)):
            total_vol += abs((norm_pareto_fitness[i][0]-norm_pareto_fitness[i-1][0]))*norm_pareto_fitness[i][1]

    return total_vol
