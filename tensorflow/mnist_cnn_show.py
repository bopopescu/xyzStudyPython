# -*- coding:utf-8 -*-

from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import tensorflow as tf
from PIL import Image

# 下载或加载数据
mnist = input_data.read_data_sets("MNIST_data", one_hot=True)


def weight_variable(shape):
    inital = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(inital)


def bias_variable(shape):
    inital = tf.constant(0.1, shape=shape)
    return tf.Variable(inital)


def add_layer(inputs, in_size, out_size, activation_function=None):
    # 在生成初始参数时，随机变量(normal distribution)会比全部为0要好很多
    # 所以我们这里的weights为一个in_size行, out_size列的随机变量矩阵。
    weights = tf.Variable(tf.random_normal([in_size, out_size]))
    # biases的推荐值不为0，所以我们这里是在0向量的基础上又加了0.1
    biases = tf.Variable(tf.zeros([1, out_size]) + 0.1)
    wx_plus_b = tf.matmul(inputs, weights) + biases
    if activation_function is None:
        outputs = wx_plus_b
    else:
        outputs = activation_function(wx_plus_b)
    return outputs


def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(prediction, feed_dict={xs: v_xs, keep_drop: 1})
    correct_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(v_ys, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={xs: v_xs, ys: v_ys, keep_drop: 1})
    return result


def conv2d(x, w):
    # stride [1, x_movement, y_movement, 1]
    # Must have strides[0] = strides[4] = 1
    return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    # stride [1, x_movement, y_movement, 1]
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


xs = tf.placeholder(tf.float32, [None, 784])  # 28 * 28
ys = tf.placeholder(tf.float32, [None, 10])
keep_drop = tf.placeholder(tf.float32)
x_image = tf.reshape(xs, [-1, 28, 28, 1])
# print x_image.shape  # [n_sample, 28, 28, 1]
# conv1 layer #
w_conv1 = weight_variable([5, 5, 1, 32])  # patch 5 x 5, in size 1, out size 32
b_conv1 = bias_variable([32])
h_conv1 = tf.nn.relu(conv2d(x_image, w_conv1) + b_conv1)  # output size 28 x 28 x 32
h_pool1 = max_pool_2x2(h_conv1)  # output size 14 x 14 x 32

# conv2 layer #
w_conv2 = weight_variable([5, 5, 32, 64])  # patch 5 x 5, in size 32, out size 64
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2) + b_conv2)  # output size 14 x 14 x 64
h_pool2 = max_pool_2x2(h_conv2)  # output size 7 x 7 x 64

# func1 layer #
w_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])  # [n_sample, 7, 7 64]  -> [n_sample, 7*7*64]
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_drop)

# func2 layer #
w_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

prediction = tf.nn.softmax(tf.matmul(h_fc1_drop, w_fc2) + b_fc2)

cross_entropy = tf.reduce_mean(-tf.reduce_sum(ys * tf.log(prediction), reduction_indices=[1]))

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)


def show_image(img, conv1, pool1, conv2, pool2, h_fc1, h_fc1_drop):
    gs1 = gridspec.GridSpec(7, 64)
    plt.subplot(gs1[0, 0]); plt.axis('off'); plt.imshow(img[:, :])
    for i in range(0, 64, 2):
        plt.subplot(gs1[1, i: i + 1]); plt.axis('off'); plt.imshow(conv1[:, :, i/2])
        plt.subplot(gs1[2, i: i + 1]); plt.axis('off'); plt.imshow(pool1[:, :, i/2])
    for i in range(64):
        plt.subplot(gs1[3, i]); plt.axis('off'); plt.imshow(conv2[:, :, i])
        plt.subplot(gs1[4, i]); plt.axis('off'); plt.imshow(pool2[:, :, i])
    plt.subplot(gs1[5, :]); plt.axis('off'); plt.imshow(h_fc1[:, :])
    plt.subplot(gs1[6, :]); plt.axis('off'); plt.imshow(h_fc1_drop[:, :])
    plt.show()


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    batch_xs, batch_ys = mnist.train.next_batch(1)
    # img = Image.open('img/cnn_sample_test.jpg').convert('L').resize((28, 28))
    # img = np.asarray(img, dtype='float32') / 256.
    # img_shape = img.shape
    # batch_xs = img.reshape(1, img_shape[0] * img_shape[1])

    h_conv1_res, h_pool1_res, h_conv2_res, h_pool2_res, h_fc1_res, h_fc1_drop_res = \
        sess.run([h_conv1, h_pool1, h_conv2, h_pool2, h_fc1, h_fc1_drop],
                 feed_dict={xs: batch_xs, ys: batch_ys, keep_drop: 0.5})
    show_image(batch_xs.reshape([28, 28]),
               h_conv1_res[0, :, :, :],
               h_pool1_res[0, :, :, :],
               h_conv2_res[0, :, :, :],
               h_pool2_res[0, :, :, :],
               h_fc1_res,
               h_fc1_drop_res)
    print 1
print "end!"
