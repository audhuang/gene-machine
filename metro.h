#include <vector>
#include <random>
#include <iostream>


using namespace std; 


class metropolis {
	public:
		metropolis(int size, double temp);
		~metropolis(); 
		void init_lattice_random(); 
		void init_J_random(); 
		double energy(); 
		double energy_new(); 
		void step(); 
		void step_new(); 
		vector<int> run(int repeat, int n_steps); 
		void simulate(int n_steps);
		void simulate_new(int n_steps); 
		vector<int> get_lattice();
		vector<vector<double>> get_J(); 
		void print_lattice(); 
		void print_J(); 
		int bin_to_int(); 

		// void set_temp(double temp);
		// void set_J(vector<vector<double>> J); 


	private:  
		vector<int> lattice_; // spin lattice
		double temp_;  // temperature ( T = 1/beta ) 
		vector<vector<double>> J_; 
		int size_; 

		unsigned seed_;  // random seed
		default_random_engine r_engine_;
		uniform_int_distribution<int> bin_rand_;
		uniform_int_distribution<int> ind_rand_;
		uniform_real_distribution<double> prob_rand_;
		normal_distribution<double> norm_rand_; 

};


