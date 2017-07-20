#include "metro.h"
#include <chrono> 
using namespace std; 


metropolis::metropolis(int size, double temp, vector<vector<double>> J) :
	lattice_(size),
	temp_(temp),
	size_(size), 
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
  for (int i=0; i < size_; i++) {
    lattice_[i] = -1 + 2 * bin_rand_(r_engine_);
  }
}

double metropolis::energy()
{
	double sum = 0; 
	for (int i = 0; i < size_; i++)
	{
		vector<double> col = J_[i]; 
		sum = sum + inner_product(lattice_.begin(), lattice_.end(), col.begin(), 0.); 
		// cout << sum << " | "; 

	}
	// cout << "\n"; 
	return sum; 
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
	cout << energy_old << " vs. " << energy_new << "\n"; 
	double trans_prob = min(exp(-(energy_new - energy_old) / temp_), 1.); 
	double rv = prob_rand_(r_engine_); 
	cout << rv << ", " << trans_prob << "\n"; 
	
	if (rv > trans_prob)
	{
		energy_new = energy_old; 
		lattice_[flip_ind] = -lattice_[flip_ind]; 
	}
	print_lattice(); 
	return energy_new; 
}

vector<double> metropolis::simulate(int n_steps)
{
	cout << "start: "; 
	print_lattice(); 
	cout << "\n";  
	vector<double> energy_vector(n_steps + 1); 
	double energy_old = energy(); 
	energy_vector[0] = energy_old; 
	for (int i = 0; i < n_steps; i++) 
	{
		double e = step(energy_old); 
		energy_vector[i+1] = e; 
		energy_old = e; 
	}
	return energy_vector;
}


vector<int> metropolis::get_lattice()
{
	return lattice_; 
}

void metropolis::print_lattice()
{
	for (int i=0; i < size_; i++) {
		cout << lattice_[i] << " | "; 
	}
	cout << '\n';
}

// void metropolis::set_temp(double temp) 
// {
// 	temp_ = temp; 
// }

// void metropolis::set_J(vector<vector<double>> J)
// {
// 	J_ = J; 
// }




