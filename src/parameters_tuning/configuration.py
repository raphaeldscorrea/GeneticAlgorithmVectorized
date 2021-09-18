
"""

"""

class Configuration():
    
    def __init__(self, parameters_distribution, parameters, rank = None):
          
        self._parameters_distribution = parameters_distribution
        self._parameters = parameters
        self._rank = rank

    def get_parent_probability (self, N):
        return (N-(self._rank+1)+1)/(N *(N+1)/2)
    
    @staticmethod
    def update_elite_probability (elite_config_list, it, N_races):
        for elt in elite_config_list:  
            for i in range(len(elt.parameters)): # para cada parametro
                actual = elt.parameters[i]      
                for j in range(len(elt.parameters_distribution[i]['values'])):  
                    if elt.parameters_distribution[i]['values'][j] == actual:
                        delta_p = (it-1)/N_races
                    else:
                        delta_p = 0
                    elt.parameters_distribution[i]['prob'][j] = elt.parameters_distribution[i]['prob'][j] * (1-(it-1)/N_races) + delta_p
                    
        return elite_config_list
   
    def set_rank(self, value):
        self._rank = value
    
    @property
    def parameters_distribution(self):
        return self._parameters_distribution
    
    @property
    def parameters(self):
        return self._parameters
    
    @property  
    def rank(self):
        return self._rank