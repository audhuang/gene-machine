import numpy as np
import time
from mitro import Simulator


def main(): 
	n = 10
	temp = 1
	repeat = 10 ** 5
	n_steps = 1000

	t = time.time()

	# pool = mp.Pool()
	# results = [pool.apply_async(vary_samples2, args=(x, n, params[x, 0], params[x, 1])) for x in range(len(params))]
	# output = [p.get() for p in results]


	# for i in range(repeat): 
	# 	J = np.random.normal(0, 1, [n, n])
	# 	metro = Simulator(n, temp, J)
	# 	# metro.print_lattice()
	# 	metro.simulate_new(n_steps)
	# 	# metro.print_lattice()
	# 	if i % 10**4 == 0: 
	# 		print i

	counts = np.zeros([2**n])

	metro = Simulator(n, temp)
	for i in range(repeat): 
		metro.simulate_new(n_steps)
		metro.init_J_random()
		state = metro.bin_to_int()
		counts[state] += 1
	
		if i % 10000 == 0: 
			print 'iter ', i, ': ', state

	# metro.run(repeat, n_steps)
	print time.time() - t
	print counts
	


if __name__ == '__main__':
 	main()

