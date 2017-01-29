% initiate weight matrix and initial state
m = 5; 
kb = physconst('Boltzmann'); 
T = 310; 

J_temp = normrnd(0, 1, m);
J = triu(J_temp) + triu(J_temp,1)';
J(1:m+1:end) = 0; 
% display(J)

% display(x_0)

% imagesc(J)
% colormap hot
% colorbar

% check results by finding lowest energy for every possible x
[x_eq, energy_x_eq] = check_eq(m, J); 
% display(x_eq)
% display(energy_x_eq)

landscape = energy_landscape(m, J); 

iter = 5; 
repeat = 5000; 
dist_array = zeros(2^m, 1); 
equal = 0; 


for r = 1:repeat
    x_0 = binornd(1, 0.5, 1, m); 
    x_0 = 2 * x_0 - 1;
    e_0 = energy(x_0, J); 
    x_cur = x_0; 
    
%     x_array = zeros((iter*m), m); 
%     energy_array = zeros((iter*m), 1); 

    x_array = zeros(iter, m); 
    energy_array = zeros(iter, 1);
    
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

%             x_array((i-1)*(m)+j,:) = x_cur; 
%             energy_array((i-1)*(m)+j, 1) = energy(x_cur, J);
%             
            x_array(i,:) = x_cur; 
            energy_array(i, 1) = energy(x_cur, J);

        end
    end
    
    equal = equal + (isequal(x_eq(1,:), x_cur) || isequal(x_eq(2,:), x_cur));

    dist_array(bi2de((x_cur+1)/2) + 1, 1) = ...
        dist_array(bi2de((x_cur+1)/2) + 1, 1) + 1; 
end

x_array = vertcat(x_0, x_array);
energy_array = vertcat(e_0, energy_array); 

% display(size(x_array))
% display(size(energy_array))

% plot state and energy over each iteration of metropolis
figure 
subplot(3, 4, 1:3)
imagesc(transpose(x_array))
colormap hot
% xlim([1, m*iter])
xlim([1, iter])


subplot(3, 4, 4)
imagesc(transpose(x_eq)); axis off
colormap gray
colorbar
text(2.5, 2, sprintf(['energy = \n' num2str(energy_x_eq)]))

subplot(3, 4, 5:7)
plot(transpose(energy_array))
text(iter, energy_array(end) + 2, ...
    sprintf(['energy = \n' num2str(energy_array(end))]))
% xlim([1, m*iter])
xlim([1, iter])

subplot(3, 4, 9:10)
bar0 = bar(dist_array); hold on
x1 = (bi2de((x_eq(1,:)+1)/2) + 1); 
x2 = (bi2de((x_eq(2,:)+1)/2) + 1); 

bar1 = bar(x1, dist_array(x1), 'r'); 
bar2 = bar(x2, dist_array(x2), 'r'); 
str = {'true'; 'true'};
display([(bi2de((x_eq(1,:)+1)/2) + 1) (bi2de((x_eq(2,:)+1)/2) + 1)])
text(2^m, 1, num2str(equal))

set(bar0,'edgecolor','none');
set(bar1,'edgecolor','none');
set(bar2,'edgecolor','none');

subplot(3, 4, 11:12)
plot(landscape)

% display(x_array(end,:))
% display(energy_array(end))












