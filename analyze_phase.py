from __future__ import division, print_function
import numpy as np
import random
import matplotlib.pyplot as plt
from boltzmann import solve

n = 10
num_sparse = 20

def phase_graph(inp, out): 
	results = np.load(inp + '.npy')
	print(np.shape(results))

	graph_dict = {}

	q = results[:, 0].astype(int)
	i = results[:, 1].astype(int)
	err_none = results[:, 4]
	err_l1 = results[:, 5]

	
	delta = i / n**2
	nu = np.divide(q, i) 
	
	for j in range(len(delta)): 
		key = str(q[j]) + '_' + str(i[j])
		if key not in graph_dict: 
			graph_dict[key] = [0, 0]
		if err_l1[j] < 0.1:
			graph_dict[key][0] += 1
		graph_dict[key][1] += 1 

	err = np.zeros(len(q))
	x = np.zeros(len(q))
	y = np.zeros(len(q))
	count = 0
	for key in graph_dict.keys():
		lel = key.split('_')
		xlel = int(lel[0])
		ylel = int(lel[1])
		x[count] = ylel / n**2
		y[count] = xlel / ylel
		err[count] = graph_dict[key][0] / graph_dict[key][1]
		count += 1
	print(xlel, ylel)




	


	plt.figure()
	plt.scatter(x, y, c=err, s=10, cmap="jet", vmin=0, vmax=1, lw=0)
	plt.colorbar()
	plt.xlabel('delta')
	plt.ylabel('nu')
	plt.title('phase least squares')
	plt.xlim([0, 1])
	plt.ylim([0, 1])
	plt.savefig(out + '_graph')






	# plt.figure()
	# plt.scatter(delta, nu, c=err_none, s=1, cmap="jet", vmin=0, vmax=1)
	# plt.colorbar()
	# plt.xlabel('delta')
	# plt.ylabel('nu')
	# plt.title('phase least squares')
	# plt.xlim([0, 1])
	# plt.ylim([0, 1])
	# plt.savefig(out + '_none')

	# plt.figure()
	# plt.scatter(delta, nu, c=err_l1, s=1, cmap="jet", vmin=0, vmax=1)
	# plt.colorbar()
	# plt.xlabel('delta')
	# plt.ylabel('nu')
	# plt.title('phase lasso')
	# plt.xlim([0, 1])
	# plt.ylim([0, 1])
	# plt.savefig(out + '_l1')



def main(): 
	inp = './phase_results/phase_l0_5_2'
	out = inp
	phase_graph(inp, out)


if __name__ == '__main__':
	main()


