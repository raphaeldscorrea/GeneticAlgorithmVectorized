"""
Decorators: decorators for GAME methods
Authors: Raphael Corrêa
"""

def check_fitness_type(func):
    '''
    Check if the objective is mono or multi.
    Default is mono objective
    '''
    def inner(ref, var):
        if var in 'mono' or var in 'multi':
            var = func(ref, var)
        else:
            var = func(ref, 'mono')
        return var
    return inner

def convert_list(func):
    '''
    Check if individual is list and converts if necessary
    '''
    def inner(ref, var):
        if isinstance(var, list):
            var = func(ref, var)
        else:
            var_list = var.tolist()
            var = func(ref, var_list)
        return var
    return inner
