import random 
import multiprocessing as mp
from boltzmann import *




def run(i, n, low, high, x_all, bin_to_int, threshold=10.): 
	c_ = np.random.uniform(low, high)
	c = 10. ** c_
	repeat = np.random.randint(100, 10**5)

	# J = random_network(n)
	J = sparse_random_network(n, 0.75)
	h = np.zeros([n])

	energies = energy_all(x_all, J, h, c, n)
	
	x_array, e_array = prob_dist(J, h, c, n, x_all, energies, repeat)
	
	states = x_to_states(x_array, n, repeat, bin_to_int)
	
	dE, S = states_to_dE_one(states, x_all, n, threshold, c)

	S_flat = S.reshape([2**n, n**2])
	dE_flat = dE

	# J_hat = solve_l1(S_flat, dE_flat, 2.)
	J_hat = solve(S_flat, dE_flat)
	J_hat = J_hat.reshape([n, n])
	
	err = error(J, J_hat, n)

	if i % 1000 == 0: 
		print('run: ', i, c, repeat, err)
		# np.save(out + 'err_repeat_temp', errors)
	
	return (c_, repeat, err)



def run_repeat_temp(n, number, low, high, threshold, out): 
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
	results = [pool.apply_async(run, args=(x, n, low, high, x_all, bin_to_int)) for x in range(number)]
	output = [p.get() for p in results]

	np.save(out + 'repeat_temp_sparse', output)

	# print(output)
	# np.save(out + 'err_repeat_temp', results)
	# print(errors)






def main(): 
	return 


if __name__ == '__main__':
	main()

