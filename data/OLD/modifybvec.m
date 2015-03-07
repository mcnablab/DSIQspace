clear, clc, close all

bvecs = importdata('DSI11_exvivo_bvecs.txt');
tmp = bvecs(:, 2);
bvecs(:, 2) = bvecs(:, 3);
bvecs(:, 3) = -tmp;
dlmwrite('DSI11_exvivo_bvecslala.txt', bvecs, 'delimiter', ' ');

