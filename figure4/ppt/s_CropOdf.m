% s_CropOdf.m
% This script is used to crop PDF images
%
%
% (c) Qiyuan Tian, McNab Lab, Stanford University
% Spetember 2014

clear, clc, close all
cd(fileparts(which('s_CropOdf.m')));

%%
files = dir('../*.png');
croppath = 'croppedimg';
mkdir(croppath);

for imgNum = 1 : length(files)
    thisFile = files(imgNum);
    imgName = thisFile.name;
    img = imread(fullfile('..', imgName));
%     figure, imshow(img);
    
    imgcrop = img(100 : 510, 110 : 480, :);
    imwrite(imgcrop, fullfile(croppath, ['crop_' imgName]));
end % end imgNum