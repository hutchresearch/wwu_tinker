#!/usr/bin/python
#
# Optimizing the hyperparameters of a simple TensorFlow model via tinker
# @author: Ryan Baerwolf (rdbaerwolf@gmail.com, baerwor@wwu.edu)

from wwu_tinker.experiment import Experiment
from wwu_tinker.variable import Variable

from mlp_iris import MLP

"""iris_expt = Experiment("iris_expt")

iris_expt.add_var(Variable("hidden_size", "int", v_range=[5, 20]))
iris_expt.add_var(Variable("lr", "float", v_range=[0.001, 0.1]))
iris_expt.add_var(Variable("optimizer", "enum", values=["gd", "adam", "rms"]))

expt_id = iris_expt.submit()

for i in range(5):
    config = iris_expt.next_configuration()
    model = MLP(config["lr"], config["hidden_size"], config["optimizer"], loss_fn="iris_loss.txt")
    loss, acc  = model.train()
    config.report_loss(loss)


"""

iris_expt2 = Experiment("iris_expt", optimizer="bayesian")

iris_expt2.add_var(Variable("hidden_size", "int", v_range=[5, 20], step_size=1))
iris_expt2.add_var(Variable("lr", "float", v_range=[0.001, 0.1], step_size=.01))
iris_expt2.add_var(Variable("optimizer", "enum", values=["gd", "adam", "rms"]))

expt_id = iris_expt2.submit()

for i in range(15):
    config = iris_expt2.next_configuration()
    model = MLP(config["lr"], config["hidden_size"], config["optimizer"], loss_fn="iris_loss.txt")
    loss, acc  = model.train()
    config.report_loss(loss)
