# This script is for helping to copy the results from ICML_modulized folders so that they appear in different plots in /home/sr365/NA+Paper_plots

import os
import numpy as np
import shutil

source_dir = '/home/sr365/ICML_exp'
dest_dir = '/home/sr365/NA+Paper_plots/R6_best_ball'

#dataset_list = ['robotic_arm','ballistics','sine_wave']
# All the methods: [R M V I c] BP: [0 1] FF:[0 1]
#folders_to_copy = ['R00','M00','V00','I00','C00']
#folders_to_copy = ['R10','M10','V10','I10','C10']
#folders_to_copy = ['R01','M01','V01','I01','C01']
#folders_to_copy = ['R11','M11','V11','I11','C11']


#dataset_list = ['robotic_arm']
#folders_to_copy = ['R11','M01','V10','I11','C01']

#dataset_list = ['sine_wave']
#folders_to_copy = ['R10','M01','V11','I01','C01']

dataset_list = ['ballistics']
folders_to_copy = ['R10','M01','V01','I10','C01']

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


def copy_result_files():
    """
    The function that copies the result files (only the mse* ones) to the destination folder
    """
    for code in folders_to_copy:
        folder = decode_folder(code)
        for dataset in dataset_list:
            # Get the src and dest folders ready
            copy_source = os.path.join(source_dir, folder, dataset)
            copy_dest = os.path.join(dest_dir, folder, dataset)
            
            # Creat this folder is not exist for target
            if not os.path.isdir(copy_dest):
                os.makedirs(copy_dest)
            
            # Copy the files with mse in the name
            for file in os.listdir(copy_source):
                if 'mse' not in file:
                    continue
                shutil.copyfile(os.path.join(copy_source, file), os.path.join(copy_dest, file))
            

if __name__ == '__main__':
    #print(decode_folder('C00'))
    copy_result_files()