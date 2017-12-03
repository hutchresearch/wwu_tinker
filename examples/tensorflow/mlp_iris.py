#!/usr/bin/python

# Iris classification demo for use with Tinker
# @author: Ryan Baerwolf (baerwor@wwu.edu, rdbaerwolf@gmail.com)

import tensorflow as tf
import numpy as np

class MLP:

    def __init__(self, lr, hidden_size, optimizer, loss_fn):
        
        """
        Loads training data and creates the TensorFlow graph.

        Args:
            lr (float): Learning rate
            hidden_size (int): Number of nodes in the hidden layer
            optimizer (string): Optimization algorithm to use
            loss_fn (string): Name of the loss file
        """

        self.data = data = np.loadtxt("iris_feats.txt")
        self.feats = feats = data[:,:4]
        self.labels = data[:,-1]
        self.loss_fn = loss_fn

        self.n = n = data.shape[0] 	        # Number of datapoints
        self.d = d = feats.shape[1]             # Dimensionality of features
        self.c = c = 3			        # Number of classes
        self.l = l = hidden_size	        # Hidden layer size
        self.LR  = lr		                # Learning Rate

        # Data placeholders
        self.x = x = tf.placeholder(tf.float32, [1, d])
        self.y_ = y_ = tf.placeholder(tf.int32, [1])

        # Hidden layer
        W_x = tf.Variable(tf.random_normal([d, l]))
        b_x = tf.Variable(tf.random_normal([l]))
        h = tf.sigmoid(tf.matmul(x, W_x) + b_x)

        # Output
        W_o = tf.Variable(tf.random_normal([l, c]))
        b_o = tf.Variable(tf.random_normal([c]))
        y = tf.matmul(h, W_o) + b_o

        # Calculate loss and accuracy
        self.loss = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=y_)
        self.accuracy = tf.equal(y_, tf.cast(tf.argmax(y, 1), tf.int32))

        # Select optimizer
        if optimizer == "adam":
            self.optimizer = tf.train.AdamOptimizer(lr)
        elif optimizer == "rms":
            self.optimizer = tf.train.RMSPropOptimizer(lr)
        else:
            self.optimizer = tf.train.GradientDescentOptimizer(lr)

        self.train_op = self.optimizer.minimize(self.loss)


    def train(self, epochs=30):

        """
        Trains the model for the given number of epochs.

        Args:
            epochs (int): Number of times to train on the data set

        Returns:
            ep_loss (float): Loss value of the final epoch
            ep_acc (float): Accuracy achieved in the final epoch
        """

        n = self.n
        d = self.d
        x = self.x
        y_ = self.y_

        with tf.Session() as sess:
            loss_file = open(self.loss_fn, 'a')
            sess.run(tf.global_variables_initializer())

            for ep in range(epochs):
                ep_loss = 0.0
                ep_acc = 0.0
                for i in range(n):
                    _, loss_, acc = sess.run([self.train_op, self.loss, self.accuracy], 
                                              feed_dict={x: self.feats[i,:].reshape(1, d), 
                                                         y_:self.labels[i].reshape(1)})
                    ep_loss += loss_
                    ep_acc += acc

                # Print/write loss at the end of each epoch
                print ("Epoch %s - Loss: %f Acc: %f" % (ep, ep_loss/n, ep_acc/n))
                loss_file.write("Epoch %s - Loss: %f Acc: %f\n" % (ep, ep_loss/n, ep_acc/n))
        return ep_loss/n, ep_acc/n
