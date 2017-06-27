function [states, s_l2, p_l4, p_l2, p_l3] = boltzmann(m, J, h, T, steps, repeat)
%     tic; 

%     m = 10; 
%     kb = 1;%physconst('Boltzmann'); 
%     T = 5; 

%     J_temp = normrnd(0, 1, m);
%     J = triu(J_temp) + triu(J_temp,1)';
%     J(1:m+1:end) = 0; 
%     h = zeros([1, m]); 

    % [x_eq, energy_x_eq] = check_eq(m, J, h);
    % landscape = energy_landscape(m, J, h); 

%     steps = 200; 
%     repeat = 20000; 

    states = metropolis_boltzmann(J, h, T, steps, repeat);
    p = zeros(size(states)); 
    states_threshold = 10; 
    states_total = sum(states); % ignore < 10 states in sum? 

    % count up probabilities (greater than 10)
    for i = 1:numel(states),
        if states(i) > states_threshold,
            p(i) = states(i) / states_total; 
    %         disp(['state: ', mat2str(de2bi(i-1, m)), ' | ', 'prob: ', num2str(p(i))])
        end
    end

    % construct states matrix
    s = zeros([2^m, m]); 
    for i = 1:numel(states),
        s(i, :) = fliplr(de2bi(i-1, m)); 
    end
    s = s * 2 - 1;
    
    p_l2 = zeros([2^m, 2^m]); 
    s_l2 = zeros([2^m, 2^m, m^2]); 
    p_l3 = zeros([2^m, 2^m]); 

    % construct system of equations
    % dE_l = E(s^n) - E(s^k) 
    % s_l = flat [outer product s^n - outer product s^k]
    l = 0.5 * sum(p>0) * (sum(p>0) - 1); 
    dE_l = zeros([l, 1]); 
    s_l = zeros([l, m^2]); 


    l_ind = 1; 
    for i=1:numel(p), 
        for j=(i+1):numel(p),
            temp = transpose(s(i,:)) * s(i,:) - transpose(s(j,:)) * s(j,:); 
            s_l2(i, j, :) = reshape(tril(temp), [1, m^2]); 
            if p(i) > 0 && p(j) > 0, 
                p_l3(i, j) = min(p(i), p(j)); 
                p_l2(i, j) = -T * log(p(i) / p(j)) + s(j, :) * transpose(h) - s(i, :) * transpose(h); 

                dE_l(l_ind, 1) = -T * log(p(i) / p(j)) + s(j, :) * transpose(h) - s(i, :) * transpose(h); 
                s_l(l_ind, :) = reshape(tril(temp), [1, m^2]); 
                l_ind = l_ind + 1; 
            end
        end
    end
%     
%     display(s_l2)
%     display(p_l2)

    
    s_l4 = reshape(s_l2, size(s_l2, 1)*size(s_l2, 2), size(s_l2, 3)); 
    p_l4 = reshape(p_l2, size(p_l2, 1)*size(p_l2, 2), 1); 
    
    filter = p_l4 ~= 0; 
    s_l4 = s_l4(filter, :); 
    p_l4 = p_l4(filter); 

%     display(s_l)
%     display(p_l2)
%     display(s_l2)
%     
    display(reshape(linsolve(s_l4, p_l4), [m, m])); 
    

    % construct J coefficients 
    J_l = reshape(linsolve(s_l, dE_l), [m, m]); 
    display(J)
    display(J_l)
%     TimeSpent = toc; 
%     display(TimeSpent)
end

% reconstruction error vs temp 
% new energy 


