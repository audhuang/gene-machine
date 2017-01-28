function e = energy(x, J)
    e = x * J * transpose(x); 
    e = e / 2;
end