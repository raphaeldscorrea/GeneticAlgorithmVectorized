# -*- coding: utf-8 -*-

from collections import defaultdict, Counter
import numpy as np

max_f1 = 0
max_f2 = 0
# =============================================================================
#   Non Dominated Sorting Function
#   Input: List of fitness and the objective (minimize or maximize)
#   Output: List of pareto fronts         
# =============================================================================
def non_dominated_sorting_old(fitness,objective="maximize"):
    
    # List of tuples with each objective value
    fitness = [tuple(i) for i in fitness]
    
    # Objectives as keys 
    map_fit_ind = defaultdict(list)
    for i, f_value in enumerate(fitness):
        map_fit_ind[f_value].append(i)
    
    # Creating lists of fronts
    current_front = []
    next_front = []
    
    # The number of individuals dominate you
    dominating_fits = defaultdict(int)
    
    #The individuals you dominate
    dominated_fits = defaultdict(list) 
    
    #Identify if the objective is minimize or maximize
    if(objective == "minimize"):
        sign = [-1, -1]
    else:
        sign = [1, 1]
    
    # Ranking Pareto front
    for i, fit_i in enumerate(fitness):
        for fit_j in fitness[i+1:]:
            if dominates(fit_i, fit_j, sign):
                dominating_fits[fit_j] += 1  
                dominated_fits[fit_i].append(fit_j)  
                
            elif dominates(fit_j, fit_i, sign):  
                dominating_fits[fit_i] += 1
                dominated_fits[fit_j].append(fit_i)
                
        # The first front        
        if dominating_fits[fit_i] == 0: 
            current_front.append(fit_i) 

    fronts = [[]]
    for fit in current_front:
        fronts[-1].extend(map_fit_ind[fit])
    pareto_sorted = len(fronts[-1])
    
    # Rank the next front until all individuals are sorted
    while pareto_sorted < len(fitness):
        fronts.append([])
        for fit_p in current_front:
            for fit_d in dominated_fits[fit_p]:
                dominating_fits[fit_d] -= 1  
                if dominating_fits[fit_d] == 0:
                    next_front.append(fit_d)
                    # Count and append chromosomes with same objectives
                    pareto_sorted += len(map_fit_ind[fit_d])
                    fronts[-1].extend(map_fit_ind[fit_d])
        current_front = next_front
        next_front = []

    return fronts
    
# =============================================================================
#   Dominates function
#   Input: Solutions and the sign (-1,-1 if minimize and 1,1 if maximize)
#   Output: Indicator to check dominance         
# =============================================================================
def dominates(solution1, solution2, sign=[-1, -1]):
    indicator = False
    
    for a, b, sign in zip(solution1, solution2, sign):
        if a * sign > b * sign:
            indicator = True
        # If one of the objectives is dominated, then return False
        elif a * sign < b * sign:
            return False
        
    return indicator

# =============================================================================
#   Crowding Distance Function
#   Input: List of fitness values
#   Output: List of crowding distances         
# =============================================================================
def crowding_dist(fitness = None):

    #Initializing list of distances
    distances = [0.0] * len(fitness)

    # Create keys for fitness values
    crowd = [(f_value,i) for i,f_value in enumerate(fitness)]
    
    number_objectives = len(fitness[0])
    
    for i in range(0,number_objectives):
        
        # Sorting to identify the boundary solutions
        crowd.sort(key=lambda element: element[0][i])
        distances[crowd[0][1]] = float("Inf")
        distances[crowd[-1][1]] = float("Inf")
        
        # Check if objective values of boundary solutions are the same, if true skip this loop
        if crowd[-1][0][i] == crowd[0][0][i]:
            continue
        
        # Normalization
        norm = float(crowd[-1][0][i] - crowd[0][0][i])
        
        for previous, current, successor in zip(crowd[:-2], crowd[1:-1], crowd[2:]):
            distances[current[1]] += (successor[0][i] - previous[0][i]) / norm
            
    return distances

def non_dominated_sorting(fitness):
    fitness_copy = fitness.copy()
    global max_f1
    global max_f2

    def check_dominance_f1(value):
        global max_f1
        result = True if value > max_f1 else False
        max_f1 = value if result == True else max_f1
        
        return result
    
    def check_dominance_f2(value):
        global max_f2
        result = True if value > max_f2 else False
        max_f2 = value if result == True else max_f2
        
        return result
    
    frontier = []
    
    while len(fitness_copy) > 0:  
        sorted_f1 = sorted(fitness_copy, key=lambda tup: (tup[0],tup[1]), reverse=True)
        sorted_f2 = sorted(fitness_copy, key=lambda tup: (tup[1],tup[0]), reverse=True)
                        
        f2_f1_sorted = list(list(zip(*sorted_f1))[1])
        f1_f2_sorted = list(list(zip(*sorted_f2))[0])
        
        max_f1 = f1_f2_sorted[0]
        max_f2 = f2_f1_sorted[0]
                
        results_f1 = np.array(list(map(check_dominance_f1, f1_f2_sorted)))
        results_f2 = np.array(list(map(check_dominance_f2, f2_f1_sorted)))
        
        non_dominated_f1_values = [x for x in sorted_f1 if results_f2[sorted_f1.index(x)]]
        non_dominated_f2_values = [x for x in sorted_f2 if results_f1[sorted_f2.index(x)]]
        
        non_dominated_vals_duplicated = non_dominated_f1_values + non_dominated_f2_values
        non_dominated_vals = [list(x) for x in set(tuple(x) for x in non_dominated_vals_duplicated)]                
        
        if len(non_dominated_vals) > 0:
            #index_non_dominated_vals = [fitness.index(x) for x in non_dominated_vals]
            index_non_dominated_vals = [i for i, x in enumerate(fitness) if x in non_dominated_vals]
            frontier.append(list(index_non_dominated_vals))
            dominated_vals = list(filter(lambda x: x not in non_dominated_vals, fitness_copy))
        else:
            non_dominated_vals = sorted_f1[0]
            frontier.append([fitness.index(non_dominated_vals)])
            dominated_vals = sorted_f1[1:len(sorted_f1)]
                
        counter_dominated_vals = Counter([tuple(i) for i in dominated_vals])
        if len(counter_dominated_vals) == 1:
            #frontier.append([fitness.index(dominated_vals)])
            fitness_copy = []
        else:
            fitness_copy = dominated_vals.copy()
        #print(fitness_copy)
    #print(frontier)
    return frontier
