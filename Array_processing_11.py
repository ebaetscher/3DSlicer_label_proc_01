# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 12:52:20 2017

@author: baetscer
"""
#array processing for by-slice

import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
from glob import glob

print("\n")
print("Working directory:")
print(os.getcwd())
new_dir = input("New working dir:\n")
os.chdir(str(new_dir))
print("Directory contents:")
print(os.listdir(os.getcwd()))
dir_contents = os.listdir(os.getcwd())

#label_vol_arr_name = input("file name of label volume array:\n")
#label_vol_arr = np.load(str(label_vol_arr_name))
#label_vol_title = label_vol_arr_name[0:-4]

label_vol_arrs = []
num_arrs_in_dir = len(dir_contents)
i = 0
for i in range(num_arrs_in_dir):
    label_vol_arrs.append(np.load(dir_contents[i]))

label_vol_title = 'All full segmented'
figure_save_name1 = (str(label_vol_title)+'_by_slice.png')
figure_save_name2 = (str(label_vol_title)+'_sub_samp_dists.png')



#print("Shape of loaded array")
#print(np.shape(label_vol_arr))
#print("Max value of loaded array")
#print(np.max(label_vol_arr))
arr_counter = 0
for arr_counter in range(len(label_vol_arrs)):
    num_slices = int(np.shape(label_vol_arrs[arr_counter])[0])
    print(dir_contents[arr_counter])
    print("Number of slices in volume:")
    print(num_slices)    
    
    j = range(num_slices)
    i = 0
    list_of_slice_arrs = []
    for i in j:
        list_of_slice_arrs.append(label_vol_arrs[arr_counter][i,:,:])

#print("Number of slices in list:")
#print(len(list_of_slice_arrs))

    total_ab_per_slice = []
    i = 0
    for i in j:
        (ab_per_slice_temp, bins_temp) = np.histogram(list_of_slice_arrs[i], bins=[1, 2, 3, 4, 5])
        total_ab_per_slice.append(np.sum(ab_per_slice_temp))

    list_of_label_counts = []
    i = 0
    for i in j:
        (counts, bins) = np.histogram(list_of_slice_arrs[i], bins=[1, 2, 3, 4, 5])
        list_of_label_counts.append(counts)
    
    arr_of_counts = np.vstack(list_of_label_counts)
    arr_of_mm3 = (arr_of_counts*9.4)
#print(arr_of_counts)
    file_name_pfix0 = dir_contents[arr_counter]
    file_name_pfix = file_name_pfix0[:11]
    file_name = (file_name_pfix + '_mm3.csv')    
    np.savetxt(file_name, arr_of_mm3, delimiter=",")

#%%

    SAT_pcts = []
    Musc_pcts = []
    Organ_pcts = []
    VAT_pcts = []
    generated_pcts = []

    i = 0
    k = 0
    def generate_pcts(arr_of_counts, k):
        i = 0
        generated_pcts = []
        for i in j:
            if total_ab_per_slice[i] != 0:
                generated_pcts.append(float(arr_of_counts[i,k])/float(total_ab_per_slice[i])*100)
            else:
                pass
        return generated_pcts
    
    SAT_pcts = generate_pcts(arr_of_counts, 0)
    Musc_pcts = generate_pcts(arr_of_counts, 1)
    Organ_pcts = generate_pcts(arr_of_counts, 2)
    VAT_pcts = generate_pcts(arr_of_counts, 3)

#print(SAT_pcts)
#print(Musc_pcts)
#print(Organ_pcts)
#print(VAT_pcts)

#overall means
    total_SAT_pct = 0.0
    total_Musc_pct = 0.0
    total_Organ_pct = 0.0
    total_VAT_pct = 0.0

    (hist_segged_voxels, bins) = np.histogram(label_vol_arrs[arr_counter], bins=[1,2,3,4,5])
#print(hist_segged_voxels)
    total_num_seg_vox = np.sum(hist_segged_voxels)

    total_SAT_pct = (float(hist_segged_voxels[0])/float(total_num_seg_vox)*100)
    total_Musc_pct = (float(hist_segged_voxels[1])/float(total_num_seg_vox)*100)
    total_Organ_pct = (float(hist_segged_voxels[2])/float(total_num_seg_vox)*100)
    total_VAT_pct = (float(hist_segged_voxels[3])/float(total_num_seg_vox)*100)


    number_seg_slices = len(SAT_pcts)
    seg_slice_range = range(number_seg_slices)

#total_SAT_pct_for_plot = []
#total_Musc_pct_for_plot = []
#total_Organ_pct_for_plot = []
#total_VAT_pct_for_plot = []
#
#i = 0
#def extend_total_pcts_for_plots(total_SAT_pct, seg_slice_range):
#    for i in seg_slice_range:
        

##%%

    plt.subplots_adjust(left=0.2, bottom=0.2, right=1.6, top=3.2, wspace=0.2, hspace=0.3)
    #fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(20, 30))
    #plt.suptitle(label_vol_title)

    plt.subplot(4, 1, 1)
    plt.plot(seg_slice_range, SAT_pcts, 'go')
    plt.axhline(y=total_SAT_pct, xmin=0, xmax=number_seg_slices, linewidth=2, ls='-.', color = 'k')
    plt.title('Percentages by slice')
    plt.ylabel('Pct. of total abdominal')
    plt.title('SAT')

    plt.subplot(4, 1, 2)
    plt.plot(seg_slice_range, Musc_pcts, 'bo')
    plt.axhline(y=total_Musc_pct, xmin=0, xmax=number_seg_slices, linewidth=2, ls='-.', color = 'k')
    plt.xlabel('Slice number')
    plt.ylabel('Pct. of total abdominal')
    plt.title('Muscle')
    
    plt.subplot(4, 1, 3)
    plt.plot(seg_slice_range, Organ_pcts, 'ro')
    plt.axhline(y=total_Organ_pct, xmin=0, xmax=number_seg_slices, linewidth=2, ls='-.', color = 'k')
    plt.ylabel('Pct. of total abdominal')
    plt.title('Organ')

    plt.subplot(4, 1, 4)
    plt.plot(seg_slice_range, VAT_pcts, 'yo')
    plt.axhline(y=total_VAT_pct, xmin=0, xmax=number_seg_slices, linewidth=2, ls='-.', color = 'k')
    plt.ylabel('Pct. of total abdominal')
    plt.title('VAT')

#plt.suptitle(label_vol_title)  
#fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(20, 30))
#plt.savefig(figure_save_name1)
plt.show()

#%%
#uniform sampling

list_of_samples_SAT = []
list_of_samples_Musc = []
list_of_samples_Organ = []
list_of_samples_VAT = []
list_of_samples_temp = []

range_of_seg_slices = range(number_seg_slices)
num_samples = 0
range_num_samples = []
seed1 = 0
step_size = 0

#SAT_pcts
#Musc_pcts
#Organ_pcts
#VAT_pcts

def uniform_sampler1(SAT_pcts, num_samples, seed1):
    step_size = (int(number_seg_slices/num_samples))    
    list_of_samples_temp = (SAT_pcts[seed1:number_seg_slices:step_size])
    return list_of_samples_temp
        
#list_of_samples_SAT.append(uniform_sampler1(SAT_pcts, 4, 0))
#print(list_of_samples_SAT)

i = 0
for i in range_of_seg_slices:
    num_samples = (i+1)
    list_of_samples_SAT.append(uniform_sampler1(SAT_pcts, num_samples, seed1))

i = 0
for i in range_of_seg_slices:
    num_samples = (i+1)
    list_of_samples_Musc.append(uniform_sampler1(Musc_pcts, num_samples, seed1))

i = 0
for i in range_of_seg_slices:
    num_samples = (i+1)
    list_of_samples_Organ.append(uniform_sampler1(Organ_pcts, num_samples, seed1))
    
i = 0
for i in range_of_seg_slices:
    num_samples = (i+1)
    list_of_samples_VAT.append(uniform_sampler1(VAT_pcts, num_samples, seed1))
    
mean_pct_by_slice_SAT = []
pct_StDev_by_slice_SAT = []
mean_pct_by_slice_Musc = []
pct_StDev_by_slice_Musc = []
mean_pct_by_slice_Organ = []
pct_StDev_by_slice_Organ = []
mean_pct_by_slice_VAT = []
pct_StDev_by_slice_VAT = []

i = 0
for i in range_of_seg_slices:
    mean_pct_by_slice_SAT.append(np.mean(list_of_samples_SAT[i]))
i = 0
for i in range_of_seg_slices:
    mean_pct_by_slice_Musc.append(np.mean(list_of_samples_Musc[i]))
i = 0
for i in range_of_seg_slices:
    mean_pct_by_slice_Organ.append(np.mean(list_of_samples_Organ[i]))
i = 0
for i in range_of_seg_slices:
    mean_pct_by_slice_VAT.append(np.mean(list_of_samples_VAT[i]))
    
i = 0
for i in range_of_seg_slices:
    pct_StDev_by_slice_SAT.append(np.std(list_of_samples_SAT[i]))
i = 0
for i in range_of_seg_slices:
    pct_StDev_by_slice_Musc.append(np.std(list_of_samples_Musc[i]))
i = 0
for i in range_of_seg_slices:
    pct_StDev_by_slice_Organ.append(np.std(list_of_samples_Organ[i]))
i = 0
for i in range_of_seg_slices:
    pct_StDev_by_slice_VAT.append(np.std(list_of_samples_VAT[i]))
    

#%%

#plt.subplots_adjust(left=0.2, bottom=0.2, right=1.6, top=4.2, wspace=0.2, hspace=0.3)
#meanlineprops = dict(linestyle='--', linewidth=1.5, color='green')
#
#fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(20, 30))   
#
#plt.suptitle(label_vol_title)
#
#axes[0].plot(list_of_samples_SAT)
#axes[0].set_title('SAT')
#axes[0].axhline(y=total_SAT_pct, xmin=0, xmax=38, linewidth=2, ls='-.', color = 'k')
#
#axes[1].plot(list_of_samples_Musc)
#axes[1].set_title('Muscle')
#axes[1].axhline(y=total_Musc_pct, xmin=0, xmax=38, linewidth=2, ls='-.', color = 'k')
#
#axes[2].plot(list_of_samples_Organ)
#axes[2].set_title('Organ')
#axes[2].axhline(y=total_Organ_pct, xmin=0, xmax=38, linewidth=2, ls='-.', color = 'k')
#    
#axes[3].plot(list_of_samples_VAT)
#axes[3].set_title('VAT')    
#axes[3].axhline(y=total_VAT_pct, xmin=0, xmax=38, linewidth=2, ls='-.', color = 'k')
#
#plt.savefig(figure_save_name2)
#plt.show()

#print(list_of_samples_SAT)
#print(list_of_samples_Musc)
#print(list_of_samples_Organ)
#print(list_of_samples_VAT)

#plt.violinplot(SAT_pcts, showmeans=True, showmedians=False)
#plt.show()
#
#plt.violinplot(Musc_pcts, showmeans=True, showmedians=False)
#plt.show()
#
#plt.violinplot(Organ_pcts, showmeans=True, showmedians=False)
#plt.show()
#
#plt.violinplot(VAT_pcts, showmeans=True, showmedians=False)
#plt.show()
 
#plt.subplots_adjust(left=0.2, bottom=0.2, right=1.6, top=3.2, wspace=0.2, hspace=0.3)
#
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(20, 30))
plt.suptitle(label_vol_title)

plt.subplot(4, 1, 1)
i = 0
for i in range_of_seg_slices:
    plt.plot(seg_slice_range[i], mean_pct_by_slice_SAT[i], 'go')
    plt.errorbar(seg_slice_range[i], mean_pct_by_slice_SAT[i], yerr=pct_StDev_by_slice_SAT[i], fmt='-go')
plt.axhline(y=total_SAT_pct, xmin=0, xmax=38, linewidth=2, ls='-.', color = 'k')
plt.title('Percentages by slice')
plt.ylabel('Pct. of total abdominal')

plt.subplot(4, 1, 2)
i = 0
for i in range_of_seg_slices:
    plt.plot(seg_slice_range[i], mean_pct_by_slice_Musc[i], 'bo')
    plt.errorbar(seg_slice_range[i], mean_pct_by_slice_Musc[i], yerr=pct_StDev_by_slice_Musc[i], fmt='-bo')
plt.axhline(y=total_Musc_pct, xmin=0, xmax=38, linewidth=2, ls='-.', color = 'k')
plt.xlabel('Slice number')
plt.ylabel('Pct. of total abdominal')

plt.subplot(4, 1, 3)
i = 0
for i in range_of_seg_slices:
    plt.plot(seg_slice_range[i], mean_pct_by_slice_Organ[i], 'ro')
    plt.errorbar(seg_slice_range[i], mean_pct_by_slice_Organ[i], yerr=pct_StDev_by_slice_Organ[i], fmt='-ro')
plt.axhline(y=total_Organ_pct, xmin=0, xmax=38, linewidth=2, ls='-.', color = 'k')
plt.ylabel('Pct. of total abdominal')

plt.subplot(4, 1, 4)
i = 0
for i in range_of_seg_slices:
    plt.plot(seg_slice_range[i], mean_pct_by_slice_VAT[i], 'yo')
    plt.errorbar(seg_slice_range[i], mean_pct_by_slice_VAT[i], yerr=pct_StDev_by_slice_VAT[i], fmt='-yo')
plt.axhline(y=total_VAT_pct, xmin=0, xmax=38, linewidth=2, ls='-.', color = 'k')
plt.ylabel('Pct. of total abdominal')

plt.savefig(figure_save_name2)
plt.show()

