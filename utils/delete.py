import os
import numpy
from utils.create_folder_modulized import create_directory_folder

#input_dir = create_directory_folder
input_dir = '/home/sr365/Why_NA/NA_loss_surface/NA_true_SGD_30k_init/NA_temp'
# This is the program to delete all the duplicate Xtruth Ytruth files generated
#input_dir = '/work/sr365/multi_eval/'                # NIPS code version
#input_dir = '/work/sr365/multi_eval/'                # NIPS code version
#input_dir = '/work/sr365/NA_compare/'                # ICML code version
#input_dir = '/data/users/ben/robotic_stuck/retrain5/'                
#input_dir = '/data/users/ben/multi_eval/'                
###############
# QUAD MACHINE#
###############
#input_dir =  '/home/sr365/ICML_exp/'   # quad
#input_dir = '/home/sr365/ICML_exp_robo/'    # For quad
#input_dir =  '/home/sr365/ICML_MDN/'   # quad
#input_dir =  '/home/sr365/ICML_exp_0402/'   # quad
#input_dir =  '/home/sr365/multi_eval/'   # quad


################
# Groot machine#
################
#input_dir = '/data/users/ben/ICML_exp/'                #  I am Groot!
#input_dir = '/data/users/ben/ICML_exp_mm/'                #  I am Groot!
#input_dir = '/work/sr365/ICML_mm/'                # ICML code version --- MM special
delete_mse_file_mode = True                           # Deleting the mse file for the forward filtering


# For all the architectures
for folders in os.listdir(input_dir):
    #print(folders)
    if not os.path.isdir(os.path.join(input_dir,folders)):
        continue
    # For all the datasets inside it
    for dataset in os.listdir(os.path.join(input_dir, folders)):
        #print(dataset)
        if not os.path.isdir(os.path.join(input_dir, folders, dataset)):
            continue
        current_folder = os.path.join(input_dir, folders, dataset)
        print("current folder is:", current_folder)
        for file in os.listdir(current_folder):
            current_file = os.path.join(current_folder, file)
            if os.path.getsize(current_file) == 0:
                print('deleting file {} due to empty'.format(current_file))
                os.remove(current_file)
            elif '_Ytruth_' in file:
                if 'ce0.csv' in file or 'NA' in folders:
                    os.rename(current_file, os.path.join(current_folder, 'Ytruth.csv'))
                else:
                    os.remove(current_file)
            elif '_Xtruth_' in file:
                if 'ce0.csv' in file or 'NA' in folders:
                    os.rename(current_file, os.path.join(current_folder, 'Xtruth.csv'))
                else:
                    os.remove(current_file)
            elif '_Ypred_' in file and file.endswith(dataset + '.csv'):
                os.rename(current_file, os.path.join(current_folder, 'Ypred.csv'))
            elif '_Xpred_' in file and file.endswith(dataset + '.csv'):
                os.rename(current_file, os.path.join(current_folder, 'Xpred.csv'))
            if delete_mse_file_mode and 'mse_' in file:
                os.remove(current_file)
                
            

            
