(1. build cython and c++ code) python setup.py build_ext -i  
(2. run the simulation through python) python run.py  
  
  
metro.cpp - actual simulation functions in C++  
mitro.pyx - cython code for compiling C++ code  
setup.py - python code for compiling cython code   
run.py - python script which runs simulations; set parameter values here (network size, temp, # runs, # steps, etc)

(main.cpp was used just for testing purposes and boltzmann.py is the old python code for simulating stuff, used for reference)
