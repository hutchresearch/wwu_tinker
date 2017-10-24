# tinker.py
#
# API for receiving hyperparameter configurations and sending results with the
# Tinker web service

import json
import requests
import traceback
import sys

#server = "http://140.160.142.79:6060/"
server = "http://localhost:6060/"

class Experiment:

    def __init__(self, name, load_fn=None, optimizer = "random"):

        """ 
        Initialize a new experiment with the given name. If load_fn
        is provided, create a new Experiment with the JSON saved in
        load_fn.

        Args:
            name (str): The name of the Experiment to be created
            load_fn (str): Name of the file in which Experiment JSON is saved
            optimizer (str): Name of the optimizer that the user would like to use. This can be set later.

        Todo: Add a validator for loading experiment files? Or just let
              the user be responsible for not messing it up?
        """

        if load_fn is not None:
            load_expt(open(file_name, 'r'))
        else:
            self._data = {"expt_name": name, "vars": {}, "optimizer": optimizer}
        
        self.experiment_id = None

    def __str__(self):
        return json.dumps(self._data, indent=2)

    @property
    def data(self):
        return self._data

    def to_json_string(self):

        """ 
        Convert the internal dict representation of the Experiment
        to a JSON string for sending.

        Returns:
            str: The string representation of the underlying JSON

        Todo: Is ensure_ascii=True necessary? We don't want random
              hex floating around in our messages

        """

        return json.dumps(self._data,sort_keys=True,ensure_ascii=True)

    def save_expt(self, file_name):

        """
        Saves this Experiment in JSON format to the specified file.

        Args:
            file_name (str): Name of the file in which to save the JSON
        """

        json.dump(self._data, open(file_name, 'w'))

    def load_expt(self, file_name):

        """
        Load the JSON in file_name into this Experiment.

        Args:
            file_name (str): Name of the file from which to load an Experiment JSON
        """

        self._data = json.load(open(file_name, 'r'))

    def add_var(self, var):

        """
        Adds a Variable to this Experiment.

        Args:
            var (Variable): Any valid variable
        """

        if isinstance(var, Variable) == False:
            print("Error: var must be of type Variable")
            return
        var_dict = {}
        var_dict["type"] = var.type
        if var.type == "int" or var.type == "float":
            var_dict["range"] = var.range
            if var.step_size is not None:
                var_dict["step_size"] = var.step_size
        else: 
            var_dict["values"] = var.values
        self._data["vars"][var.name] = var_dict 

    def add_vars(self, var_list):

        """
        Simultaneously adds multiple variables to this Experiment.

        Args:
            var_list (list): The list of Variable objects to be added
        """

        if isinstance(var_list, list) == False:
            print("Error: var_list must be a list of Variables!")
            return
        else:
            for var in var_list:
                self.add_var(var)

    def set_optimizer(self, optimizer):

        """
        Sets the optimizer for the for the experiment. Verifies that it is a valid optimizer.

        Args:
            optimizer (string): The optimizer you would like to set up for your experiment.
        """
        if optimizer in ["random", "bayesian", "grid", "horde", "latin_hyper"]:
            self._data["optimizer"] = optimizer
        else:
            print("%s is not a valid optimizer" % optimizer)

    def submit(self):

        """
        Sends the Experiment JSON to the server to be inserted into
        the database.

        Todo: Make sure that the user isn't inserting the experiment multiple times

        Returns:
            str: ID corresponding to the server-side experiment
            
        """

        r = requests.post(server + "setup", json=self._data) 
        response_json = r.json()
        self.experiment_id = response_json["expt_id"]
        return self.experiment_id

    def next_configuration(self,order_size=1):

        """ 
        Requests the next configuration for evaluation from the server.

        Args:
            order_size (int): Number of configurations to be retrieved

        Returns:
            JSON/dict: Dictionary of hyperparameter values for all variables 
                       in the experiment

        """

        payload = {"expt_id":self.experiment_id,"order_size":order_size}
        r = requests.post(server + "request", json=payload) 
        response_json = r.json()
        return Configuration(json.loads(r.text))


