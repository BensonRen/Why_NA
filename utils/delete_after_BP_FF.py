import os
import numpy
from utils.create_folder_modulized import check_modulized_yet

# This is the program to delete all the duplicate Xtruth Ytruth files generated
input_dir = '/work/sr365/ICML_mm/'
delete_mse_file_mode = True                            # Deleting the mse file for the forward filtering


# For all the architectures
for folders in os.listdir(input_dir):
    #print(folders)
    # Check whether this is a folder and more importantly, this is a folder that being transformed by FF or BP!!!
    if os.path.isdir(os.path.join(input_dir,folders)) and 'on' in folders:
        # For all the datasets inside it
        for dataset in os.listdir(os.path.join(input_dir, folders)):
            #print(dataset)
            if os.path.isdir(os.path.join(input_dir, folders, dataset)):
                current_folder = os.path.join(input_dir, folders, dataset)
                print("current folder is:", current_folder)

                # Check whether this has been modulized, if not, print and skip this!!
                if not check_modulized_yet(current_folder):
                    print("This folder has not been modulized!! Run NA/modulized_eval.py for this first!!")
                    continue;
                for file in os.listdir(current_folder):
                    current_file = os.path.join(current_folder, file)
                    #if 'meta_material' not in dataset:
                    if '_Ypred_' in file and 'modulized' not in file:
                        os.remove(current_file)
                    if '_Xpred_' in file and 'modulized' not in file:
                        os.remove(current_file)
                    if delete_mse_file_mode and 'mse_' in file:
                        os.remove(current_file)
                        
                    

                    
