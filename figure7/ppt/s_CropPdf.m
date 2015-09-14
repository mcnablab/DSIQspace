% s_CropPdf.m
% This script is used to crop PDF images
%
%
% (c) Qiyuan Tian, McNab Lab, Stanford University
% Spetember 2014

clear, clc, close all
cd(fileparts(which('s_CropPdf.m')));

%%
files = dir('../*pdf*.png');
croppath = 'croppedimg';
mkdir(croppath);

for imgNum = 1 : length(files)
    thisFile = files(imgNum);
    imgName = thisFile.name;
    img = imread(fullfile('..', imgName));
    
    imgcrop = img(241 : 2100, 916 : 2776, :);
    imwrite(imgcrop, fullfile(croppath, ['crop_' imgName]));
end % end imgNum