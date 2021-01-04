### This is the program for creating the model folders that stores the results.
### The experiment is to work on the cross space of all combination of initializer, optimization and forward filtering

import os
import numpy

# Where to create the folders, assume here
create_directory_folder = '/work/sr365/ICML_mm/'
#create_directory_folder = '/work/sr365/ICML_exp_1231/'
# If testing_mode on, only one folder would be in the list: cINN_on_on/robotic
testing_mode = False

# Setting up the list of datasets and method to work on
#dataset_list = ['meta_material']
dataset_list = ['meta_material','robotic_arm','sine_wave','ballistics']
initializer_list = ['Random','cINN','INN','VAE','MDN']
#optimizer_list = ['BP_off']
#filter_list = ['FF_off']
optimizer_list = ['BP_on','BP_off']
filter_list = ['FF_on','FF_off']

def get_folder_modulized(gpu=None):
    """
    Get a list of all modulized folder in the ICML exp folder that stores the major results
    :param gpu: GPU number specified. GPU03 is 2080 and hence has more jobs than other GPUs. The split of GPU jobs workload can be seen at the Experiment_spreadsheet.
    :return folder_list: A list of folders that has all the modulized folders
    """
    folder_list=[]
    if testing_mode:
        folder_list.append(os.path.join(create_directory_folder, 'VAE_BP_on_FF_off'))
        return folder_list
    for init in initializer_list:
        for opti in optimizer_list:
            for fil in filter_list:
                # Create the method_crossed folder
                path = os.path.join(create_directory_folder, init + '_' + opti + '_' + fil)
                folder_list.append(path)
    sub_list = []
    if gpu is None:
        return folder_list 
    elif gpu == 1: # Titan X (Pascal), speed = 1.4
        for folder in folder_list:
            if 'Random' in folder and 'BP_on' in folder:
                sub_list.append(folder)
            if 'MDN' in folder and 'BP_on' in folder:
                sub_list.append(folder)
    elif gpu == 2: # 1080 TI, speed = 1.55
        for folder in folder_list:
            if 'cINN' in folder or 'BP_off' in folder:
                sub_list.append(folder)
    elif gpu == 3: # Titan X, speed = 1 but very very useful for all the meta-material
        for folder in folder_list:
            sub_list.append(folder)
    elif gpu == 4: # 1080 TI, speed = 1.55
        for folder in folder_list:
            if 'INN' in folder and  'BP_on' in folder and 'cINN' not in folder:
                sub_list.append(folder)
            if 'VAE' in folder and  'BP_on' in folder:
                sub_list.append(folder)
    return sub_list

        
def check_modulized_yet(data_dir):
    """
    This function checks whether this folder has been modulized or not (Has it run NA/modulized_eval for BP and FF yet. By going through all the files in the folder and check if there are name with modulized in any of the file name, if there is, then return True, if none of the files in the folder has modulized, return False
    """
    for file in os.listdir(data_dir):
        if 'modulized' in file:
            return True
    return False
        


if __name__ == '__main__':
    for init in initializer_list:
        for opti in optimizer_list:
            for fil in filter_list:
                # Create the method_crossed folder
                path = os.path.join(create_directory_folder, init + '_' + opti + '_' + fil)
                if not os.path.exists(path):
                    os.makedirs(path)
                # create the dataset folders
                for data in dataset_list:
                    data_set_path = os.path.join(path, data)
                    if not os.path.exists(data_set_path):
                        os.makedirs(data_set_path)
