from __future__ import division, print_function
import random 
import multiprocessing as mp
from boltzmann import *
from numpy.linalg import matrix_rank
from scipy.sparse import random


mu = 0.
sigma = 1.
num_sparse=20
a = 0.001


def get_full_S(x_all, n): 
   S = np.zeros([2 ** n, n, n])
   base = np.random.randint(0, 2**n)
   for i in range(2**n): 
      S[i] = np.transpose(np.outer(x_all[i], x_all[i]) - np.outer(x_all[base], x_all[base]))
   return S

def get_random_S(n): 
   return np.random.normal(mu, sigma, [2**n, n**2])

def get_bin_S(n): 
   x = np.random.binomial(1, 0.5, [2**n, n**2])
   x = x * 2 - 1
   return x

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


def run(n, num, out): 
   params = np.zeros([n, k, repeat])

   for i in range(1, 10): 
      params[0] = 0.1 * 




   pool = mp.Pool()
   # results = [pool.apply_async(vary_samples, args=(x, n)) for x in range(num)]
   results = [pool.apply_async(graph, args=(x, n)) for x in range(num)]
   output = [p.get() for p in results]
   print(np.shape(output))

   np.save(out + 'phase_all', output)



      
   

      

def main(): 
   n = 10
   num = 10**5
   output = './phase_results/'
   run(n, num, output)
   

if __name__ == '__main__':
   main()