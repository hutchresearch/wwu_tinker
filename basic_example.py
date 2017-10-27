from Tinker.experiment import Experiment
from Tinker.variable import Variable

# This is a simple test to see how the database works.
# First we define a cost function and then we use random search to find its minimum.
def cost_function(x,y):
        return x*x+y*y

# Test the cost function.
z = cost_function(3,2)
print z

# Now we define our experiment
test_experiment = Experiment('test_experiment', optimizer="bayesian")
# Next we add our variables
test_experiment.add_var(Variable('x', 'float', v_range=[-10.0,10.0]))
test_experiment.add_var(Variable('y', 'float', v_range=[-10.0,10.0]))
experiment_id = test_experiment.submit()
for i in range(50):
        config = test_experiment.next_configuration()
        result = cost_function(config['x'],config['y'])
        print result
        config.report_loss(result)