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
	double energy_old = metro.energy(); 

	for (int i = 0; i < size; i++)
	{
		metro.print_lattice(); 		
		metro.step_new(); 
		cout << "\n"; 
	}

	// Ising2D metro (size, temp); 

	return 0; 
}
