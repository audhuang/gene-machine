from __future__ import division, print_function
import numpy as np
import random
import matplotlib.pyplot as plt
from boltzmann import *

n = 10
num_sparse = 20
thresh = 10**-1

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




def phase_new(inp, out): 
	results = np.load(inp + '.npy')
	J = results[:, :n**2]
	J_none = results[:, n**2:2*n**2]
	J_l1 = results[:, 2*n**2:]

	m = len(J)

	err_none = np.zeros([m])
	err_l1 = np.zeros([m])

	for i in range(m): 
		err_none[i] = np.linalg.norm(J[i] - J_none[i])
		err_l1[i] = np.linalg.norm(J[i] - J_l1[i])

		# err_none[i] = error_l0(J[i], J_none[i], n, thresh)
		# err_l1[i] = error_l0(J[i], J_l1[i], n, thresh)

	print(err_l1)

	n_x = 25
	n_y = 25
	n_all = 50

	xlist = np.linspace(1, 100, n_x).astype(int)
	params = np.zeros([n_x * n_y * n_all, 2])
	count = 0

	for x in xlist: 
	  ylist = np.linspace(n**2-x, n**2, n_y).astype(int)
	  for y in ylist: 
	     for j in range(n_all): 
	        params[count] = [x, y]
	        count += 1
	params = params.astype(int)

	count_dict = {}
	total_dict = {}

	for i in range(m): 
		key = str(params[i, 0]) + '_' + str(params[i, 1])
		if key not in count_dict: 
			count_dict[key] = 0 
			total_dict[key] = 0
		if err_none[i] < 5 * 10**-1: 
			count_dict[key] += 1
		total_dict[key] += 1
		

	points = np.zeros([len(count_dict.keys()), 3])
	count = 0
	for key in count_dict.keys(): 
		lel = key.split('_')
		xlel = int(lel[0])
		ylel = int(lel[1])

		if total_dict[key] != 50: 
			print(key, count_dict[key], total_dict[key])

		delta = xlel / n**2
		nu = (n**2 - ylel) / xlel

		points[count, 0] = delta
		points[count, 1] = nu
		points[count, 2] = count_dict[key] / total_dict[key]

		# print(xlel, ylel, count_dict[key] / n_all)

		count += 1
	# print(points)


	plt.figure()
	plt.scatter(points[:, 0], points[:, 1], c=points[:, 2], s=10, cmap="jet", vmin=0, vmax=1, lw=0)
	plt.colorbar()
	plt.xlabel('delta')
	plt.ylabel('nu')
	plt.title('phase least squares')
	plt.xlim([0, 1])
	plt.ylim([0, 1])
	plt.savefig(out + '_l2_ls_5')








def main(): 
	inp = './phase_results/phase_new_50'
	out = inp
	phase_new(inp, out)


if __name__ == '__main__':
	main()


