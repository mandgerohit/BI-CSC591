
import tensorflow as tf
import numpy as np

# loading Boston Database
from sklearn.datasets import load_boston

boston = load_boston()

data = boston.data
target = boston.target
datalen = len(data)

trlen = int(0.7 * datalen)

trX = tf.cast(data[0:trlen], tf.float32)
trY = tf.cast(target[0:trlen], tf.float32)
trY = tf.reshape(trY, [trlen,1])

tsX = tf.cast(data[trlen:], tf.float32)
tsY = tf.cast(target[trlen:], tf.float32)
tsY = tf.reshape(tsY, [datalen - trlen,1])

x = tf.placeholder(tf.float32, [None, 13])
W = tf.Variable(tf.random_normal([13,1], mean=0.0, stddev=0.35, dtype=tf.float32))
b = tf.Variable(tf.zeros([1]))

y = tf.add(tf.matmul(x, W), b)
y_ = tf.placeholder(tf.float32, [None, 1])

# find the cost
cost = tf.square(y - y_)

train_op = tf.train.GradientDescentOptimizer(1e-8).minimize(cost)

sess = tf.Session()
init = tf.initialize_all_variables()
sess.run(init)

for i in range(200):
    sess.run(train_op, feed_dict={x: trX.eval(session=sess), y_: trY.eval(session=sess)})

# find mean square error
mse = tf.reduce_sum(tf.pow(y - y_, 2))/(datalen - trlen)

# print the data
print sess.run(mse, feed_dict={x: tsX.eval(session=sess), y_: tsY.eval(session=sess)})

