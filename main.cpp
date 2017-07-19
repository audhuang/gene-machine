// #include "metro.h"
#include "Ising2D.h"

int main()
{
	unsigned size = 2; 
	double temp = 1; 
	vector<vector<double>> J(size, vector<double>(size)); 
	for (int i=0; i < size; i++) {
		for (int j=0; j < size; j++)
		{
	    	J[i][j] = 1;
	    }	
	}

	// metropolis metro (size, temp, J); 
	Ising2D metro (size, temp); 
}
