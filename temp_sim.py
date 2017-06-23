from __future__ import division, print_function
import numpy as np
import random 
from boltzmann import *


def visualize(): 
	return



def main(): 
	n = 10
	number = 5
	low = -1
	high = 10
	stride = 100
	it = 100
	repeat = 1000
	threshold = 1.
	output = './results/'

	run(n, number, low, high, stride, it, repeat, threshold, output)

if __name__ == '__main__':
	main()
