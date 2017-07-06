from __future__ import division, print_function
import random 
import multiprocessing as mp
from boltzmann import *
from numpy.linalg import matrix_rank


thresh = 10**-4
mu = 0.
sigma = 1.

def get_full_S(x_all, n): 
	S = np.zeros([2 ** n, n, n])
	base = np.random.randint(0, 2**n)
	for i in range(2**n): 
		S[i] = np.transpose(np.outer(x_all[i], x_all[i]) - np.outer(x_all[base], x_all[base]))
	return S

def get_random_S(n): 
	return np.random.normal(mu, sigma, [2**n, n**2])

def get_bin_S(n): 
	x = np.random.binomial(1, 0.5, [2**n, n**2])
	x = x * 2 - 1
	return x


def vary_samples(n, J, S_flat, out): 
	results = np.zeros([2**n+1, 10, 6])
	count = 0

	alist = [4 * 10**-5, 0.0002, 0.001, 0.005, 0.025, 0.125, 0.125*5, 0.125*25]
	# alist = np.zeros([10])
	# alist[0] = 0.1
	# for i in range(1, 10): 
	# 	alist[i] = alist[i-1] + 0.5

	for a in alist: 
		print('a: ', a)
		for i in range(1, 2**n+1): 
			indices = np.random.choice(2**n, i)


			S = np.take(S_flat, indices, axis=0)

			dE = np.dot(S, J)
			dE_rank = len(dE)

			J_none = solve(S, dE)
			err_none = error(J, J_none, n)
			# Jnone_rank = matrix_rank(J_none)

			J_l1 = solve_l1(S, dE, a)
			err_l1 = error(J, J_l1, n)
			# Jl1_rank = matrix_rank(J_l1)

			J_lin = solve_lin(S, dE)
			err_lin = error(J, J_lin, n)

			err_none_l0 = error_l0(J, J_none, n, thresh)

			err_l1_l0 = error_l0(J, J_l1, n, thresh)

			err_lin_l0 = error_l0(J, J_lin, n, thresh)

			results[i-1, count] = np.asarray([err_lin, err_lin_l0, err_none, err_l1, err_none_l0, err_l1_l0])
		count += 1

	np.save(out + 'results_25', results)

	

	# 	J_none = solve(S_flat, dE_flat)
	# 	J_none = J_none.reshape([n, n])
		
	# 	J_l1 = solve(S_flat, dE_flat)
	# 	J_l1 = J_l1.reshape([n, n])

	# err_none = error(J, J_none, n)
	# Jnone_rank = matrix_rank(J_none)

	# err_l1 = error(J, J_l1, n)
	# Jl1_rank = matrix_rank(J_l1)

	# # print(c_, repeat, matrix_rank(S_flat), dE_rank, err_none, err_l1, Jnone_rank, Jl1_rank)

	# if i % 1000 == 0:
	# 	# print('run: ', i, c_, repeat, J_rank, dE_rank, err_none, Jnone_rank, err_l1, Jl1_rank)
	# 	print(i, c_, repeat, J_rank, dE_rank, S_rank, err_none, Jnone_rank, err_l1, Jl1_rank)
	
	# return (c_, repeat, J_rank, dE_rank, S_rank, err_none, Jnone_rank, err_l1, Jl1_rank)


def run(n, out): 
	# bin_to_int = {}
	# int_to_bin = {}
	# x_all = np.zeros([2**n, n])
	# bin = np.zeros([n])
	# for i in range(2 ** n): 
	# 	temp = "{0:b}".format(i)
	# 	bin = '0' * (n - len(temp)) + temp
	# 	bin_to_int[bin] = i
	# 	int_to_bin[i] = bin
	# 	x_all[i] = list(bin)
	# x_all = x_all * 2 - 1

	J = sparse_random_network(n, 0.75, 0, 1.)
	while np.sum(abs(J)) == 0: 
		J = sparse_random_network(n, 0.75, 0, 1.)
	J_flat = J.reshape([n**2])
	h = np.zeros([n])
	J_rank = matrix_rank(J)
	
	S = get_random_S(n)
	# S = get_full_S(x_all, n)
	# S = get_bin_S(n)
	S_flat = S.reshape([2**n, n**2])

	vary_samples(n, J_flat, S_flat, out)

	# pool = mp.Pool()
	# results = [pool.apply_async(full_S, args=(x, n, low, high, x_all, bin_to_int)) for x in range(number)]
	# output = [p.get() for p in results]

	# np.save(out + 'rand_S', output)


def main(): 
	n = 25
	number = 1
	low = -1
	high = 4
	threshold = 10.
	output = './dep_results/'
	run(n, output)
	

if __name__ == '__main__':
	main()