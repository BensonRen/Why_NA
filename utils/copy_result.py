# This script is for helping to copy the results from ICML_modulized folders so that they appear in different plots in /home/sr365/NA+Paper_plots

import os
import numpy as np
import shutil
################################
# The worse model one for the  #
################################
"""
dataset_list = ['robotic_arm','ballistics','sine_wave','meta_material']
source_dir_list =  ['/home/sr365/ICML_exp_1st_full_March',
                    '/home/sr365/ICML_exp_worse_10_times',
                    '/home/sr365/ICML_exp_worse_50_times',
                    '/home/sr365/ICML_exp_worse_100_times']
new_name_list = ['(1X)','(10X)','(50X)','(100X)']
dest_dir_mother = '/home/sr365/NA+Paper_plots/compare_worse/'
#dest_dir = os.path.join(dest_dir_mother, 'Random_BP')
#folders_to_copy = ['R10']

#dest_dir = os.path.join(dest_dir_mother, 'Random_FF')
#folders_to_copy = ['R01']
dest_dir = os.path.join(dest_dir_mother, 'Random_BPFF')
folders_to_copy = ['R11']
"""
###############################################
# The regular copy result for individual runs #
###############################################
source_dir = '/home/sr365/ICML_exp_retrain_1'
dest_dir_mother = '/home/sr365/NA+Paper_plots/retrain_1'
#dest_dir = os.path.join(dest_dir_mother, 'R2_FF_stuck')
#folders_to_copy = ['R00','M00','V00','I00','C00','R01','M01','V01','I01','C01']
#dest_dir = os.path.join(dest_dir_mother, 'R3_BP_with_base')
#folders_to_copy = ['R00','M00','V00','I00','C00','R10','M10','V10','I10','C10']
#dest_dir = os.path.join(dest_dir_mother, 'R4_FF_BP_compare')
#folders_to_copy = ['R10','M10','V10','I10','C10','R01','M01','V01','I01','C01']
dest_dir = os.path.join(dest_dir_mother, 'R5_NA_with_BP')
folders_to_copy = ['R10','M10','V10','I10','C10','R11','M11','V11','I11','C11']

# Desolate
#dest_dir = os.path.join(dest_dir_mother, 'R1_comparing_with_baseline')
#dest_dir = os.path.join(dest_dir_mother, 'R6_best_meta')
dataset_list = ['robotic_arm','ballistics','sine_wave','meta_material']
#dataset_list = ['meta_material']
# All the methods: [R M V I c] BP: [0 1] FF:[0 1]
#folders_to_copy = ['R00','M00','V00','I00','C00']
#folders_to_copy = ['R10','M10','V10','I10','C10']
#folders_to_copy = ['R01','M01','V01','I01','C01']
#folders_to_copy = ['R11','M11','V11','I11','C11']

# This part is hand-chosen for the best performing ones in each of the initializer
#dataset_list = ['robotic_arm']
#folders_to_copy = ['R11','M01','V10','I11','C01']

#dataset_list = ['sine_wave']
#folders_to_copy = ['R10','M01','V11','I01','C01']

#dataset_list = ['ballistics']
#folders_to_copy = ['R10','M01','V01','I10','C01']

#dataset_list = ['meta_material']
#folders_to_copy = ['R11','M11','V11','I11','C11']
def decode_folder(code):
    """
    The function to decode the letter-[0,1]-[0,1] code to actual folder name in experiment setting
    :param code: The A-0-0 like code that refers to Method, BP and FF condition
    """
    decode = ''
    # Method part
    if code.startswith('R'):
        decode += 'Random'
    elif code.startswith('M'):
        decode += 'MDN'
    elif code.startswith('V'):
        decode += 'VAE'
    elif code.startswith('I'):
        decode += 'INN'
    elif code.startswith('C'):
        decode += 'cINN'
    else:
        print("Your code is incorrect! Check 1st letter")
        quit()

    # BP part
    if code[1] == '0':
        decode += '_BP_off_'
    elif code[1] == '1':
        decode += '_BP_on_'
    else:
        print("Your code is incorrect! Check 2nd letter")
        quit()

    # FF part
    if code[2] == '0':
        decode += 'FF_off'
    elif code[2] == '1':
        decode += 'FF_on'
    else:
        print("Your code is incorrect! Check 3rd letter")
        quit()

    return decode


def copy_result_files(folders_to_copy, dataset_list, source_dir, dest_dir,  prefix_add_to_dest=''):
    """
    The function that copies the result files (only the mse* ones) to the destination folder
    :param folders_to_copy: The code of the folders to copy
    :param dataset_list: The list of datasets to copy
    :param source_dir: The source directory to copy those
    :param dest_dir: The destination folder
    :param prefix_add_to_dest: The prefix to add to the destination folder (for worse_model)
    """
    for code in folders_to_copy:
        folder = decode_folder(code)
        for dataset in dataset_list:
            # Get the src and dest folders ready
            copy_source = os.path.join(source_dir, folder, dataset)
            copy_dest = os.path.join(dest_dir, prefix_add_to_dest + folder, dataset)
            
            # Creat this folder is not exist for target
            if not os.path.isdir(copy_dest):
                os.makedirs(copy_dest)
            
            # Copy the files with mse in the name
            for file in os.listdir(copy_source):
                if 'mse' not in file:
                    continue
                shutil.copyfile(os.path.join(copy_source, file), os.path.join(copy_dest, file))
            

def copy_worse_model_files(source_dir_list, new_name_list, dest_dir, folders_to_copy, dataset_list):
    """
    The function that copies the result files (mse*) for the worse models trained to plot
    :param source_dir_list: The list of folders to copy, usually a list of X_time_worse folders
    :param new_name_list: The list of new names to assign to those copied folders
    :param dest_dir: The destination directory to copy the results to
    :param dataset_list: The list of datasets to copy
    :param folders_to_copy: The code (decoder above) of the folders to copy
    """
    # Loop over the pair of source dir and new name list
    for source_dir, new_name in zip(source_dir_list, new_name_list):
        print('source dir={}, new name={}'.format(source_dir, new_name))
        copy_result_files(folders_to_copy=folders_to_copy, dataset_list=dataset_list, source_dir=source_dir,
                            dest_dir=dest_dir, prefix_add_to_dest=new_name)
        


if __name__ == '__main__':
    ###############################################
    # The regular copy result for individual runs #
    ###############################################
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    #print(decode_folder('C00'))
    copy_result_files(folders_to_copy=folders_to_copy, dataset_list=dataset_list, source_dir=source_dir, dest_dir=dest_dir)

    ################################
    # The worse model one for the  #
    ################################   
    """
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    copy_worse_model_files(source_dir_list=source_dir_list, new_name_list=new_name_list, dest_dir=dest_dir,
                        folders_to_copy=folders_to_copy, dataset_list=dataset_list)
    """
