import numpy as np
import time
import multiprocessing as mp
from mitro import Simulator

def mp_run(i, n, temp, n_steps): 
	metro = Simulator(n, temp)
	metro.simulate_new(n_steps)
	state = metro.bin_to_int()

	if i % 10000 == 0: 
		print i, state
	return state 

def run(n, temp, repeat, n_steps): 
	indices = {}
	states = np.zeros([n, n])
	counts = np.zeros([n])
	total = n
	index = 0
	pad_2D = np.zeros([n, n])
	pad_1D = np.zeros([n])
	t = time.time()

	metro = Simulator(n, temp)
	for i in range(repeat): 
		metro.simulate_new(n_steps)
		state = metro.get_lattice()
		# state_string = ''.join([str((state[i] + 1) / 2) for i in range(n)])
		state_string = metro.get_lattice_string()
		
		if state_string not in indices: 
			indices[state_string] = index
			index += 1
		states[indices[state_string]] = state
		counts[indices[state_string]] += 1

		if index >= total: 
			states = np.append(states, pad_2D, axis=0)
			counts = np.append(counts, pad_1D, axis=0)
			total += n

	print 'time elapsed: ', time.time() - t
	print '# unique states: ', len(indices.keys())
	return states[:index, :], counts[:index]



def main(): 
	'''
	parameters

		n - network size
		temp - temperature
		repeat - number of runs
		n_steps - number of simulations steps per run

	'''
	n = 100 
	temp = 2
	repeat = 10**5
	n_steps = 1000

	states, counts = run(n, temp, repeat, n_steps)



	# pool = mp.Pool()
	# results = [pool.apply_async(run, args=(x, n, temp, n_steps)) for x in range(repeat)]
	# output = [p.get() for p in results]
	# print(np.shape(output))
	# print(output[:10])


	metro = Simulator(n, temp)
	
	# for i in range(repeat): 
	# 	metro.simulate_new(n_steps) 
	# 	state = metro.bin_to_int()
	# 	# print(i, state)
	# 	if state[0] not in counts: 
	# 		counts[state[0]] = {}
	# 	if state[1] not in counts[state[0]]: 
	# 		counts[state[0]][state[1]] = 0

	# 	counts[state[0]][state[1]] += 1

	
		# state_string = ''.join([str((state[i] + 1) / 2) for i in range(n)])
		# if state_string not in indices_new: 
		# 	indices_new[state_string] = count_new
		# 	count_new += 1
		# states_new[indices_new[state_string]] = state
		# dE_new[indices_new[state_string]] += 1


	
	
	# metro.run(repeat, n_steps)
	
	# print counts_all
	# print(indices)





if __name__ == '__main__':
 	main()

