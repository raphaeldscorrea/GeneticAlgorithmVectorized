# -*- coding: utf-8 -*-
"""

"""

import boto3
import json
from boto3.dynamodb.conditions import Attr

from decimal import Decimal
import hashlib
from datetime import datetime
    
def saveDataToS3(racing_obj):
    
    project = "tuning-parameters"
    bucket = "vlr-models-artifacts"
    jobId = hashlib.sha224(datetime.now().strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')).hexdigest()
    
    output_data = {}
    output_data['ConfigData'] = racing_obj.get_config_data()
    output_data['EliteData'] = racing_obj.get_config_elite_data()
    output_data['RacingData'] = racing_obj.get_racing_data()
    output_data['ParametersLimit'] = racing_obj.get_parameters_limit()
    
    s3 = boto3.resource('s3')
    s3object = s3.Object(bucket, project + '/{}.json'.format(jobId)) 
    s3object.put( Body=(bytes(json.dumps(output_data).encode('UTF-8'))))
    s3.ObjectAcl(bucket, project +'/{}.json'.format(jobId)).put(ACL='bucket-owner-full-control')    
    
def saveDataToDynamo(data):
    
    data_json = json.dumps(data)
    
    response = {}
    response['project'] = "tuning-parameters"
    response['job_id'] = hashlib.sha224(datetime.now().strftime('%Y-%m-%d %H:%M:%S').encode('utf-8')).hexdigest()
    response['response'] = data_json
            
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('po_model_results')
    table.put_item(Item=response)
    
    # data = {}
    # data['convergence_time'] = conv_time
    
    # data['fitness_result'] = ga_obj.get_best_fitness()
    # data['parameters'] = {}
    # data['parameters']['crossover_operator'] = ga_obj.crossover_operator_str
    # data['parameters']['mating_operator'] = ga_obj.mating_operator_str
    # data['parameters']['mutation_operator'] = ga_obj.mutation_operator_str
    # data['parameters']['survivor_operator'] = ga_obj.survivor_operator_str
    # data['parameters']['maxiter'] = ga_obj.num_generations
    # data['parameters']['population'] = ga_obj.pop_size
    # data['parameters']['prob_crossover'] = ga_obj.prob_crossover
    # data['parameters']['prob_elitism'] = ga_obj.prob_elitism
    # data['parameters']['prob_mutation'] = ga_obj.prob_mutation
    # data['parameters']['ls_call'] = ga_obj.ls_call
    
    # if ga_obj.ls_call is False:
    #     data['parameters']['sa_alpha'] = False
    #     data['parameters']['sa_N'] = False
    #     data['parameters']['sa_prob'] = False
    #     data['parameters']['sa_stopping_iter'] = False
    #     data['parameters']['sa_stopping_temperature'] = False
    #     data['parameters']['sa_T'] = False
    # else:
    #     data['parameters']['sa_alpha'] = ga_obj.sa_obj.alpha
    #     data['parameters']['sa_N'] = ga_obj.sa_obj.N
    #     data['parameters']['sa_prob'] = ga_obj.sa_obj.prob
    #     data['parameters']['sa_stopping_iter'] = ga_obj.sa_obj.stopping_iter
    #     data['parameters']['sa_stopping_temperature'] = ga_obj.sa_obj.stopping_temperature
    #     data['parameters']['sa_T'] = ga_obj.sa_obj.T
        
    # if ga_obj.keep_best is True:
    #     data['best_fitness'] = ga_obj.get_best_fitness_list()
    #     data['mean_fitness'] = ga_obj.get_mean_fitness_list()
    # else:
    #     data['best_fitness'] = ga_obj.keep_best
    #     data['mean_fitness'] = ga_obj.keep_best
    