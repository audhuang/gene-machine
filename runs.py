import random 
from boltzmann import *



def run(n, number, low, high, stride, it, repeat, threshold, out): 
	bin_to_int = {}
	int_to_bin = {}
	x_all = np.zeros([2**n, n])
	bin = np.zeros([n])
	for i in range(2 ** n): 
		temp = "{0:b}".format(i)
		bin = '0' * (n - len(temp)) + temp
		bin_to_int[bin] = i
		int_to_bin[i] = bin
		x_all[i] = list(bin)
	x_all = x_all * 2 - 1

	J_dict = {}
	err_dict = {}

	energies = energy_all(x_all, J, h, c, n)


	for c_ in np.linspace(low, high+1, stride): 
		c = 10. ** c_
		print('c: ', c)

		J_dict[c_] = np.zeros([number, n, n])
		err_dict[c_] = np.zeros([number])
		for num in range(number): 
			J = random_network(n)
			h = np.zeros([n])
			
			x_array, e_array = boltz(J, h, c, n, it, repeat)
			
			states = x_to_states(x_array, n, repeat, bin_to_int)
			
			dE, S = states_to_dE_one(states, x_all, n, threshold, c)

			S_flat = S.reshape([2**n, n**2])
			dE_flat = dE

			J_hat = solve(S_flat, dE_flat)
			J_hat = J_hat.reshape([n, n])
			
			err = error(J, J_hat, n)
			print('error: ', err)

			J_dict[c_][num] = J_hat
			err_dict[c_][num] = err 
			np.save(out + './J_dict_' + str(number) + '_' + str(low) + '_' + str(high) + '_' + str(stride), J_dict)
			np.save(out + './err_dict_' + str(number) + '_' + str(low) + '_' + str(high) + '_' + str(stride), err_dict)

		print('\n')
	# print(err_dict)



def run_l1(n, number, low, high, stride, it, repeat, threshold, out, a): 
	bin_to_int = {}
	int_to_bin = {}
	x_all = np.zeros([2**n, n])
	bin = np.zeros([n])
	for i in range(2 ** n): 
		temp = "{0:b}".format(i)
		bin = '0' * (n - len(temp)) + temp
		bin_to_int[bin] = i
		int_to_bin[i] = bin
		x_all[i] = list(bin)
	x_all = x_all * 2 - 1

	J_dict = {}
	err_dict = {}

	energies = energy_all(x_all, J, h, c, n)


	for c_ in np.linspace(low, high+1, stride): 
		c = 10. ** c_
		print('c: ', c)

		J_dict[c_] = np.zeros([number, n, n])
		err_dict[c_] = np.zeros([number])
		for num in range(number): 
			J = random_network(n)
			h = np.zeros([n])
			
			x_array, e_array = boltz(J, h, c, n, it, repeat)
			
			states = x_to_states(x_array, n, repeat, bin_to_int)
			
			dE, S = states_to_dE_one(states, x_all, n, threshold, c)

			S_flat = S.reshape([2**n, n**2])
			dE_flat = dE

			J_hat = solve_l1(S_flat, dE_flat, a)
			J_hat = J_hat.reshape([n, n])
			
			err = error(J, J_hat, n)
			print('error: ', err)

			J_dict[c_][num] = J_hat
			err_dict[c_][num] = err 
			np.save(out + './J_dict_l1_' + str(number) + '_' + str(low) + '_' + str(high) + '_' + str(stride), J_dict)
			np.save(out + './err_dict_l1_' + str(number) + '_' + str(low) + '_' + str(high) + '_' + str(stride), err_dict)

		print('\n')
	# print(err_dict)


def run_repeat_temp(n, number, low, high, threshold, out): 
	bin_to_int = {}
	int_to_bin = {}
	x_all = np.zeros([2**n, n])
	bin = np.zeros([n])
	for i in range(2 ** n): 
		temp = "{0:b}".format(i)
		bin = '0' * (n - len(temp)) + temp
		bin_to_int[bin] = i
		int_to_bin[i] = bin
		x_all[i] = list(bin)
	x_all = x_all * 2 - 1

	# Jhats = np.zeros([number, n, n])
	errors = np.zeros([number, 2])

	c_list = np.random.uniform(low, high, number)
	repeat_list = np.random.randint(100, 10**6, number)

	for i in range(number):
		c = 10. ** c_list[i]
		repeat = repeat_list[i]

		J = random_network(n)
		h = np.zeros([n])

		energies = energy_all(x_all, J, h, c, n)
		
		x_array, e_array = prob_dist(J, h, c, n, x_all, energies, repeat)
		
		states = x_to_states(x_array, n, repeat, bin_to_int)
		
		dE, S = states_to_dE_one(states, x_all, n, threshold, c)

		S_flat = S.reshape([2**n, n**2])
		dE_flat = dE

		J_hat = solve(S_flat, dE_flat)
		J_hat = J_hat.reshape([n, n])
		
		err = error(J, J_hat, n)
		# print('error: ', err)

		# Js[i] = J_hat
		errors[i, 0] = c_list[i]
		errors[i, 1] = err 

		if i % 1000 == 0: 
			print('run: ', i, c_list[i], repeat)
			print('error: ', err)
			np.save(out + 'err_repeat_temp', errors)
	np.save(out + 'err_repeat_temp', errors)
	# print(errors)






def main(): 
	return 


if __name__ == '__main__':
	main()

