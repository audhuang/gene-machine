from __future__ import division, print_function
import numpy as np
import random
import matplotlib.pyplot as plt

n = 10
num_sparse = 20

def phase_graph(inp, out): 
	results = np.load(inp + '.npy')
	print(np.shape(results))
	results = results.reshape([num_sparse * n**2, 4])
	print(np.shape(results))

	delta = results[:, 0]
	nu = results[:, 1]
	err_none = np.log(results[:, 2])
	err_l1 = np.log(results[:, 3])
	# print(results[:, 3])
	# print(np.min(err_l1), np.max(err_none))

	plt.figure()
	plt.scatter(delta, nu, c=err_none, s=10, cmap="viridis", vmin=-10, vmax=0, lw=0)
	plt.colorbar()
	plt.xlabel('delta')
	plt.ylabel('nu')
	plt.title('phase least squares')
	plt.xlim([0, 1])
	plt.ylim([0, 1])
	plt.savefig(out + '_none')

	plt.figure()
	plt.scatter(delta, nu, c=err_l1, s=10, cmap="viridis", vmin=-10, vmax=0, lw=0)
	plt.colorbar()
	plt.xlabel('delta')
	plt.ylabel('nu')
	plt.title('phase lasso')
	plt.xlim([0, 1])
	plt.ylim([0, 1])
	plt.savefig(out + '_l1')



def main(): 
	inp = './phase_results/phase_10'
	out = inp
	phase_graph(inp, out)


if __name__ == '__main__':
	main()


