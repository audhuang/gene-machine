import numpy as np
import random
import matplotlib.pyplot as plt




def heatmap(inp, out): 
	err = np.load('./results/' + inp + '.npy')

	c = err[:, 0]
	repeat = err[:, 1]
	error = np.log(err[:, 2])


	plt.figure()
	plt.scatter(c, repeat, c=error, s=1, cmap="hot", vmin=-3, vmax=8)
	plt.colorbar()
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('Samples vs Temp for size 10 networks (100,000 points)')
	plt.savefig('./results/' + out)


def rankmap(inp, out): 
	results = np.load('./results/' + inp + '.npy')
	
	c = results[:, 0]
	repeat = results[:, 1]
	rank = results[:, 4]

	plt.figure()
	plt.scatter(c, repeat, c=rank, s=1, cmap="hot", vmin=0, vmax=10)
	plt.colorbar()
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('J_hat Rank')
	plt.savefig('./results/' + out)




def dEmap(inp, out): 
	results = np.load('./results/' + inp + '.npy')
	
	c = results[:, 0]
	repeat = results[:, 1]
	rank = results[:, 5]

	plt.figure()
	plt.scatter(c, repeat, c=rank, s=1, cmap="hot", vmin=0, vmax=1024)
	plt.colorbar()
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('# Entries in dE')
	plt.savefig('./results/' + out)


def main(): 
	inp = 'repeat_temp_5_old'
	out = 'samples_temp_5_old'
	heatmap(inp, out)

	out = 'rank_temp_5_old'
	rankmap(inp, out)

	out = 'dE_temp_5_old'
	dEmap(inp, out)
	




if __name__ == '__main__':
	main()

