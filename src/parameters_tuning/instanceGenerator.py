"""
Script to instantiate Objective Function Class
"""
import sys
import os
import json
import numpy as np

sys.path.append(os.path.abspath(os.path.join('..', 'functions')))
from modelParameters import ModelParameters
from technicalParameters import TechnicalParameters
from userParameters import UserParameters
from toolingsParameters import ToolingsParameters
from orders import Orders
from setup import Setup
from objectiveFunction import ObjectiveFunction
from preProcessing import PreProcessing
from groupedOrders import GroupedOrders

class Instance():
    num_instance = 0     
    INPUTS_DIRECTORY = os.path.curdir + '/inputs/'
    src_files = os.listdir(INPUTS_DIRECTORY)     
    num_total_instances = len(src_files)
    
    def select_instances (num = 1):        
        inputs = []  
        inputs_name = []
        for i in range(num):
            Instance.num_instance += 1
            index = Instance.num_instance%(len(Instance.src_files))
            with open(Instance.INPUTS_DIRECTORY+Instance.src_files[i]) as f:
                inputs_name.append(Instance.src_files[i])
                input_json = json.load(f)
                inputs.append(input_json['input'])
                
        return inputs, inputs_name
        
    def create_fitness_obj (input_data, type_obj = 'mono'):
        grouped_orders_algorithm = "heuristic_1"
        sm_stands = PreProcessing.get_sm_stands_data(input_data)
  
        # Initializing Objects
        technical_parameters = TechnicalParameters(input_data['TechnicalParameters'])
        user_parameters = UserParameters(input_data['UserParameters'])
        toolings_parameters = ToolingsParameters(input_data['ToolingsCosts'])
        model_orders = Orders(input_data['Data'], input_data['JobTimes'], input_data['TubeTimes'], input_data['SchedulingParameters'], user_parameters, sm_stands)
        model_setup = Setup(input_data['Setups'])
        model_grouped_orders = GroupedOrders(model_orders,technical_parameters,grouped_orders_algorithm)
        
        num_variables = model_grouped_orders.get_grouped_data().shape[0]        
        model_parameters = ModelParameters(input_data['ModelParameters'], num_variables)
        objective_function_obj = ObjectiveFunction(type_obj, model_grouped_orders, model_setup, user_parameters, technical_parameters, model_parameters, toolings_parameters)
        
        return (objective_function_obj, num_variables)        
    
    
                
                
                
                
                
                
                
                
                
                