import json
import requests
import traceback

from .configuration import Configuration
from .variable import Variable
from .__init__ import server

class Experiment:
    def __init__(self, name, load_fn=None, optimizer="random"):

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
            self.load_expt(open(load_fn, 'r'))
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

        return json.dumps(self._data, sort_keys=True, ensure_ascii=True)

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

    def next_configuration(self, order_size=1):

        """
        Requests the next configuration for evaluation from the server.

        Args:
            order_size (int): Number of configurations to be retrieved

        Returns:
            JSON/dict: Dictionary of hyperparameter values for all variables
                       in the experiment

        """

        payload = {"expt_id": self.experiment_id, "order_size": order_size}
        r = requests.post(server + "request", json=payload)
        response_json = r.json()
        return Configuration(json.loads(r.text))
