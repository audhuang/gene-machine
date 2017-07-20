#include "metro.h"
#include <chrono> 
using namespace std; 


metropolis::metropolis(unsigned size, double temp, vector<vector<double>> J) :
	lattice_(size),
	temp_(temp),
	seed_(std::chrono::system_clock::now().time_since_epoch().count()),
	r_engine_(seed_),
	bin_rand_(0,1),
	ind_rand_(0, size-1),
	prob_rand_(0.0, 1.0)
{
	J_ = J; 
	init_lattice_random(); 
}


metropolis::~metropolis()
{

}


void metropolis::init_lattice_random()
{
  for (unsigned i=0; i< lattice_.size(); i++) {
    lattice_[i] = -1 + 2 * bin_rand_(r_engine_);
  }
}

double metropolis::energy()
{
	
	return 0.; 
}

double metropolis::energy_new()
{
	return 0.; 
}


double metropolis::step(double energy_old)
{
	// int size = lattice_.size(); 
	int flip_ind = ind_rand_(r_engine_); 
	lattice_[flip_ind] = -lattice_[flip_ind]; 
	double energy_new = energy(); 
	double trans_prob = min(exp(-(energy_new - energy_old) / temp_), 1.); 
	
	if (prob_rand_(r_engine_) > trans_prob)
	{
		energy_new = energy_old; 
		lattice_[flip_ind] = -lattice_[flip_ind]; 
	}
	return energy_new; 
}

vector<double> metropolis::simulate(int n_steps)
{
	vector<double> energy_vector(n_steps); 
	double energy_old = energy(); 
	for (int i = 0; i < n_steps; i++) 
	{
		double e = step(energy_old); 
		energy_vector[i] = e; 
		energy_old = e; 
	}
	return energy_vector;
}


vector<int> metropolis::get_lattice()
{
	return lattice_; 
}

// void metropolis::set_temp(double temp) 
// {
// 	temp_ = temp; 
// }

// void metropolis::set_J(vector<vector<double>> J)
// {
// 	J_ = J; 
// }




