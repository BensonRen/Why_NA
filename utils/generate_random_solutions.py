# This function serves as a random solution generator for modulized inverse solution generator.

# Import standar lib
import numpy as np
import pandas as ipd
import os
import shutil
# Own module
from utils.create_folder_modulized import get_folder_modulized
from utils.helper_functions import simulator
from Simulated_DataSets.Meta_material_Neural_Simulator.generate_mm_x import generate_meta_material

dataset_list = ['meta_material','robotic_arm','sine_wave','ballistics']
#dataset_list = ['robotic_arm']
#dataset_list = ['robotic_arm','sine_wave','ballistics']
#dataset_list = ["sine_wave"]
#dataset_list = ["meta_material"]
#dataset_list = ["meta_material","sine_wave"]
data_num_base = 1000
trail_num = 2048

meta_data_num = 500

# Where to steal the Xtruth, Ytruth file (This function can not produce Xtruth and Ytruth as it is just a random generator. However the evaluation needs a Xtruth and Ytruth file, therefore we are just going to steal the Truth files from the neighbouring folder
#truth_folder = '/work/sr365/ICML_mm/cINN_BP_off_FF_off/'
#truth_folder = '/work/sr365/ICML_exp/cINN_BP_off_FF_off/'

#truth_folder = '/data/users/ben/ICML_exp_mm/cINN_BP_off_FF_off/' # I am Groot!
truth_folder =  '/home/sr365/ICML_exp_0402/cINN_BP_off_FF_off/'   # quad
#truth_folder =  '/home/sr365/ICML_exp/cINN_BP_off_FF_off/'   # quad

def generate_sine_wave(data_num):
    return np.random.uniform(size=(data_num,2), low=-1, high=1)

def generate_ballistics(data_num):
    numpy_geometry = np.zeros([data_num, 4])
    numpy_geometry[:, 0] = np.random.normal(0, 0.5, size=[data_num,])
    numpy_geometry[:, 1] = np.max(np.random.normal(1.5, 0.5, size=[data_num,]), 0)
    numpy_geometry[:, 2] = np.radians(np.random.uniform(9, 81, size=[data_num,]))
    numpy_geometry[:, 3] = np.random.poisson(15, size=[data_num,]) / 15
    return numpy_geometry

def generate_robotic_arm(data_num):
    numpy_geometry = np.random.normal(0, 0.5, size=[data_num, 4])
    numpy_geometry[:, 0] /= 2
    return numpy_geometry 

def check_if_empty_folder(data_dir):
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    # Check if a folder is empty
    return len(os.listdir(data_dir)) == 0

if __name__ == '__main__':
    # Get the list of folders to generate
    folders = get_folder_modulized(off_only=True)

    for folder in folders:
        # Loop over only the random folders
        if 'Random' in folder:
            # Start generating the Xpred files, loop over the methods
            for dataset in dataset_list:
                print("currently in folder", folder," -  ", dataset)
                if 'on' in folder:
                    print("Current version the generate would only generate solutions for the baseline off off version, therefore skipping any folder with on", folder)
                    continue;
                elif not check_if_empty_folder(os.path.join(folder, dataset)):
                    print("This folder is not empty, therefore random generated solution function is skipping it", os.path.join(folder,dataset))
                    continue;
                # Skip MM for now ONLY
                #if 'meta_material' not in dataset:
                #    continue;
                data_num = data_num_base
                output_dir = os.path.join(folder, dataset)
                if dataset == 'meta_material':
                    generator = generate_meta_material
                    data_num = meta_data_num
                elif dataset == 'ballistics':
                    generator = generate_ballistics
                elif dataset == 'sine_wave':
                    generator = generate_sine_wave
                elif dataset == 'robotic_arm':
                    generator = generate_robotic_arm
                
                # Steal the Xtruth and Ytruth file from neighbouring folder
                shutil.copyfile(os.path.join(truth_folder, dataset, 'Xtruth.csv'), os.path.join(output_dir, 'Xtruth.csv')) 
                shutil.copyfile(os.path.join(truth_folder, dataset, 'Ytruth.csv'), os.path.join(output_dir, 'Ytruth.csv')) 
                
                
                print("currently generating in folder:", os.path.join(folder, dataset))
                # create a Xpred file for each of the trails
                for i in range(trail_num):
                    # Set up the filename
                    file_name = 'test_Xpred_point_' + dataset + '_inference' + str(i) + '.csv'
                    Xpred_full_name = os.path.join(output_dir, file_name)
                    # generate the data
                    data = generator(data_num)
                    # Save Xpred file
                    np.savetxt(Xpred_full_name, data)
                    # Get Ypred
                    if dataset != 'meta_material':  
                        Ypred = simulator(dataset, data)
                        np.savetxt(Xpred_full_name.replace('Xpred','Ypred'), Ypred)



