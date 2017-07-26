from __future__ import division, print_function
import random 
import multiprocessing as mp
from boltzmann import *
from numpy.linalg import matrix_rank
from scipy.sparse import random


mu = -1.
sigma = 1.
num_sparse=20
a = 0.001



def graph(x, n, param):  
   obs = param[0]
   sparse = param[1]

   J = sparse_rand(n, k)
   k = np.sum(J != 0)

   S_flat = get_random_S(n).reshape([2**n, n**2])
   indices = np.random.choice(2**n, obs)
   S = np.take(S_flat, indices, axis=0)

   dE = np.dot(S, J)
   dE_rank = len(dE)

   J_none = solve(S, dE)
   J_l1 = solve_l1(S, dE, a)
   
   err_none_0 = error_l0(J, J_none, n, 10**-6)
   err_l1_0 = error_l0(J, J_l1, n, 10**-6)
   err_none_2 = np.linalg.norm(J - J_none)
   err_l1_2 = np.linalg.norm(J - J_l1)

   # results[x] = np.asarray([delta, nu, err_none, err_l1])

   if x % 1000 == 0: 
      print(x, k, sparse, obs, err_none_0, err_l1_0, err_none_2, err_l1_2)

   return (k, obs, err_none_0, err_l1_0, err_none_2, err_l1_2)


def vary_samples(x, n): 
   # results = np.zeros([num, 4])
  
   # for q in np.linspace(0., .9, num=num_sparse, endpoint=True): 
   # for x in range(num): 
   i = np.random.randint(low=1., high=n**2+1)
   q = np.random.randint(low=n**2-i, high=n**2+1)

   
   # J = sparse_random_network(n, q, 0, 1.).reshape([n**2])
   # J = sparse_num_network(n, q).reshape([n**2])
   J = sparse_rand(n, q)
   k = np.sum(J != 0)

   S_flat = get_random_S(n).reshape([2**n, n**2])

   # for i in range(1, n**2): 

   indices = np.random.choice(2**n, i)

   S = np.take(S_flat, indices, axis=0)

   dE = np.dot(S, J)
   dE_rank = len(dE)

   J_none = solve(S, dE)
   err_none_3 = error_l0(J, J_none, n, 10**-3)

   J_l1 = solve_l1(S, dE, a)
   err_l1_3 = error_l0(J, J_l1, n, 10**-3)
   
   err_none_6 = error_l0(J, J_none, n, 10**-6)
   err_l1_6 = error_l0(J, J_l1, n, 10**-6)

   # results[x] = np.asarray([delta, nu, err_none, err_l1])

   if x % 1000 == 0: 
      print(x, i, q, k, err_none_3, err_l1_3)

   return (k, i, err_none_3, err_l1_3, err_none_6, err_l1_6)

   # np.save(out + 'phase_' + str(num), results)

def vary_samples2(x, n, i, q): 
   
   J = sparse_rand(n, q)
   k = np.sum(J != 0)

   # S_flat = get_random_S(n)
   S_flat = get_noise_S(n)

   indices = np.random.choice(2**n, i)

   S = np.take(S_flat, indices, axis=0)

   dE = np.dot(S, J)
   dE_rank = len(dE)

   J_none = solve(S, dE)
   J_l1 = solve_l1(S, dE, a)
   
   if x % 400 == 0: 
      print(x, i, q, k)

   return list(J) + list(J_none) + list(J_l1)


def run(n, num, out): 

   pool = mp.Pool()
   # results = [pool.apply_async(vary_samples, args=(x, n)) for x in range(num)]
   results = [pool.apply_async(graph, args=(x, n)) for x in range(num)]
   output = [p.get() for p in results]
   print(np.shape(output))

   np.save(out + 'phase_all', output)

def run2(n, num, out): 
   n_x = 10
   n_y = 10
   n_all = 20

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

   pool = mp.Pool()
   results = [pool.apply_async(vary_samples2, args=(x, n, params[x, 0], params[x, 1])) for x in range(len(params))]
   output = [p.get() for p in results]
   # print(np.shape(output))

   np.save(out + 'test', output)




      
   

      

def main(): 
   n = 10
   num = 10**5
   output = './phase_results/'
   run2(n, num, output)
   

if __name__ == '__main__':
   main()