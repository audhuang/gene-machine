from __future__ import division, print_function
import numpy as np
import random 
from sklearn.linear_model import Lasso
from numpy.linalg import matrix_rank



def random_network(n, mu = 0., sigma = 1.): 
	random = np.random.normal(mu, sigma, [n, n])
	network = np.tril(random) + np.tril(random, -1).T
	np.fill_diagonal(network, 0)
	return network

def sparse_random_network(n, perc, mu = 0., sigma = 1.): 
	num = int(np.ceil(n**2 * perc)) 
	random = np.random.normal(mu, sigma, [n, n])
	indices = np.random.choice(range(n**2), num, replace=False)
	for i in range(num): 
		index = indices[i]
		x = int(np.floor(index / n)) 
		y = index % n
		random[x, y] = 0

	network = np.tril(random) + np.tril(random, -1).T
	np.fill_diagonal(network, 0)
	return network

def sparse_num_network(n, number, mu = 0., sigma = 1.): 
	num = int(number / 2 - n)
	if num < 0: 
		num = 0
	m = int(n * (n-1) / 2)
	random = np.random.normal(mu, sigma, [m])
	# print(random)
	indices = np.random.choice(range(m), num, replace=False)
	for i in range(num): 
		random[indices[i]] = 0
	# print(random)
	
	temp = np.zeros([n, n])
	temp[np.tril_indices(n, -1)] = random
	# print(temp)

	network = temp + temp.T
	# print(network)
	np.fill_diagonal(network, 0)
	return network

def sparse_rand(n, num, mu = 0., sigma = 1.): 
	random = np.random.normal(mu, sigma, [n**2])
	if num == 0: 
		return random
	else: 
		indices = np.random.choice(range(n**2), num, replace=False)
		for i in range(num): 
			random[indices[i]] = 0
		return random

# check the math here
def energy(x, J, h):
	# print(np.sum(np.dot(J, np.outer(x, x))))
	# print(np.dot(np.dot(x, J), np.transpose(x)))
	e = np.dot(np.dot(x, J), np.transpose(x)) + np.dot(x, np.transpose(h)) 
	return e 


def acceptance(x_new, x_cur, J, h, c): 
	e_new = energy(x_new, J, h)
	e_cur = energy(x_cur, J, h)
	p_ratio = np.exp(-(e_new - e_cur) / c)
	return min(1, p_ratio), e_new


def energy_all(x_all, J, h, c, n): 
	energies = np.zeros([2**n])
	for i in range(2**n): 
		energies[i] = energy(x_all[i], J, h)
	return energies

def boltz(J, h, c, n, it, repeat): 
	# J_true = random_network(n)
	# J = np.random.normal(mu, sigma, [n, n])
	# h = np.zeros([1, n])

	x_array = np.zeros([repeat, n])
	e_array = np.zeros([repeat])

	for i in range(repeat): 
		x_0 = 2 * np.random.binomial(1, 0.5, [n]) - 1
		x_cur = x_0
		e_cur = energy(x_0, J, h)

		for j in range(it): 

			x_new = x_cur.copy() 
			flip_index = np.random.randint(n)
			x_new[flip_index] = -1 * x_cur[flip_index] 

			a, e_new = acceptance(x_new, x_cur, J, h, c)
			q = np.random.uniform(0., 1.)

			if q <= a: 
				x_cur = x_new
				e_cur = e_new
		x_array[i] = x_cur
		e_array[i] = e_cur
	
	return x_array, e_array


def prob_dist(J, h, c, n, x_all, energies, repeat):
	p = np.exp(-energies / c)
	# print('p: ', p)
	Z = np.sum(p)
	probabilities = p / Z
	# print('probabilities: ', probabilities)

	indices = np.random.choice(range(2**n), repeat, replace=True, p=probabilities)
	# print(indices[:10])
	x_array = np.take(x_all, indices, axis=0)
	e_array = np.take(energies, indices)
	return x_array, e_array


def x_to_states(x_array, n, repeat, bin_to_int): 
	x = ((x_array + 1) / 2).astype(int)
	# print('x: ', x)
	states = np.zeros([2**n])

	for i in range(repeat): 
		state = ''.join(list(x[i].astype(str)))
		dec = bin_to_int[state]
		# print(state, dec)
		states[dec] += 1
	return states

