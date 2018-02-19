# api_test.py
#
# Quick demonstration of the tinker Python API. We can create experiments,
# variables, and print the underlying JSON representations.

from wwu_tinker import experiment
from wwu_tinker import variable

################# Simple Experiment ######################
'''
expt = Experiment("simple_expt")
int_var = Variable("var1", "int", v_range=[0, 10])
float_var = Variable("var2", "float", v_range=[0.1, 0.5])

expt.add_var(int_var)
expt.add_var(float_var)

print(expt)
'''
##########################################################


############### Adding Variable Lists ####################
'''
expt = Experiment("list_expt")
enum_var = Variable("optimizer", "enum", values=["gd", "adam", "rmsprop"])
var_list = [Variable(("int_%s" % i), "int", v_range=[1, 5]) for i in range(10)]

expt.add_var(enum_var)
expt.add_vars(var_list)

print(expt)
'''
##########################################################


############# Variable Names Must Be Unique ##############
'''
var1 = Variable("Bill", "int", v_range=[1, 100])
var2 = Variable("Suzy", "float", v_range=[0.015, 5.0])
impostor = Variable("Bill", "enum", values=["foo", "bar"])
'''
##########################################################


############# Submit Experiment to Server ################

expt = experiment.Experiment("submit_expt") 
int_var = variable.Variable("var1", "int", v_range=[0, 10])
expt.add_var(int_var)
print ("EXPT ID: %s" % expt.submit())

############# Request A Configuration To Evaluate ########
config = expt.next_configuration()
config.get_value("var1")
config.report_loss("10")
##########################################################

