# distutils: language = c++
# distutils: sources = metro.cpp
# distutils: extra_compile_args = -std=c++11 -stdlib=libc++ -mmacosx-version-min=10.7

from libcpp.vector cimport vector

cdef extern from "metro.h":
    cdef cppclass metropolis:
        metropolis(int size, double temp) except +
        void init_lattice_random()
        void init_J_random()
        double energy()
        double energy_new()
        void step()
        void step_new()
        vector[int] run(int repeat, int n_steps)
        void simulate(int n_steps)
        void simulate_new(int n_steps)
        vector[int] get_lattice()
        vector[vector[double]] get_J()
        void print_lattice()
        void print_J()
        int bin_to_int()
        
cdef class Simulator:
    cdef metropolis *thisptr
    def __cinit__(self, int size, double temp):
        self.thisptr = new metropolis(size, temp)
    def __dealloc__(self):     
        del self.thisptr
    def init_lattice_random(self):
        self.thisptr.init_lattice_random()
    def init_J_random(self): 
        self.thisptr.init_J_random()
    def energy(self):
        return self.thisptr.energy()
    def energy_new(self): 
        return self.thisptr.energy_new()
    def run(self, int repeat, int n_steps): 
        return self.thisptr.run(repeat, n_steps)
    def step(self):
        return self.thisptr.step()
    def step_new(self):
        self.thisptr.step_new()
    def simulate(self, int n_steps):
        self.thisptr.simulate(n_steps)
    def simulate_new(self, int n_steps): 
        self.thisptr.simulate_new(n_steps)
    def get_lattice(self):
        return self.thisptr.get_lattice()
    def get_J(self): 
        return self.thisptr.get_J()
    def print_lattice(self): 
        self.thisptr.print_lattice()
    def print_J(self): 
        self.thisptr.print_J()
    def bin_to_int(self): 
        return self.thisptr.bin_to_int()



