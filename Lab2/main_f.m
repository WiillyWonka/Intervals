clear all; clc;

% % bar for solution
% X = intval([infsup(-30, 30), infsup(-30, 30)]);
% % Rosenbrock function
% [Z, WorkList, diameter] = globopt0(X);
% iter = 1:1:length(diameter);
% plot(iter, diameter);
% hold on;
% xlim([0, length(diameter)]);
% xlabel('Iterations');
% ylabel('Diameter');
% path = 'D:\Intervals local\Lab2\fig';
% full_title = 'rosenbrock';
% saveas(gcf, fullfile(path, char(full_title)), 'png'); 
% 
% 
% for i = 1:30
%     disp(WorkList(i).Box);
%     s = ['f(y) = ', num2str(WorkList(i).Estim)];
%     disp(s);
% end

% Schaffer function
X = intval([infsup(-50, 50), infsup(-50, 50)]);
[Z, WorkList, diameter] = globopt0(X);
solution = 0;

answer = [];
for i = 1 : length(WorkList)
    answer(i) = WorkList(i).Estim;
end

for i = 1:length(answer)
    diff(i) = abs(answer(i) - solution);
end

iter = 1:1:length(answer);

figure
semilogx(iter, diff);
hold on;
xlim([0, length(answer)]);
xlabel('Iterations');
ylabel('Abs error');
path = 'D:\Intervals local\Lab2\fig';
full_title = 'convergence';
saveas(gcf, fullfile(path, char(full_title)), 'png'); 