% initiate weight matrix and initial state
m = 5; 
a = normrnd(0, 1, m);
J = triu(a) + triu(a,1)';
J(1:m+1:end) = 0; 
x_0 = 2 * binornd(1, 0.5, 1, m) - 1; 
% x_0 = [-1 -1 -1 -1 -1]; 

kb = physconst('Boltzmann'); 
T = 310; 

% imagesc(J)
% colormap hot
% colorbar

display(x_0)
% display(J)
e_0 = energy(x_0, J);

% iterations of MH
iter = 10; 
x_cur = x_0; 
x_array = zeros((iter*m), m); 
% x_array = zeros(iter, m);
energy_array = zeros((iter*m), 1); 

for i=1:iter
    for j=1:m
        
        x_new = x_cur; 
        x_new(1, j) = -x_cur(1, j); 
        
        a = acceptance(x_new, x_cur, J, (kb*T)); 
        q = unifrnd(0, 1); 
       	% display([a, q])
        
        if q <= a 
            x_cur = x_new; 
        end
        
        x_array((i-1)*(m)+j,:) = x_cur; 
        energy_array((i-1)*(m)+j, 1) = energy(x_cur, J); 

    end
    % x_array(i,:) = x_cur; 
end
x_array = vertcat(x_0, x_array); 
energy_array = vertcat(e_0, energy_array); 

[x_eq, energy_x_eq] = check_eq(m, J); 
display(x_eq)
display(energy_x_eq)

display(x_array(end,:))
display(energy_x_eq(end))


figure 
subplot(2, 1, 1)
imagesc(transpose(x_array))
colormap hot
xlim([1, m*iter])

subplot(2, 1, 2)
plot(transpose(energy_array))
xlim([1, m*iter])













