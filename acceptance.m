function a = acceptance(x_new, x_cur, J, c)
    e_new = energy(x_new, J);  
    e_cur = energy(x_cur, J); 
    p_ratio = exp(-(e_new - e_cur) / c);
    a = min(1, p_ratio); 
end