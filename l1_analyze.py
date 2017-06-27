from __future__ import division, print_function
import random 
import multiprocessing as mp
from boltzmann import *
from numpy.linalg import matrix_rank
import matplotlib.pyplot as plt



def l1_none_c(inp, out): 
	results = np.load('./l1_results/' + inp + '.npy')
	
	c_ = results[:, 0]
	repeat = results[:, 1]
	err_none = np.log(results[:, 4])
	err_l1 = np.log(results[:, 6])
	# print(c_[::20])

	plt.figure()
	plt.scatter(err_none, err_l1, c=c_, s=1, cmap="hot", vmin=-1, vmax=4)
	plt.colorbar()
	plt.xlabel('Unreg. Error')
	plt.ylabel('L1 Reg. Error')
	plt.xlim([0, np.max(err_none) + 1])
	plt.ylim([0, np.max(err_none) + 1])
	plt.title('Error')
	plt.savefig('./l1_results/' + out + '_c')


def l1_none_dE(inp, out): 
	results = np.load('./l1_results/' + inp + '.npy')
	
	c = results[:, 0]
	dE = results[:, 3]
	err_none = np.log(results[:, 4])
	err_l1 = np.log(results[:, 6])
	

	plt.figure()
	plt.scatter(err_none, err_l1, c=dE, s=1, cmap="hot", vmin=0, vmax=1024)
	plt.colorbar()
	plt.xlabel('Unreg. Error')
	plt.ylabel('L1 Reg. Error')
	plt.xlim([0, np.max(err_none) + 1])
	plt.ylim([0, np.max(err_none) + 1])
	plt.title('Error')
	plt.savefig('./l1_results/' + out + '_dE')


def l1_temp_err(inp, out): 
	results = np.load('./l1_results/' + inp + '.npy')

	c = results[:, 0]
	err_none = np.log(results[:, 4])
	err_l1 = np.log(results[:, 6])
	dE = results[:, 3]
	J_rank = results[:, 2]
	J_none = results[:, 5]
	J_l1 = results[:, 7]

	plt.figure()
	plt.scatter(c, err_l1, c='r', s=.5)
	plt.scatter(c, err_none, c='b', s=.5)
	plt.xlabel('Log(Temp)')
	plt.ylabel('Error')
	plt.title('Error v Temp, 20 random sparse networks')
	plt.savefig('./l1_results/' + out)

	plt.figure()
	plt.scatter(c, J_l1, c='r', s=.5)
	plt.scatter(c, J_none, c='b', s=.5)
	plt.xlabel('Log(Temp)')
	plt.ylabel('Rank')
	plt.title('Rank v Temp, 20 random sparse networks')
	plt.savefig('./l1_results/' + out + '_rank')

	plt.figure()
	plt.scatter(c, dE, c='g', s=1)
	plt.xlabel('Log(Temp)')
	plt.ylabel('# dE')
	plt.title('dE v Temp')
	plt.savefig('./l1_results/' + out + '_dE')

	plt.figure()
	plt.scatter(c, J_rank, c='g', s=1)
	plt.xlabel('Log(Temp)')
	plt.ylabel('J rank')
	plt.title('J rank v Temp')
	plt.savefig('./l1_results/' + out + '_Jrank')


def l1_repeat_temp(inp, out): 
	results = np.load('./l1_results/' + inp + '.npy')

	c = results[:, 0]
	repeat = results[:, 1]
	err_none = np.log(results[:, 4])
	err_l1 = np.log(results[:, 6])
	dE = results[:, 3]
	J_rank = results[:, 2]
	J_none = results[:, 5]
	J_l1 = results[:, 7]
	print(np.max(err_none), np.max(err_l1))

	plt.figure()
	plt.scatter(c, repeat, c=err_none, s=1, cmap="hot", vmin=-3, vmax=8)
	plt.colorbar()
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('Samples vs Temp for size 10 sparse networks')
	plt.savefig('./l1_results/' + out + '_none')

	err_diff = err_none - err_l1
	plt.figure()
	plt.scatter(c, repeat, c=err_diff, s=1, cmap="seismic", vmin=-4, vmax=4)
	plt.colorbar()
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('Samples vs Temp for size 10 sparse networks Diff')
	plt.savefig('./l1_results/' + out + '_diff')
	return

	plt.figure()
	plt.scatter(c, repeat, c=err_none, s=1, cmap="hot", vmin=-3, vmax=8)
	plt.colorbar()
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('Samples vs Temp for size 10 sparse networks')
	plt.savefig('./l1_results/' + out + '_none')


	plt.figure()
	plt.scatter(c, repeat, c=err_l1, s=1, cmap="hot", vmin=-3, vmax=8)
	plt.colorbar()
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('Samples vs Temp for size 10 sparse networks L1')
	plt.savefig('./l1_results/' + out + '_l1')

	plt.figure()
	plt.scatter(c, repeat, c=J_rank, s=1, cmap="hot", vmin=0, vmax=10)
	plt.colorbar()
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('J Rank')
	plt.savefig('./l1_results/' + out + '_rank')

	plt.figure()
	plt.scatter(c, repeat, c=J_none, s=1, cmap="hot", vmin=0, vmax=10)
	plt.colorbar()
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('J_hat Rank')
	plt.savefig('./l1_results/' + out + '_rank_none')

	plt.figure()
	plt.scatter(c, repeat, c=J_l1, s=1, cmap="hot", vmin=0, vmax=10)
	plt.colorbar()
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('J_hat Rank L1')
	plt.savefig('./l1_results/' + out + '_rank_l1')

	plt.figure()
	plt.scatter(c, repeat, c=dE, s=1, cmap="hot", vmin=0, vmax=1024)
	plt.colorbar()
	plt.xlabel('Log(Temp)')
	plt.ylabel('Samples')
	plt.title('# Entries in dE')
	plt.savefig('./l1_results/' + out + '_rank_dE')



def main(): 
	# inp = 'none_l1_4_1'
	# out = 'none_l1_4_1'
	# l1_none_c(inp, out)
	# l1_none_dE(inp, out)

	# inp = 'temp_err_20_50_1'
	# out = inp
	# l1_temp_err(inp, out)

	inp = 'none_l1_5_1'
	out = inp
	l1_repeat_temp(inp, out)

if __name__ == '__main__':
	main()

