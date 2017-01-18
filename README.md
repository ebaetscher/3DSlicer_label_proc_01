# 3DSlicer_label_proc_01
Process segmentation label maps generated in 3D slicer for Volumetrics intialy - python

We start with a label map volume in 3D Slicer. This is something we would have after someone was doing segmentation of structures on a medical image, for example.

We want to know some things about the data in the label map. Slicer already has some of this functionality built-in. See the module "LabelStatistics" under "Quantification". 

We especially want to know things about the label map on a per-slice basis.

The intial data-set for which this code will be written is a relatively narrow case, and I won't worry much about general usage of the code at first. This is because I am on a deadline and more general code is almost always more challenging.

We have one axial T1-weighted abdominal MRI scan for each of around 100 research participants, over three time points.
These image volumes typically have between 45 and 65 "slices".
Of these we have segmentation data for 11 slices (or more).
The particular 11 slices are carefully chosen, however they are chosen with respect to annatomy in the images rather than the volume dimensions. That being the case, we will assume no a priori knowlege of which slices contain segmentation.

First though, we will treat volumes for which we have full segmentation and want to subsample the segmentation volume to look for convergence to the mean of all the slicer for each segmentated MRI study. 
