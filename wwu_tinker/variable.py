import json
import requests
import traceback

class Variable:
    var_names = set()

    # TODO: Add client side validation that step_size is filled in if gridsearch is selected as optimizer
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
            elif isinstance(v_range, list) == False:
                print("Error: range must be a list of ints [MIN, MAX]")
                return False
            elif len(v_range) != 2:
                print ("Error: range list must contain a MAX and MIN")
                return False
            elif v_type == "int":
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