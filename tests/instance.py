''' Instance Class '''
import json

class Instance():
    '''
        Class to read all instances for unit tests.
    '''
    def __init__(self, test_paste, instance, general=False):
        '''
            Load files used as input and output for all tests.
                - test_paste: name of the specific paste of the test
                - instance: name of the instance which is being tested in this call
        '''
        with open(str(test_paste) + 'inputs/' +
                  str(instance), encoding='UTF8') as input_json:
            self._input = json.load(input_json)

        with open(str(test_paste) + 'outputs/' +
                  str(instance), encoding='UTF8') as input_json:
            self._output = json.load(input_json)

        if general:
            with open(str(test_paste) + 'general.json', encoding='UTF8') as input_json:
                self._general = json.load(input_json)

    @property
    def input(self):
        ''' Get input data '''
        return self._input

    @property
    def output(self):
        ''' Get output data '''
        return self._output

    @property
    def general(self):
        ''' Get general data: parameters that are the same for all inputs used in the test '''
        return self._general
