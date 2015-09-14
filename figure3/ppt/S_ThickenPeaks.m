% s_ThickenPeaks.m
%
%
% (c) Qiyuan Tian, McNab Lab, Stanford University
% Spetember 2014

clear, clc, close all
cd(fileparts(which('s_ThickenPeaks.m')));

%%
files = dir('../*odfpeaks*.png');
thickpath = 'thickenedimg';
mkdir(thickpath);

for imgNum = 1 : length(files)
    thisFile = files(imgNum);
    imgName = thisFile.name;
    img = imread(fullfile('..', imgName));
    
    se = strel('disk', 4);
    dilateimg = imdilate(img, se);

    imwrite( dilateimg, fullfile(thickpath, ['thick_' imgName]));
end % end imgNum