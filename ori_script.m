%% Import Script for ODF Data
%
% This script was automatically created by the import wizard. You should
% run the whoole script or parts of it in order to import your data. There
% is no problem in making any changes to this script.

%% Specify Crystal and Specimen Symmetries

% crystal symmetry
CS = crystalSymmetry('m-3m', [3.7 3.7 3.7], 'mineral', 'Iron');

% specimen symmetry
SS = specimenSymmetry('mmm');

% plotting convention
setMTEXpref('xAxisDirection','north');
setMTEXpref('zAxisDirection','outOfPlane');

%% Specify File Names

% path to files
pname = 'L:\DRX_sample_simulations\Industrial_finishing_mill\simulation\postProc';

% which files to be imported
fname = [pname '\MDRX_ori_29000.txt'];

%% Import the Data

% specify kernel
psi = deLaValleePoussinKernel('halfwidth',5*degree);

% load the ODF into the variable odf
odf = ODF.load(fname,CS,SS,'density','kernel',psi,'resolution',5*degree,...
  'interface','generic',...
  'ColumnNames', { 'phi1' 'Phi' 'phi2'}, 'Bunge', 'Radians');

setMTEXpref('FontSize',28);
plot(odf,'phi2',[45]*degree,'contourf','silent','colorrange',[0,14]);
mtexColorMap LaboTeX;
mtexColorbar;
