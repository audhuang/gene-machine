from __future__ import division, print_function
import random 
import multiprocessing as mp
from boltzmann import *
from numpy.linalg import matrix_rank

'''
if n_dE = 2, J_hat becomes 0 

at c = -0.5, m = 10k, rank(J) = 2, n_dE = 32
rank(none) = 5 and rank(L1) = 0
error ~0.05
setting all zero is basically the same as a shitty full-rank matrix
all the values in the normal solution are already close to zero 
'''

def run_all(i, n, c_, repeat, x_all, bin_to_int, threshold=10.): 
	# c_ = np.random.uniform(low, high)
	c = 10. ** c_
	# repeat = np.random.randint(100, 10**5)

	# J = random_network(n)
	J = sparse_random_network(n, 0.75, 0, 1.)

	h = np.zeros([n])

	energies = energy_all(x_all, J, h, c, n)
	
	x_array, e_array = prob_dist(J, h, c, n, x_all, energies, repeat)
	
	states = x_to_states(x_array, n, repeat, bin_to_int)
	
	dE, S, zero_states = states_to_dE(states, x_all, n, threshold, c)
	# print(dE)
	dE_rank = len(dE)
	if dE_rank == 0: 
		J_hat = np.zeros([n, n])
	else: 
		J_rank = matrix_rank(J)
		print(J)
		print('RUN: ', c_, repeat, J_rank, dE_rank)
		S_flat = S.reshape([dE_rank, n**2])
		dE_flat = dE

		# J_hat = solve_l1(S_flat, dE_flat, 1.)
		J_hat = solve(S_flat, dE_flat)
		J_hat = J_hat.reshape([n, n])
		err = error(J, J_hat, n)
		Jhat_rank = matrix_rank(J_hat)
		print(J_hat)
		print('none: ', err, Jhat_rank)

		J_hat = solve_l1(S_flat, dE_flat, 0.5)
		J_hat = J_hat.reshape([n, n])
		err = error(J, J_hat, n)
		Jhat_rank = matrix_rank(J_hat)
		print(J_hat)
		print('L1: ', err, Jhat_rank)
	
	# return (c_, repeat, err, J_rank, Jhat_rank, dE_rank)



def run_test(n, c, repeat, threshold, out): 
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

	run_all(n, c, repeat, x_all, bin_to_int)

	# np.save(out + 'repeat_temp_5_old', output)

	# print(output)
	# np.save(out + 'err_repeat_temp', results)
	# print(errors)



def run_all(i, n, low, high, x_all, bin_to_int, threshold=10.):
	c_ = np.random.uniform(low, high)
	c = 10. ** c_
	repeat = np.random.randint(100, 10**5)

	J = sparse_random_network(n, 0.75, 0, 1.)



def main(): 
	n = 6 
	number = 1
	c = 1.
	repeat = 10 ** 4
	threshold = 10.
	output = './l1reg/'
	run_test(n, c, repeat, threshold, output)



if __name__ == '__main__':
	main()

