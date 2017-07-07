from __future__ import division, print_function
import random 
import multiprocessing as mp
from boltzmann import *
from numpy.linalg import matrix_rank
from scipy.sparse import random


thresh = 10**-4
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


def vary_samples(x, n): 
   # results = np.zeros([num, 4])
  
   # for q in np.linspace(0., .9, num=num_sparse, endpoint=True): 
   # for x in range(num): 
   q = np.random.uniform(low=0., high=1.)
   i = np.random.randint(low=1., high=n**2+1)
   
   J = sparse_random_network(n, q, 0, 1.)
   while np.sum(abs(J)) == 0: 
      J = sparse_random_network(n, q, 0, 1.)
   J = J.reshape([n**2])
   k = np.sum(J != 0)

   S_flat = get_random_S(n).reshape([2**n, n**2])

   # for i in range(1, n**2): 

   indices = np.random.choice(2**n, i)

   S = np.take(S_flat, indices, axis=0)

   dE = np.dot(S, J)
   dE_rank = len(dE)

   J_none = solve(S, dE)
   # print(J_none.reshape([n, n]))
   err_none = error(J, J_none, n)
   # Jnone_rank = matrix_rank(J_none)

   J_l1 = solve_l1(S, dE, a)
   # print(J_l1.reshape([n, n]))
   err_l1 = error(J, J_l1, n)
      

   # results[x] = np.asarray([delta, nu, err_none, err_l1])

   if x % 100 == 0: 
      print(x, q, i, err_none, err_l1)

   return (q, i, err_none, err_l1)

   # np.save(out + 'phase_' + str(num), results)


def run(n, num, out): 
   pool = mp.Pool()
   results = [pool.apply_async(vary_samples, args=(x, n)) for x in range(num)]
   output = [p.get() for p in results]
   print(np.shape(output))

   np.save(out + '_phase_3', output)
   

      

def main(): 
   n = 10
   num = 10**3
   output = './phase_results/'
   run(n, num, output)
   

if __name__ == '__main__':
   main()