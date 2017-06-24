from __future__ import division, print_function
import numpy as np
import random 
# from boltzmann import *
from runs import *
import matplotlib.pyplot as plt


def visualize(out, number, low, high, stride, outfile): 
	path = out + 'err_dict_' + str(number) + '_' + str(low) + '_' + str(high) + '_' + str(stride)
	err_dict = np.load(path + '.npy').item()

	path = './results_l1/' + 'err_dict_l1_' + str(number) + '_' + str(low) + '_' + str(high) + '_' + str(stride)
	err_dict_l1 = np.load(path + '.npy').item()

	
	plt.figure()
	for key in err_dict.keys(): 
		if key < 3:  
			plt.scatter([key] * number, np.log(err_dict[key]), color='b', s=1)
	for key in err_dict_l1.keys(): 
		if key < 3: 
			plt.scatter([key] * number, np.log(err_dict_l1[key]), color='r', s=1)
	plt.ylabel('error')
	plt.xlabel('temperature')
	plt.show()


def main(): 
	# n = 10
	# number = 5
	# low = -1
	# high = 5
	# stride = 20
	# it = 100
	# repeat = 1000
	# threshold = 1.
	# l1 = False
	# runvar = False

	# if l1 == False: 
	# 	output = './results/'
	# 	outfile = output + 'vis'
	# 	if runvar==True: 
	# 		run(n, number, low, high, stride, it, repeat, threshold, output)

	# elif l1 == True: 
	# 	output = './results_l1/'
	# 	outfile = output + 'vis'
	# 	a = 1.
	# 	if runvar==True: 
	# 		run_l1(n, number, low, high, stride, it, repeat, threshold, output, a)

	# visualize(output, number, low, high, stride, outfile)


	n = 10
	number = 10**8
	low = -1
	high = 4
	threshold = 10.
	output = './results/'
	run_repeat_temp(n, number, low, high, threshold, output)


if __name__ == '__main__':
	main()
