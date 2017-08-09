#include "metro.h"
#include <chrono> 
#include <sstream>
#include <string>
using namespace std; 


metropolis::metropolis(int size, double temp) :
	lattice_(size),
	J_(size, vector<double>(size)), 
	temp_(temp),
	size_(size), 
	h_(size), 
	seed_(std::chrono::system_clock::now().time_since_epoch().count()),
	r_engine_(seed_),
	bin_rand_(0,1),
	ind_rand_(0, size-1),
	prob_rand_(0.0, 1.0), 
	norm_rand_(0.0, 1.0)
{
	init_lattice_random(); 
	init_J_random(); 
	init_h_zero(); 

}


metropolis::~metropolis()
{

}

void metropolis::init_lattice_random()
{
  for (int i=0; i < size_; i++) {
    lattice_[i] = -1 + 2 * bin_rand_(r_engine_);
    // lattice_[i] = 1; 
  }
}

void metropolis::init_J_random()
{
	for (int i=0; i < size_; i++) {
		for (int j=0; j < i; j++)
		{
	    	J_[i][j] = norm_rand_(r_engine_);
	    	J_[j][i] = J_[i][j]; 
	    }
	    J_[i][i] = 0; 	
	}
}

// add in h 
double metropolis::energy()
{
	double sum = 0; 
	for (int i = 0; i < size_; i++)
	{
		for (int j = 0; j < size_; j++)
		{
			sum = sum + lattice_[i] * lattice_[j] * J_[i][j]; 
		}
	}
	return sum; 
}

double metropolis::energy_new()
{
	return 0.; 
}


void metropolis::step()
{
	int flip_ind = ind_rand_(r_engine_); 
	double energy_old = energy(); 
	lattice_[flip_ind] = -lattice_[flip_ind]; 
	double energy_new = energy(); 
	cout << "old: " << energy_new - energy_old << "\n"; 

	double trans_prob = min(exp(-1 * (energy_new - energy_old) / temp_), 1.); 
	double rv = prob_rand_(r_engine_); 
	// cout << "old: " << -1 * (energy_new - energy_old) << "\n"; 
	
	if (rv > trans_prob)
	{
		lattice_[flip_ind] = -lattice_[flip_ind]; 
	}
	return; 
}

// add in h 
// https://stackoverflow.com/questions/3376124/how-to-add-element-by-element-of-two-stl-vectors
void metropolis::step_new()
{

	int flip_ind = ind_rand_(r_engine_); 

	// double energy_old = energy(); 
	// lattice_[flip_ind] = -lattice_[flip_ind]; 
	// double energy_new = energy(); 
	// lattice_[flip_ind] = -lattice_[flip_ind]; 
	// cout << "old: " << energy_new - energy_old << "\n"; 

	int val_i = lattice_[flip_ind]; 
	double energy_diff = -4 * val_i * inner_product(lattice_.begin(), lattice_.end(), J_[flip_ind].begin(), 0.); 
	// cout << "new: " << energy_diff << "\n"; 
	
	if (energy_diff <= 0)
	{
		// cout << "new: 1" << "\n"; 
		lattice_[flip_ind] = -lattice_[flip_ind]; 
	}
	
	else
	{
		double trans_prob = exp(-1 * energy_diff / temp_); 

		double rv = prob_rand_(r_engine_); 
		// cout << "new: " << trans_prob << "\n"; 
		
		if (rv < trans_prob)
		{
			lattice_[flip_ind] = -lattice_[flip_ind]; 
		}
	}
	
	return; 
}

vector<int> metropolis::run(int repeat, int n_steps)
{
	vector<int> counts(pow(2, size_), 0); 
	for (int i = 0; i < repeat; i++)
	{
		simulate_new(n_steps); 
		vector<unsigned long int> index = bin_to_int(); 
		counts[index[0]] = counts[index[0]] + 1; 
		
		if (i % 10000 == 0)
		{
			cout << i << ": " << index[0] << "\n"; 
		}
	}
	return counts; 
}



vector<unsigned long int> metropolis::bin_to_int()
{
	vector<unsigned long int> sum = {0, 0}; 
	unsigned long int temp = 1; 
	unsigned long int mult = 2; 
	for (int i = 0; i < (size_ /2); i++)
	{
		if (lattice_[i] == 1)
		{
			sum[0] = sum[0] + temp; 
		}
		temp = temp * mult; 
		// cout << i << " | " << sum[0] << "\n"; 
	}

	temp = 1; 
	mult = 2; 
	for (int i = (size_ / 2); i < size_ ; i++)
	{
		if (lattice_[i] == 1)
		{
			sum[1] = sum[1] + temp; 
		}
		temp = temp * mult; 
		// cout << i << " || " << sum[1] << "\n"; 
	}

	return sum; 
}

void metropolis::simulate_new(int n_steps)
{
	for (int i = 0; i < n_steps; i++) 
	{
		step_new(); 
	}
	return; 
}


void metropolis::simulate(int n_steps)
{
	for (int i = 0; i < n_steps; i++) 
	{
		step(); 
	}
	return;
}


vector<int> metropolis::get_lattice()
{
	return lattice_; 
}


vector<vector<double>> metropolis::get_J()
{
	return J_; 
}

void metropolis::print_lattice()
{
	for (int i=0; i < size_; i++) {
		cout << lattice_[i] << " | "; 
	}
	cout << "\n";
}

string metropolis::get_lattice_string()
{
	vector<int> binary(size_); 
	for (int i = 0; i < size_; i++)
	{
		binary[i] = (lattice_[i] + 1) / 2; 
	}

	stringstream result;
	copy(binary.begin(), binary.end(), ostream_iterator<int>(result, ""));

	return result.str(); 
}


void metropolis::print_J()
{
	for (int i=0; i < size_; i++) 
	{
		for (int j = 0; j < size_; j++)
		{
			cout << J_[i][j] << " | "; 
		}
		cout << "\n";
	}
}

void metropolis::set_h(vector<double> h)
{
	h_ = h; 
}

void metropolis::init_h_zero()
{
	for (int i = 0; i < size_; i++)
	{
		h_[i] = 0; 
	}
}

vector<double> metropolis::get_h()
{
	return h_; 
}

// void metropolis::set_temp(double temp) 
// {
// 	temp_ = temp; 
// }

// void metropolis::set_J(vector<vector<double>> J)
// {
// 	J_ = J; 
// }




