function landscape = energy_landscape(m, J)
    table = dec2bin(0:(2^m-1)) - '0';
    table = 2*table - 1; 
    
    landscape = zeros(2^m, 1); 
    for i=1:2^m
        landscape(i,1) = energy(table(i,:), J); 
    end
end