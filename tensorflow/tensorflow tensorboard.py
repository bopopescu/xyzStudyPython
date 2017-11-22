#! /usr/bin/python
# -*- coding:utf-8 -*-
"""
@author: abc
@file: tensorflow tensorboard.py
@date: 2017-02-12
"""
__author__ = "abc"
import tensorflow as tf
from tensorflow.python.ops.logging_ops import histogram_summary, scalar_summary
import numpy as np


# 添加神经层 add_layer
def add_layer(inputs, in_size, out_size, n_layer, activation_function=None):
    # add one more layer and return the output of this layer
    layer_name = 'layer%s' % n_layer
    with tf.name_scope('layer'):
        with tf.name_scope('weights'):
            Weights = tf.Variable(tf.random_normal([in_size, out_size]), name='W')
            # histogram_summary(layer_name + '/weights', Weights)
            tf.summary.histogram(layer_name + '/weights', Weights)  # tensorflow >= 0.12

        with tf.name_scope('biases'):
            biases = tf.Variable(tf.zeros([1, out_size]) + 0.1, name='b')
            # histogram_summary(layer_name + '/biase', biases)
            tf.summary.histogram(layer_name + '/biases', biases)  # Tensorflow >= 0.12

        with tf.name_scope('Wx_plus_b'):
            Wx_plus_b = tf.add(tf.matmul(inputs, Weights), biases)

        if activation_function is None:
            outputs = Wx_plus_b
        else:
            outputs = activation_function(Wx_plus_b)

        histogram_summary(layer_name + '/outputs', outputs)
        # tf.summary.histogram(layer_name + '/outputs', outputs) # Tensorflow >= 0.12

    return outputs


# 输入值
with tf.name_scope("inputs"):
    xs = tf.placeholder(tf.float32, [None, 1], name="x_input")
    ys = tf.placeholder(tf.float32, [None, 1], name="y_input")

# 建造神经网络
x_data = np.linspace(-1, 1, 300)[:, np.newaxis]
# 方差0.05, x_data.shape数据形式
noise = np.random.normal(0, 0.05, x_data.shape)
# x_data 二次方
y_data = np.square(x_data) - 0.5 + noise

# 输入层 -> 隐藏层 -> 输出层

# 定义隐藏层 1 输入层神经元数量， 输出层神经元数量，隐藏层神经元数量
l1 = add_layer(xs, 1, 10, n_layer=1, activation_function=tf.nn.relu)
# 定义输出层
prediction = add_layer(l1, 10, 1, n_layer=2, activation_function=None)

with tf.name_scope("loss"):
    # 预测误差 二者差的平方和再求平均值
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices=[1]))
    scalar_summary('loss', loss)
with tf.name_scope("train"):
    # 提供学习效率0.1，通常小于1， 最小化误差
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

with tf.Session() as sess:
    merged = tf.summary.merge_all()
    writer = tf.summary.FileWriter("logs/", sess.graph)
    sess.run(tf.global_variables_initializer())

    for i in range(1000):
        feed_dict = {xs: x_data, ys: y_data}
        sess.run(train_step, feed_dict=feed_dict)
        if i % 50 == 0:
            result = sess.run(merged, feed_dict=feed_dict)
            writer.add_summary(result, i)
