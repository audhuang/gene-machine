function dist_array = metropolis_boltzmann(J, T, iter, repeat)
    m = size(J, 1); 
    [x_eq, energy_x_eq] = check_eq(m, J);
    landscape = energy_landscape(m, J); 

    dist_array = zeros(2^m, 1); 
    equal = 0; 

    for r = 1:repeat
        x_0 = binornd(1, 0.5, 1, m); 
        x_0 = 2 * x_0 - 1;
        e_0 = energy(x_0, J); 
        x_cur = x_0; 

        x_array = zeros(iter, m); 
        energy_array = zeros(iter, 1);

        for i=1:iter
            j = randi([1, m]); 

            x_new = x_cur; 
            x_new(1, j) = -x_cur(1, j); 

            a = acceptance(x_new, x_cur, J, T); 
            q = unifrnd(0, 1); 

            if q <= a 
                x_cur = x_new; 
            end

            x_array(i,:) = x_cur; 
            energy_array(i, 1) = energy(x_cur, J);
        end

        equal = equal + (isequal(x_eq(1,:), x_cur) || isequal(x_eq(2,:), x_cur));

        ind = bi2de(fliplr(x_cur+1)/2) + 1; 
        dist_array(ind, 1) = dist_array(ind, 1) + 1; 
    end

    x_array = vertcat(x_0, x_array);
    energy_array = vertcat(e_0, energy_array); 


    % plot state and energy over each iteration of metropolis
    figure 
    subplot(4, 4, 1:3)
    imagesc(transpose(x_array))
    colormap hot
    xlim([1, iter])
    title(sprintf(['States Over ' num2str(iter) ' Iterations in One Trial']))
    ylabel('state')

    subplot(4, 4, 4)
    imagesc(transpose(x_eq)); axis off
    colormap gray
    colorbar
    % text(2.5, 2, sprintf(['energy = \n' num2str(energy_x_eq)]))
    title(sprintf(['Lowest Energy States\nEnergy = ' num2str(energy_x_eq)]))

    subplot(4, 4, 5:7)
    plot(transpose(energy_array))
    text(iter, energy_array(end) + 2, ...
        sprintf(['energy = \n' num2str(energy_array(end))]))
    % xlim([1, m*iter])
    xlim([1, iter])
    title(sprintf(['Energy Over ' num2str(iter) ' Iterations in One Trial']))
    ylabel('energy')

    subplot(4, 4, 9:12)
    bar0 = bar(dist_array); hold on
    x1 = (bi2de((fliplr(x_eq(1,:))+1)/2) + 1); 
    x2 = (bi2de((fliplr(x_eq(2,:))+1)/2) + 1); 

    bar1 = bar(x1, dist_array(x1), 'r'); 
    bar2 = bar(x2, dist_array(x2), 'r'); 
    str = {'true'; 'true'};
    display([x1 x2])
    % text(2^m, 1, num2str(equal))
    xlim([0, 2^m-1])

    set(bar0,'edgecolor','none');
    set(bar1,'edgecolor','none');
    set(bar2,'edgecolor','none');
    title(sprintf(['Distribution of States, '...
        num2str(equal) ' true (red) out of ' num2str(repeat) ' trials '])) 
    ylabel('number')
    xlabel('state')

    subplot(4, 4, 13:16)
    plot(transpose(landscape))
    xlim([0, 2^m-1])
    title('Energy Landscape Over All States')
    xlabel('state')
    ylabel('energy')
    display(x_eq)
end
% display(x_array(end,:))
% display(energy_array(end))












