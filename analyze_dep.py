from __future__ import division, print_function
import numpy as np
import random
import matplotlib.pyplot as plt




def analyze_full(inp, out): 
	results = np.load(inp + '.npy')
	print(np.shape(results))
	c = results[:, 0]
	repeat = results[:, 1]
	err_none = np.log(results[:, 5])
	err_l1 = np.log(results[:, 7])

	print(np.min(err_none), np.max(err_none), np.min(err_l1), np.max(err_l1))

	plt.figure()
	plt.subplot(1, 2, 1)
	plt.scatter(c, repeat, c=err_none, s=1, cmap="hot", vmin=-50, vmax=0, lw=0)
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('Samples vs Temp for size 10 networks (100,000 points)')

	plt.subplot(1, 2, 2)
	plt.scatter(c, repeat, c=err_l1, s=1, cmap="hot", vmin=-50, vmax=0, lw=0)
	plt.colorbar()
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('Samples vs Temp for size 10 networks (100,000 points)')
	plt.savefig(out)

def vary_samples(inp, out): 
	results = np.load(inp + '.npy')[:-1]
	print(np.shape(results))
	print(results[-1])
	colors = ['pink', 'red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'grey', 'brown']

	plt.figure()

	err_none = np.log(results[:, 0, 2])
	plt.scatter(range(1024), err_none, s=2, c='black', lw=0, marker='o')

	err_lin = np.log(results[:, 0, 0])
	plt.scatter(range(1024), err_lin, s=2, c='grey', lw=0, marker='o')
	for i in range(8): 
		
		err_l1 = np.log(results[:, i, 3])
		print(np.shape(err_none))
		
		plt.scatter(range(1024), err_l1, s=2, c=colors[i], lw=0, marker='o')
		# plt.scatter(range(1024), err_none_l0, s=2, c='g', lw=0)
		# plt.scatter(range(1024), err_l1_l0, s=2, c='b', lw=0)
	plt.savefig(out + '_err')

	plt.xlim([0, 200])
	plt.savefig(out + '_err_zoom')

	plt.figure()
	err_none_l0 = results[:, 0, 4]
	plt.scatter(range(1024), err_none_l0, s=2, c='black', lw=0, marker='o')
	err_lin_l0 = results[:, 0, 1]
	plt.scatter(range(1024), err_lin_l0, s=2, c='grey', lw=0, marker='o')
	for i in range(8): 
		
		err_l1_l0 = results[:, i, 5]
		# plt.scatter(range(1024), err_none, s=2, c='r', lw=0, marker='o')
		# plt.scatter(range(1024), err_l1, s=2, c='b', lw=0, marker='o')
		# plt.scatter(range(1024), err_none_l0, s=2, c='r', lw=0, marker='o')
		plt.scatter(range(1024), err_l1_l0, s=2, c=colors[i], lw=0, marker='o')
	plt.savefig(out + '_err_l1')

	plt.xlim([0, 200])
	plt.savefig(out + '_err_l1_zoom')

	return

	plt.figure()
	for i in range(10): 
		err_l1 = np.log(results[:, i, 3])
		plt.scatter(range(1024), err_l1, s=2, c=colors[i], lw=0, marker='o')
		# plt.scatter(range(1024), err_none_l0, s=2, c='g', lw=0)
		# plt.scatter(range(1024), err_l1_l0, s=2, c='b', lw=0)
	plt.savefig(out + '_l1_a')

	plt.xlim([0, 200])
	plt.savefig(out + '_l1_a_zoom')

	plt.figure()
	for i in range(10): 
		err_l1 = results[:, i, 5]
		plt.scatter(range(1024), err_l1, s=2, c=colors[i], lw=0, marker='o')
		# plt.scatter(range(1024), err_none_l0, s=2, c='g', lw=0)
		# plt.scatter(range(1024), err_l1_l0, s=2, c='b', lw=0)
	plt.savefig(out + '_l1_l0_a')

	plt.xlim([0, 200])
	plt.savefig(out + '_l1_l0_a_zoom')




def main(): 
	# inp = './dep_results/rand_S' 
	inp = './dep_results/results_lin_smaller'
	out = inp
	vary_samples(inp, out)



if __name__ == '__main__':
	main()