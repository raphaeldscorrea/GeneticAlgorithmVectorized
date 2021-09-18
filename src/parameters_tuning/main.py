#************************************************************
# Parameters Tuning
# Author: Aurea Halfeld and Gabriela Girundi and Lara Cota
# Vallourec Soluções Tubulares do Brasil
#************************************************************

# Import libraries
from gaParameters import gaParameters
from preTuning import preTuning
from saParameters import saParameters
from iRace import Racing
from handleraws import saveDataToS3

import logging
import argparse

# Add functions to sys.path that will be used for all files loaded after this
import os
import sys
sys.path.append(os.path.abspath(os.path.join('..', 'functions')))
from applogging import logging_levels, init_logging

# mainFunc 
def tuning_parameters ():
    
    ga_param_obj = GAParameters()
    racing_obj = Racing(ga_param_obj,
                        num_parameters = 7,
                        num_experiments = 200)
    
    logging.info('Running Parameters Tuning ...')
    # sa_param_obj = SAParameters()
    # racing_obj = Racing(sa_param_obj,
    #                     num_parameters = 5,
    #                     num_experiments = 1500)
    
    config_elite_list = racing_obj.iterated_racing()
    best_config = ga_param_obj.getConfigData(config_elite_list[0])
    logging.info('Calculation finished.')
    
    saveDataToS3(racing_obj)
    logging.info('Results saved in S3.')
        
    return best_config

if __name__ == "__main__":
    
    # Argument parsing
    aparser = argparse.ArgumentParser()
    
    leveldic = logging_levels()
    aparser.add_argument('--loglevel',
        help="Log level integer value where options are: {0}"
            .format(['{0} = {1}'.format(k, v) for k,v in leveldic.items()]),
        required=True,
        type=int,
        choices=[v for v in leveldic.values()])
    args = aparser.parse_args()
    
    init_logging(args.loglevel)
    
    # Call IRace
    best_parameters = tuning_parameters()
    logging.info('Best Parameters Configuration:')
    logging.info(best_parameters)
    