class Configuration():

    def __init__(self, config_json):
        
        """
        Creates a new Configuration object given the raw JSON
        returned by the server by next_configuration in the 
        Experiment class.

        Args:
            config_json (JSON/dict): raw configuration JSON returned by the server

        """

        self.data = config_json

    def __getitem__(self, key):

        """
        Allows for dict-like retrieval of elements.

        Args:
            key (str): Name of a hyperparameter in the config
        
        Returns:
            value: Int, float, or enum associated with hyperparameter
        """

        value = self.data["config"][key]
        if value is None:
            print "The key '%s' does not exist in this configuration"
        else:
            return self.data["config"][key]

    def get_eval_id(self):

        """
        Retrieves the ID corresponding to the evaluation in the database

        Returns:
            str: Evaluation ID

        """

        return self.data["eval_id"]

    def get_value(self, key):

        """
        Retrieves the value associated with a given variable.

        Args:
            name (str): Name of the variable to retrieve

        Returns:
            str: Value of the variable with key 'name'

        """

        value = self.data["config"][key]
        if value is None:
            print "The key '%s' does not exist in this configuration"
        else:
            return self.data["config"][key]

    def report_loss(self, loss):

        """
        Adds a loss value to this configuration and returns it to the server.

        Args:
            loss (float): Loss generated by running a model with this configuration

        Todo: There should be something returned from the post request indicate success/failure
        """

        try:
            loss = float(loss)
            self.data["result"] = loss
            r = requests.post(server + "report", json=self.data)
        except ValueError:
            traceback.print_stack()
            print("Error: reported loss must be a parsable float")



class Variable:

    var_names = set()

    #TODO: Add client side validation that step_size is filled in if gridsearch is selected as optimizer
    def __init__(self, name, v_type, v_range=None, values=None, step_size=None):

        """ 
        Creates a new variable object to be inserted into an Experiment.
        
        Args:
            name (str): The name of the variable. Must be unique.
            v_type (str): Type of variable. (int, float, or enum)
            v_range (list/tuple): A min and max range to test (only for int/float Variables)
            values (list): The list of possible enum values (only for enum Variables)
            step_size(int or float): the preferred step size for use with grid search
        """

        if Variable.__validate(name, v_type, v_range, values, step_size):
            self._name = name
            self._type = v_type
            self._range = v_range
            self._values = values
            self._step_size = step_size

    @staticmethod
    def __validate(name, v_type, v_range=None, values=None, step_size=None):

        """
        Checks that the provided fields can create a valid Variable.

        Args:
            name (str): The name of the variable. Must be unique.
            v_type (str): Type of variable. (int, float, or enum)
            v_range (list/tuple): A min and max range to test (only for int/float Variables)
            values (list): The list of possible enum values (only for enum Variables)
        Returns:
            bool: True if the provided parameters are valid, false otherwise
        """

        if name in Variable.var_names:
            print("Error: a variable with name \"%s\" already exists!" % name)
            return False
        else:
            Variable.var_names.add(name)
        if v_type == "int" or v_type == "float":
            if v_range is None:
                print("Error: must provide a range for variable type \"%s\"" % v_type)
                return False
            elif isinstance(v_range,list) == False:
                print("Error: range must be a list of ints [MIN, MAX]")
                return False
            elif len(v_range) != 2:
                print ("Error: range list must contain a MAX and MIN")
                return False
            elif v_type == "int" :
                if not all(isinstance(n, int) for n in v_range):
                    print("Error: elements in v_range must match v_type")
                    return False
                elif step_size != None and not isinstance(step_size, int):
                    print("Error: element in step_size must match v_type")
                    return False
            elif v_type == "float":
                if not all(isinstance(n, float) for n in v_range):
                    print("Error: elements in v_range must match v_type")
                    return False
                elif step_size != None and not isinstance(step_size, float):
                    print("Error: elements in v_range must match v_type")
                    return False
            return True
        elif v_type == "enum":
            if values is None:
                print("Error: must provide a set of values for variable type enum!")
                return False
            else:
                return True
        else:
            print("Error: \"%s\" is not a valid variable type" % v_type)
            return False
   
    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def range(self):
        return self._range

    @property
    def values(self):
        return self._values

    @property
    def step_size(self):
        return self._step_size