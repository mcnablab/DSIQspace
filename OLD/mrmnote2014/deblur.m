clear, clc, close all 

load('PDF_PSF.mat');

%%
PDF = pdf(1, 1, 1, :, :, :);
PDF = squeeze(PDF);
% idx = PDF < (max(PDF(:))/15);
% PDF(idx) = max(PDF(:));
%%
PDFdeconv = deconvlucy(PDF, PSF .* mask / sum(sum(sum(PSF .* mask))));
%PDFdeconv = deconvwnr(PDF, PSF .* mask, 10);
%PDFdeconv = deconvreg(PDF, PSF .* mask);
%%
PDFslice = PDF(100, :, :);
imagesc(squeeze(PDFslice / max(PDFslice(:))))
axis square

%%
PDFslice = PDFdeconv(:, :, 100);
figure, imagesc(PDFslice / max(PDFslice(:)))
axis square

%%
PSFmask = mask .* PSF;
PSFslice = PSFmask(:, :, 100);
figure, imagesc(PDFslice / max(PDFslice(:)))
axis square

%%
PSFline = PSFsmall(:, 17, 17);
plot(PSFline)

%% mask
mask = zeros(201, 201, 201);
for ii = -100 : 100
    for jj = -100 : 100
        for kk = -100 : 100
            if ii*ii + jj*jj + kk*kk <= 17 * 17
                mask(ii+101,jj+101,kk+101)=1;
            end
        end
    end
end
%%
PSFmask = PSF .* mask;
PSFsmall = PSFmask(100-17:100+17, 100-17:100+17, 100-17:100+17);
