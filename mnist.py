from __future__ import division, print_function
import numpy as np
import random
import sklearn 
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import scipy.io
from keras.utils import np_utils
from keras.datasets import mnist
from keras import backend as K
from boltzmann import solve



def main(): 
	(x_train, y_train), (x_test, y_test) = mnist.load_data()
	inp_dim = x_train.shape[1] * x_train.shape[2]
	x_train = x_train.reshape(x_train.shape[0], 28*28).astype('float32')
	x_test = x_test.reshape(x_test.shape[0], 28*28).astype('float32')

	indices = np.where(y_train < 2)
	ytrain_bin = np.take(y_train, indices)[0]
	xtrain_bin = np.take(x_train, indices, axis=0)[0]
	xtrain_bin = xtrain_bin / 255

	indices = np.where(y_test < 2)
	ytest_bin = np.take(y_test, indices)[0]
	xtest_bin = np.take(x_test, indices, axis=0)[0]
	xtest_bin = xtest_bin / 255

	print(np.shape(xtrain_bin), np.shape(ytrain_bin), np.shape(xtest_bin), np.shape(ytest_bin))

	clf = LogisticRegression()
	clf.fit(xtrain_bin, ytrain_bin)
	score_train = clf.score(xtrain_bin, ytrain_bin)
	score_test = clf.score(xtest_bin, ytest_bin)

	print(score_train, score_test)

	prob = clf.predict_proba(xtrain_bin)
	prob_1 = prob[:, 1]

	J = solve(xtrain_bin, prob_1)
	print(np.shape(J))

	prob_hat = np.dot(xtrain_bin, J)
	print(np.shape(prob_hat))

	print(np.linalg.norm(prob_hat-prob_1) / len(J))

	pred = prob_hat > 10**-3
	print(np.sum(pred != ytrain_bin)/len(pred))







	



if __name__ == '__main__':
	main()


