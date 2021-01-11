clear all; clc

A_inf = [
    4 -9 0 2 5 -23 15;
    0 6 -1 -1 -5 1 -3;
    0 -20 12 -6 0 -18 0;
    -4 -1 -3 3 5 1 1;
    0 0 0 -1 8 -6 10;
    -7 1 7 -3 0 3 -2;
    -1 -3 0 1 -5 2 6
    ];
A_sup = [
    6 0 12 3 9 -9 23;
    1 10 1 3 1 15 -1;
    3 -9 77 30 3 1 1;
    1 1 1 5 9 2 4;
    3 6 20 5 14 1 17;
    -2 2 14 1 2 5 1;
    5 2 8 11 10 7 82;
];
b_inf = [-10 35 -6 30 4 -6 -2];
b_sup = [95 14 2 7 95 46 65];
A(:, :, 1) = A_inf;
A(:, :, 2) = A_sup;
b = zeros(size(A,1), 2);
b(:, 1) = b_inf;
b(:, 2) = b_sup;

% 2D plot
tau_values = 0.5:0.001:1.0;
% n = length(tau_values);
% ni_values = zeros(1, n);
% 
% for i = 1:n
%     [x, ni] = subdiff(A, b, tau_values(i), false);
%     ni_values(i) = ni;
% end
% plot(tau_values, ni_values);
% hold on;

% A(7, 7, 1) = 8;
% for i = 1:n
%     [x, ni] = subdiff(A, b, tau_values(i), false);
%     ni_values(i) = ni;
% end
% plot(tau_values, ni_values);
% 
% A(7, 7, 1) = 10;
% for i = 1:n
%     [x, ni] = subdiff(A, b, tau_values(i), false);
%     ni_values(i) = ni;
% end
% plot(tau_values, ni_values);
% 
% A(7, 7, 1) = 12.8;
% for i = 1:n
%     [x, ni] = subdiff(A, b, tau_values(i), false);
%     ni_values(i) = ni;
% end
% plot(tau_values, ni_values);
% xlabel('$\tau$', 'interpreter', 'latex');
% ylabel('iterations');
% legend('$\gamma = 6$', ...
%     '$\gamma = 8$', ...
%     '$\gamma = 10$', ...
%     '$\gamma = 12.8$', 'interpreter','latex');
% saveas(gcf,'1.png')
% hold off;
% figure;
% 
% % Animation
% g = 6:0.05:14;
% nr_fr = length(g);
% frames = moviein(nr_fr); 
% writerObj = VideoWriter('2.avi');
% writerObj.FrameRate = 2;
% open(writerObj);
% for i = 1 : nr_fr
%     A(7, 7, 1) = g(i);
%     for k = 1:n
%         [x, ni] = subdiff(A, b, tau_values(k), false);
%         ni_values(k) = ni;
%     end
%     plot(tau_values, ni_values);
%     xlabel('$\tau$', 'interpreter', 'latex');
%     ylabel('iterations');
%     title(sprintf('$\\gamma = $ %f', g(i)), 'interpreter','latex');
%     writeVideo(writerObj, getframe(gcf));
% end
% close(writerObj);
% figure;

g = 8.6;
A(7, 7, 1) = g;
A_inf(7, 7) = g;
[x0, ni] = subdiff(A, b, 0.9, true, false);

% g1 = 8.5;
% A(7, 7, 1) = g1;
% A_inf(7, 7) = g1;
% [x, ni] = subdiff(A, b, 0.9, true, true, x);
% 
% x_inf = x(1:length(x)/2);
% x_sup = x(length(x)/2 + 1:length(x));
% 
% x1 = zeros(2*length(x_inf), 1);
% for i=1:length(x_inf)
%    x1(2*i - 1) = x_inf(i);
%    x1(2*i) = x_sup(i);
% end

% figure
% hold on
% [c_inf, c_sup] = dot(A_inf, A_sup, x_inf, x_sup);
% plot(c_inf)
% plot(c_sup)
% plot(b_inf)
% plot(b_sup)
% 
% legend('Ax_{inf}', 'Ax_{sup}', 'b_{inf}', 'b_{sup}')

% % 3D plot
g = 7.50:0.01:9.4;
tau_values = 0.75:0.01:1.0;
[T, G] = meshgrid(tau_values, g);
N = zeros(size(T));
for i = 1:size(T, 1)
    for j = 1:size(T, 2)
        A(7, 7, 1) = G(i, j);
        [x, ni] = subdiff(A, b, 0.9, false, true, x0);
        N(i, j) = ni;
%         fprintf('%i\n', 100*(i + j)/(size(T, 1) + size(T, 2)))
    end
%     disp(i)
end
% 
% for i=1:size(N, 1)
%     for j=1:size(N,2)
%         if (N(i, j) == 1000)
%             N(i, j) = 0;
%         end
%     end
% end
% 
% heatmap(tau_values, g, N)
imagesc(tau_values, g, N)
xlabel('$\tau$', 'interpreter', 'latex');
ylabel('$\gamma$', 'interpreter', 'latex');
colorbar
% figure
% surf(T, G, N);
% xlabel('$\tau$', 'interpreter', 'latex');
% ylabel('$\gamma$', 'interpreter', 'latex');
% zlabel('iterations');