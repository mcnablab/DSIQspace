% s_ThickenV1.m
%
%
% (c) Qiyuan Tian, McNab Lab, Stanford University
% Spetember 2014

clear, clc, close all
cd(fileparts(which('s_ThickenV1.m')));

%%
files = dir('../*v1_fa.png');
thickpath = 'thickenedimg';
mkdir(thickpath);

for imgNum = 1 : length(files)
    thisFile = files(imgNum);
    imgName = thisFile.name;
    img = imread(fullfile('..', imgName));
    img = im2double(img);
%     figure, imshow(img);
    
    varmap = var(img, 0, 3);
%     figure, imagesc(varmap);
    
    mask = varmap > 0.00018; % look at the final result and select this number
%     figure, imshow(mask);
    
    maskedimg = img .* repmat(mask, [1, 1, 3]);
%     figure, imshow(maskedimg);

    se = strel('disk', 5);
    dilatemask = imdilate(mask, se);
%     figure, imshow(dilatemask)
    
    dilatemaskedimg = imdilate(maskedimg, se);
%     figure, imshow(dilatemaskedimg)

    result = img .* repmat(~dilatemask, [1, 1, 3]) + dilatemaskedimg;
%     figure, imshow(result)

    imwrite( result, fullfile(thickpath, ['thick_' imgName]));
end % end 



















