from __future__ import division, print_function
import numpy as np
import random 


it = 10
repeat = 100
n = 5
c = 1
threshold = 1.

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


# fix matrix dE
# set to high energy


def random_network(n, mu = 0., sigma = 1.): 
	random = np.random.normal(mu, sigma, [n, n])
	network = np.tril(random) + np.tril(random, -1).T
	np.fill_diagonal(network, 0)
	return network

def energy(x, J, h):
	e = np.dot(np.dot(x, J), np.transpose(x)) + np.dot(x, np.transpose(h)) 
	return e 

def acceptance(x_new, x_cur, J, h, c): 
	e_new = energy(x_new, J, h)
	e_cur = energy(x_cur, J, h)
	p_ratio = np.exp(-(e_new - e_cur) / c)
	return min(1, p_ratio), e_new


def energy_all(x_all, J, h, c): 
	energies = np.zeros([2**n])
	for i in range(2**n): 
		energies[i] = energy(x_all[i], J, h)
	return energies

def boltz(n, J, h, c): 
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


def x_to_states(x_array): 
	x = ((x_array + 1) / 2).astype(int)
	# print('x: ', x)
	states = np.zeros([2**n])

	for i in range(repeat): 
		state = ''.join(list(x[i].astype(str)))
		dec = bin_to_int[state]
		# print(state, dec)
		states[dec] += 1
	return states

def states_to_dE(states): 
	dE = np.zeros([2**n, 2**n])
	for i in range(2**n): 
		for j in range(2**n): 
			if states[j] == 0: 
				dE[i, j] = 0
			else: 
				dE[i, j] = states[i] / states[j] 
	
	dE = -c * np.log(dE)
	return dE
	# what did we do again if there was zero in state count?

def states_to_dE_one(states): 
	dE = np.zeros([2 ** n])
	S = np.zeros([2 ** n, n, n])
	base = np.argmax(states)
	base_count = states[base]
	for i in range(2 ** n): 
		count = states[i]
		if count > threshold: 
			dE[i] = states[i] / base_count
		else: 
			dE[i] = 0.00001
		S[i] = np.transpose(np.outer(x_all[i], x_all[i]) - np.outer(x_all[base], x_all[base]))


	print('dE": ', dE)
	dE = -c * np.log(dE)
	return dE, S




def xall_to_S(x_all): 
	S = np.zeros([2**n, 2**n, n, n])
	for i in range(2**n): 
		for j in range(2**n): 
			prod = np.outer(x_all[i], x_all[i]) - np.outer(x_all[j], x_all[j])
			S[i, j] = prod
	return S


def solve(S, dE):
	inv = np.linalg.pinv(S)
	return np.dot(np.linalg.pinv(S), dE) 

def solve_l1(S, dE): 
	return 


def error(true, pred, n): 
	return np.sum(np.abs(true - pred)) / n



def main(): 
	J = random_network(n)
	h = np.zeros([n])
	energies = energy_all(x_all, J, h, c)
	print('energies: ', energies)
	x_array, e_array = boltz(n, J, h, c)
	# print('x array:', x_array)
	# print('e array:', e_array)
	states = x_to_states(x_array)
	# states = [0., 47., 41., ]
	print('states: ', states)
	dE, S = states_to_dE_one(states)
	print('dE: ', dE)
	# print(S)

	S_flat = S.reshape([2**n, n**2])
	dE_flat = dE


	J_hat = solve(S_flat, dE_flat)
	J_hat = J_hat.reshape([n, n])
	print('J": ', J_hat)
	print('J: ', J)

	err = error(J, J_hat, n)
	print('error: ', err)


# l1 penalty	
# optimal temperature for runs 

'''
notes


'''

if __name__ == '__main__':
	main()





