function [x_eq, energy_x_eq] = check_eq(m, J)
    table = dec2bin(0:(2^m-1)) - '0';
    table = 2*table - 1; 
    
    x_eq = zeros(0, m);     
    energy_x_eq = Inf; 
    
    for i=1:2^m
        x = table(i,:); 
        energy_x = energy(x, J); 
        
%         disp(x)
%         disp(energy_x)
       
        if energy_x < energy_x_eq
            x_eq = [x]; 
            energy_x_eq = energy_x; 
        elseif energy_x == energy_x_eq
            x_eq = vertcat(x_eq, x);  
        end
    end
    
end