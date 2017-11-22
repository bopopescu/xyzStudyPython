# -*- coding:utf-8 -*-

import os
import shutil
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data", one_hot=True)
log_path = 'logs/'

if os.path.exists(log_path):
    shutil.rmtree(log_path)
    os.mkdir(log_path)

INPUT_NODE = 784
OUTPUT_NODE = 10

LAYER1_NODE = 500
BATCH_SIZE = 100

LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY = 0.99
REGULARIZATION_RATE = 0.0001
TRAINING_STEPS = 3000
MOVING_AVERAGE_DECAY = 0.99
TRAINING_PRINT_STEPS = 100


def inference(input_tensor, avg_class, weights1, biases1, weights2, biases2):
    if avg_class is None:
        layer1 = tf.nn.relu(tf.matmul(input_tensor, weights1) + biases1)
        return tf.matmul(layer1, weights2) + biases2
    else:
        layer1 = tf.nn.relu(tf.matmul(input_tensor, avg_class.average(weights1)) + avg_class.average(biases1))
        return tf.matmul(layer1, avg_class.average(weights2)) + avg_class.average(biases2)


x = tf.placeholder(tf.float32, [None, INPUT_NODE], name='x-input')
y_ = tf.placeholder(tf.float32, [None, OUTPUT_NODE], name='y-input')

weights1 = tf.Variable(tf.truncated_normal([INPUT_NODE, LAYER1_NODE], stddev=0.1))
biases1 = tf.Variable(tf.constant(0.1, shape=[LAYER1_NODE]))

weights2 = tf.Variable(tf.truncated_normal([LAYER1_NODE, OUTPUT_NODE], stddev=0.1))
biases2 = tf.Variable(tf.constant(0.1, shape=[OUTPUT_NODE]))

y = inference(x, None, weights1, biases1, weights2, biases2)

global_step = tf.Variable(0, trainable=False)
tf.summary.scalar('global_step', global_step)

variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)

variables_averages_op = variable_averages.apply(tf.trainable_variables())

average_y = inference(x, variable_averages, weights1, biases1, weights2, biases2)

cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))

cross_entropy_mean = tf.reduce_mean(cross_entropy)
tf.summary.scalar('cross_entropy_mean', cross_entropy_mean)

regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
regularization = regularizer(weights1) + regularizer(weights2)
tf.summary.scalar('regularization', regularization)

loss = cross_entropy_mean + regularization
tf.summary.scalar('loss', loss)

learnging_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step, mnist.train.num_examples / BATCH_SIZE,
                                            LEARNING_RATE_DECAY)
tf.summary.scalar('learnging_rate', learnging_rate)

train_step = tf.train.GradientDescentOptimizer(learnging_rate).minimize(loss, global_step=global_step)

with tf.control_dependencies([train_step, variables_averages_op]):
    train_op = tf.no_op(name='train')

correct_prediction = tf.equal(tf.argmax(average_y, 1), tf.argmax(y_, 1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


with tf.Session() as sess:
    merged = tf.summary.merge_all()
    writer = tf.summary.FileWriter(log_path, sess.graph)
    tf.global_variables_initializer().run()
    validate_feed = {x: mnist.validation.images,
                     y_: mnist.validation.labels}
    test_feed = {x: mnist.test.images, y_: mnist.test.labels}

    for i in range(TRAINING_STEPS):
        if i % TRAINING_PRINT_STEPS == 0:
            validate_acc = sess.run(accuracy, feed_dict=validate_feed)
            print i, validate_acc
        xs, ys = mnist.train.next_batch(BATCH_SIZE)
        sess.run(train_op, feed_dict={x: xs, y_: ys})
        result = sess.run(merged, feed_dict={x: xs, y_: ys})
        writer.add_summary(result, i)

    test_acc = sess.run(accuracy, feed_dict=test_feed)
    print TRAINING_STEPS, test_acc
