// #include "metro.h"
#include "metro.h"
using namespace std; 


int main()
{
	int size = 5; 
	double temp = 1; 
	vector<vector<double>> J(size, vector<double>(size)); 
	for (int i=0; i < size; i++) {
		for (int j=0; j < size; j++)
		{
	    	J[i][j] = 1.;
	    }	
	}


	metropolis metro(size, temp); 
	metro.print_J(); 
	metro.simulate_new(3); 
	metro.print_lattice(); 
	int result = metro.bin_to_int(); 
	cout << result << "\n"; 

	// Ising2D metro (size, temp); 

	return 0; 
}
