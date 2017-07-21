import numpy as np
import time
import multiprocessing as mp
from mitro import Simulator

def run(i, n, temp, n_steps): 
	metro = Simulator(n, temp)
	metro.simulate_new(n_steps)
	state = metro.bin_to_int()

	if i % 10000 == 0: 
		print i, state
	return state 


def main(): 
	n = 10
	temp = 1
	repeat = 10 ** 5
	n_steps = 1000

	t = time.time()

	# pool = mp.Pool()
	# results = [pool.apply_async(run, args=(x, n, temp, n_steps)) for x in range(repeat)]
	# output = [p.get() for p in results]
	# print(np.shape(output))
	# print(output[:10])

	metro = Simulator(n, temp)
	counts = np.asarray(metro.run(repeat, n_steps))

	# counts = np.zeros([2**n])

	# metro = Simulator(n, temp)
	# for i in range(repeat): 
	# 	metro.simulate_new(n_steps)
	# 	# metro.init_J_random()
	# 	state = metro.bin_to_int()
	# 	counts[state] += 1
	
	# 	if i % 10000 == 0: 
	# 		print 'iter ', i, ': ', state

	# metro.run(repeat, n_steps)
	print time.time() - t
	# print counts



if __name__ == '__main__':
 	main()

