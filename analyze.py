import numpy as np
import random
import matplotlib.pyplot as plt




def heatmap(inp, out): 
	err = np.load('./results/' + inp + '.npy')
	print(np.shape(err))

	c = err[:, 0]
	repeat = err[:, 1]
	error = np.log(err[:, 2])


	plt.figure()
	plt.scatter(c, repeat, c=error, s=5, cmap="hot", vmin=-3, vmax=8)
	plt.colorbar()
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('Samples vs Temp for size 10 networks (10,000 points)')
	plt.savefig('./results/' + out)


def rank_v_T(inp, out): 
	results = np.load('./results/' + inp + '.npy')
	c = err[:, 0]
	rank = results[:, 3]

	plt.figure()
	plt.scatter(c, rank)
	plt.xlabel('Log(Temp)')
	plt.ylabel('Rank')
	plt.title('Rank v Temp')
	plt.savefig('./results/' + out)


def main(): 
	inp = 'repeat_temp_l1'
	out = 'samples_temp_l1_10000'
	heatmap(inp, out)
	




if __name__ == '__main__':
	main()

