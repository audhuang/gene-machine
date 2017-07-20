// #include "metro.h"
#include "metro.h"
using namespace std; 


int main()
{
	int size = 3; 
	double temp = 1; 
	vector<vector<double>> J(size, vector<double>(size)); 
	for (int i=0; i < size; i++) {
		for (int j=0; j < size; j++)
		{
	    	J[i][j] = 1;
	    }	
	}


	metropolis metro(size, temp, J); 


	int n_steps = 5; 
	vector<double> energy = metro.simulate(n_steps); 
	for (int i = 0; i < (n_steps + 1); i++) {
		cout << energy[i] << " | "; 
	}
	cout << '\n';  


	// Ising2D metro (size, temp); 

	return 0; 
}
