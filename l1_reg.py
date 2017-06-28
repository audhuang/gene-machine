from __future__ import division, print_function
import random 
import multiprocessing as mp
from boltzmann import *
from numpy.linalg import matrix_rank

a = 1
l0_thresh = 10.**-3

'''
if n_dE = 2, J_hat becomes 0 

at c = -0.5, m = 10k, rank(J) = 2, n_dE = 32
rank(none) = 5 and rank(L1) = 0
error ~0.05
setting all zero is basically the same as a shitty full-rank matrix
all the values in the normal solution are already close to zero 
'''

def run_none_l1(i, n, low, high, x_all, bin_to_int, threshold=10.): 
	c_ = np.random.uniform(low, high)
	c = 10. ** c_
	repeat = np.random.randint(100, 10**5)

	# J = random_network(n)
	J = sparse_random_network(n, 0.75, 0, 1.)
	while np.sum(abs(J)) == 0: 
		J = sparse_random_network(n, 0.75, 0, 1.)
	h = np.zeros([n])

	energies = energy_all(x_all, J, h, c, n)
	
	x_array, e_array = prob_dist(J, h, c, n, x_all, energies, repeat)
	
	states = x_to_states(x_array, n, repeat, bin_to_int)
	
	dE, S, zero_states = states_to_dE(states, x_all, n, threshold, c)

	dE_rank = len(dE)
	J_rank = matrix_rank(J)

	if dE_rank == 0: 
		J_none = np.zeros([n, n])
		J_l1 = J_none
	else: 
		S_flat = S.reshape([dE_rank, n**2])
		dE_flat = dE

		J_none = solve(S_flat, dE_flat)
		J_none = J_none.reshape([n, n])
		
		J_l1 = solve_l1(S_flat, dE_flat, a)
		J_l1 = J_l1.reshape([n, n])
	
	err_none = error_l0(J, J_none, n, l0_thresh)
	Jnone_rank = matrix_rank(J_none)

	err_l1 = error_l0(J, J_l1, n, l0_thresh)
	Jl1_rank = matrix_rank(J_l1)

	if i % 1000 == 0:
		print('run: ', i, c_, repeat, J_rank, dE_rank, err_none, Jnone_rank, err_l1, Jl1_rank)
		
	
	return (c_, repeat, J_rank, dE_rank, err_none, Jnone_rank, err_l1, Jl1_rank)



def run_1(n, number, low, high, threshold, out): 
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

	pool = mp.Pool()
	results = [pool.apply_async(run_none_l1, args=(x, n, low, high, x_all, bin_to_int)) for x in range(number)]
	output = [p.get() for p in results]

	np.save(out + 'none_l1_5_10_l0err_' + str(a), output)



def run_temp_err(i, n, c_, repeat, x_all, bin_to_int, threshold=10.): 
	c = 10. ** c_
	J = sparse_random_network(n, 0.75, 0, 1.)
	h = np.zeros([n])

	energies = energy_all(x_all, J, h, c, n)
	
	x_array, e_array = prob_dist(J, h, c, n, x_all, energies, repeat)
	
	states = x_to_states(x_array, n, repeat, bin_to_int)
	
	dE, S, zero_states = states_to_dE(states, x_all, n, threshold, c)

	dE_rank = len(dE)
	J_rank = matrix_rank(J)

	if dE_rank == 0: 
		J_none = np.zeros([n, n])
		J_l1 = J_none
	else: 
		S_flat = S.reshape([dE_rank, n**2])
		dE_flat = dE

		J_none = solve(S_flat, dE_flat)
		J_none = J_none.reshape([n, n])
		
		J_l1 = solve_l1(S_flat, dE_flat, a)
		J_l1 = J_l1.reshape([n, n])
	
	err_none = error(J, J_none, n)
	Jnone_rank = matrix_rank(J_none)

	err_l1 = error(J, J_l1, n)
	Jl1_rank = matrix_rank(J_l1)

	if i % 20 == 0:
		print('run: ', c_, repeat, J_rank, dE_rank, err_none, Jnone_rank, err_l1, Jl1_rank)
	
	return (c_, repeat, J_rank, dE_rank, err_none, Jnone_rank, err_l1, Jl1_rank)



def run_2(n, repeat, mult, low, high, bins, threshold, out): 
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

	clist_temp = np.linspace(low, high, num=bins)
	c_list = np.zeros([mult * bins])
	for i in range(bins): 
		c_list[i*mult:(i+1)*mult] = clist_temp[i]
	# print('clist: ', c_list)

	number = len(c_list)
	pool = mp.Pool()
	results = [pool.apply_async(run_temp_err, args=(x, n, c_list[x], repeat, x_all, bin_to_int)) for x in range(number)]
	output = [p.get() for p in results]

	np.save(out + 'temp_err_' + str(mult) + '_' + str(bins) + '_' + str(a), output)






def main(): 
	n = 10
	number = 10**5
	low = -1
	high = 4
	threshold = 10.
	output = './l1_results/'
	run_1(n, number, low, high, threshold, output)

	# repeat = 10 ** 4
	# bins = 50
	# mult = 20
	# run_2(n, repeat, mult, low, high, bins, threshold, output)



if __name__ == '__main__':
	main()