def states_to_dE(states, x_all, n, threshold, c): 
	dE = np.zeros([2 ** n])
	S = np.zeros([2 ** n, n, n])
	base = np.argmax(states)
	base_count = states[base]
	zero_states = np.zeros([2 ** n])

	for i in range(2**n): 
		count = states[i]
		if count > threshold: 
			zero_states[i] = 1
			dE[i] = count / base_count
			S[i] = np.transpose(np.outer(x_all[i], x_all[i]) - np.outer(x_all[base], x_all[base]))
			# print(x_all[i])
	
	# print(S)
	indices = np.where(dE != 0)

	dE = np.take(dE, indices)[0]
	S = np.take(S, indices, axis=0)[0]

	dE = -c * np.log(dE)
	return dE, S, zero_states

def states_to_dE_one(states, x_all, n, threshold, c): 
	dE = np.zeros([2 ** n])
	S = np.zeros([2 ** n, n, n])
	base = np.argmax(states)
	base_count = states[base]
	for i in range(2 ** n): 
		count = states[i]
		if count > threshold: 
			dE[i] = count / base_count
		else: 
			dE[i] = 0.000001
		S[i] = np.transpose(np.outer(x_all[i], x_all[i]) - np.outer(x_all[base], x_all[base]))

	dE = -c * np.log(dE)
	return dE, S




def xall_to_S(x_all, n): 
	S = np.zeros([2**n, 2**n, n, n])
	for i in range(2**n): 
		for j in range(2**n): 
			prod = np.outer(x_all[i], x_all[i]) - np.outer(x_all[j], x_all[j])
			S[i, j] = prod
	return S


def solve(S, dE):
	inv = np.linalg.pinv(S)
	return np.dot(np.linalg.pinv(S), dE) 

def solve_l1(S, dE, a): 
	clf = Lasso(alpha=a, fit_intercept=False, tol=0.0001, max_iter=10**6)
	clf.fit(S, dE)
	return clf.coef_


def error(true, pred, n): 
	return np.sum(np.abs(true - pred)) / n**2

def error_l0(true, pred, n, thresh): 
	temp = np.abs(true - pred)
	return np.sum(temp < thresh) / n**2






def main(): 
	it = 100
	repeat = 1000
	n = 5
	c = 1.
	threshold = 10.

	bin_to_int = {}
	int_to_bin = {}
	x_all = np.zeros([2**n, n])
	bin = np.zeros([n])
	for i in range(2 ** n): 
		temp = "{0:b}".format(i)
		bin = '0' * (n - len(temp)) + temp
		bin_to_int[bin] = i
		int_to_bin[i] = bin
		x_all[i] = list(bin)
	x_all = x_all * 2 - 1


	J = sparse_random_network(n, 0.75)
	# J = random_network(n)
	h = np.zeros([n])

	# x_array, e_array = boltz(J, h, c, n, it, repeat)
	# st = x_to_states(x_array, n, repeat, bin_to_int)
	# print('st: ', st)
	

	energies = energy_all(x_all, J, h, c, n)
	print('energies: ', energies)
	x_array, e_array = prob_dist(J, h, c, n, x_all, energies, repeat)

	states = x_to_states(x_array, n, repeat, bin_to_int)
	print('states: ', states)
	
	dE, S, zero_states = states_to_dE(states, x_all, n, threshold, c)
	# dE, S = states_to_dE_one(states, x_all, n, threshold, c)
	print('dE: ', dE)
	print('zero states: ', zero_states)

	S_flat = S.reshape([len(dE), n**2])
	dE_flat = dE


	J_hat = solve_l1(S_flat, dE_flat, 0.1)
	# J_hat = solve(S_flat, dE_flat)
	J_hat = J_hat.reshape([n, n])
	print('J": ', J_hat)
	print('J: ', J)

	err = error_l0(J, J_hat, n, thresh = 10. ** -4)
	print('error: ', err)

	print(matrix_rank(dE_flat), matrix_rank(J), matrix_rank(J_hat))

# l1 penalty	
# optimal temperature for runs 

'''
notes


'''

if __name__ == '__main__':
	main()





