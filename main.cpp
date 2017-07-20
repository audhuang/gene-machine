// #include "metro.h"
#include "metro.h"
using namespace std; 

int main()
{
	unsigned size = 2; 
	double temp = 1; 
	vector<vector<double>> J(size, vector<double>(size)); 
	for (unsigned i=0; i < size; i++) {
		for (unsigned j=0; j < size; j++)
		{
	    	J[i][j] = 1;
	    }	
	}

	metropolis metropolis(size, temp, J); 
	// Ising2D metro (size, temp); 

	return 0; 
}
