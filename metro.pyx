# distutils: language = c++
# distutils: sources = metro.cpp
# distutils: extra_compile_args = -std=c++11 -stdlib=libc++ -mmacosx-version-min=10.7 

from libcpp.vector cimport vector

cdef extern from "metro.h":
    cdef cppclass metropolis:
        metropolis(int size, double temp, vector[vector[double]] J) except +
        void init_lattice_random()
        double energy()
        double energy_new()
        double step(double energy_old)
        void step_new()
        vector[double] simulate(int n_steps)
        void simulate_new(int n_steps)
        vector[int] get_lattice()
        void print_lattice()
        
cdef class Simulator:
    cdef metropolis *thisptr
    def __cinit__(self, int size, double temp, vector[vector[double]] J):
        self.thisptr = new metropolis(size, temp, J)
    def __dealloc__(self):     
        del self.thisptr
    def init_lattice_random(self):
        self.thisptr.init_lattice_random()
    def energy(self):
        return self.thisptr.energy()
    def energy_new(self): 
        return self.thisptr.energy_new()
    def step(self, double energy_old):
        return self.thisptr.step(energy_old)
    def step_new(self):
        self.step_new()
    def simulate(self, int n_steps):
        return self.thisptr.simulate(n_steps)
    def simulate_new(self, int n_steps): 
        self.thisptr.simulate_new(n_steps)
    def get_lattice(self):
        return self.thisptr.get_lattice()
    def print_lattice(self): 
        self.thisptr.print_lattice()



