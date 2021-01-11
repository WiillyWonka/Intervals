function [c_inf, c_sup] = dot(A_inf, A_sup, x_inf, x_sup)
c_inf = zeros([size(A_inf, 1), 1]);
c_sup = zeros([size(A_inf, 1), 1]);
for i=1:length(c_inf)
    for j=1:size(A_inf, 2)
        [inf, sup] = mul(A_inf(i, j), A_sup(i, j), x_inf(j), x_sup(j));
        [c_inf(i), c_sup(i)] = add(c_inf(i), c_sup(i), inf, sup);
    end
end
end

function [inf, sup] = mul(inf1, sup1, inf2, sup2)
    inf = min([inf1 * inf2, inf1 * sup2, sup1 * inf2, sup1 * sup2]);
    sup = max([inf1 * inf2, inf1 * sup2, sup1 * inf2, sup1 * sup2]);
end

function [inf, sup] = add(inf1, sup1, inf2, sup2)
    inf = inf1 + inf2;
    sup = sup1 + sup2;
end