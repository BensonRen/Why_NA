### This is the program for creating the model folders that stores the results.
### The experiment is to work on the cross space of all combination of initializer, optimization and forward filtering

import os
import numpy
import shutil
# Where to create the folders, assume here
# create_directory_folder = '/work/sr365/ICML_mm/'
# create_directory_folder = '/work/sr365/ICML_exp/'
# create_directory_folder = '/home/sr365/ICML_exp_cINN_ball/'    # For quad
#create_directory_folder = '/home/sr365/ICML_exp_ball_0.01/'    # For quad
create_directory_folder = '/home/sr365/ICML_exp_timing/'
#create_directory_folder = '/home/sr365/ICML_exp_worse_10_times_NA/'    # For quad
#create_directory_folder = '/home/sr365/ICML_exp_worse_50_times_NA/'    # For quad
#create_directory_folder = '/home/sr365/ICML_exp_worse_100_times_NA/'    # For quad
#create_directory_folder = '/home/sr365/ICML_exp_0402/'    # For quad
#create_directory_folder = '/home/sr365/ICML_exp_robo/'    # For quad
#create_directory_folder = '/data/users/ben/ICML_exp_mm/'    # For Groot 
# If testing_mode on, only one folder would be in the list: cINN_on_on/robotic
testing_mode = False

# Setting up the list of datasets and method to work on
dataset_list = ['meta_material','robotic_arm','sine_wave','ballistics']
#dataset_list = ['meta_material']
#initializer_list = ['Random','cINN']
#initializer_list = ['Random','cINN','INN','VAE']
#initializer_list = ['Random','cINN','INN','VAE','MDN']
initializer_list = ['MDN']
optimizer_list_base = ['BP_off']
filter_list_base = ['FF_off']
optimizer_list_full = ['BP_on','BP_off']
filter_list_full = ['FF_on','FF_off']

def get_folder_modulized(gpu=None, off_only=False):
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
        for opti in optimizer_list_full:
            for fil in filter_list_full:
                # Create the method_crossed folder
                path = os.path.join(create_directory_folder, init + '_' + opti + '_' + fil)
                if off_only and 'on' in path:
                    continue
                folder_list.append(path)
    sub_list = []
    
    """
    # This is the work allocation for Meta_material only since it is consuming a lot of time
    if gpu is None:
        return folder_list
    elif gpu==0:
        for folder in folder_list:
            if 'Random' in folder or 'BP_off' in folder:
                sub_list.append(folder)
    elif gpu==1:
        for folder in folder_list:
            if 'INN' in folder and 'BP_on' in folder:
                sub_list.append(folder)
    elif gpu==2:
        for folder in folder_list:
            if 'MDN' in folder :
                sub_list.append(folder)
    elif gpu==3:
        for folder in folder_list:
            if 'VAE' in folder :
                sub_list.append(folder)
    return sub_list

    # This is the original work allocation on Groot
    if gpu is None:
        return folder_list 
    elif gpu == 0: # Titan X (Pascal), speed = 1.4
        for folder in folder_list:
            if 'Random' in folder and 'BP_on' in folder:
                sub_list.append(folder)
            if 'MDN' in folder and 'BP_on' in folder:
                sub_list.append(folder)
    elif gpu == 1: # 1080 TI, speed = 1.55
        for folder in folder_list:
            if 'cINN' in folder or 'BP_off' in folder:
                sub_list.append(folder)
    elif gpu == 2: # Titan X, speed = 1 but very very useful for all the meta-material
        for folder in folder_list:
            sub_list.append(folder)
    elif gpu == 3: # 1080 TI, speed = 1.55
        for folder in folder_list:
            if 'INN' in folder and  'BP_on' in folder and 'cINN' not in folder:
                sub_list.append(folder)
            if 'VAE' in folder and  'BP_on' in folder:
                sub_list.append(folder)
    return sub_list
    """

    # This is the allocation for quad 3090 non_mm parts 
    if gpu is None:
        return folder_list 
    elif gpu == 0: 
        for folder in folder_list:
            if 'Random' in folder and 'BP_on' in folder:
                sub_list.append(folder)
    elif gpu == 1:
        for folder in folder_list:
            if 'cINN' in folder or 'BP_off' in folder:
                sub_list.append(folder)
    elif gpu == 2: 
        for folder in folder_list:
            if 'MDN' in folder and 'BP_on' in folder:
                sub_list.append(folder)
            #if 'VAE' in folder and  'BP_on' in folder:
            # For timing purpose only
            if 'VAE' in folder:# and  'BP_on' in folder:
                sub_list.append(folder)
    elif gpu == 3: 
        for folder in folder_list:
            if 'INN' in folder and  'BP_on' in folder and 'cINN' not in folder:
                sub_list.append(folder)
    elif gpu == 9:
        # special test case for easy testing
        for folder in folder_list:
            if 'Random' in folder and 'BP_on' in folder:
                sub_list.append(folder)
    return sub_list
    
    """
    # This is the allocation for quad 3090 mm only
    if gpu is None:
        return folder_list 
    elif gpu == 0: 
        for folder in folder_list:
            if 'Random' in folder and 'BP_on' in folder:
                sub_list.append(folder)
            if 'MDN' in folder and 'BP_on' in folder:
                sub_list.append(folder)
    elif gpu == 1:
        for folder in folder_list:
            if 'cINN' in folder and 'BP_on' in folder:
                sub_list.append(folder)
    elif gpu == 2: 
        for folder in folder_list:
            if 'VAE' in folder and 'BP_on' in folder or 'BP_off' in folder:
                sub_list.append(folder)
    elif gpu == 3: 
        for folder in folder_list:
            if 'INN' in folder and  'BP_on' in folder and 'cINN' not in folder:
                sub_list.append(folder)
    elif gpu == 9:
        # special test case for easy testing
        return folder_list 
    return sub_list
        
    # This is the allocation for quad 3090 MDN part 
    if gpu is None:
        return folder_list 
    elif gpu == 0: 
        for folder in folder_list:
            if 'MDN' in folder and 'BP_on' in folder:
                sub_list.append(folder)
    elif gpu == 1:
        for folder in folder_list:
            if 'MDN' in folder and 'BP_on' in folder:
                sub_list.append(folder)
    elif gpu == 2: 
        for folder in folder_list:
            if 'MDN' in folder and 'BP_on' in folder:
                sub_list.append(folder)
    elif gpu == 3: 
        for folder in folder_list:
            if 'MDN' in folder and 'BP_on' in folder:
                sub_list.append(folder)
    elif gpu == 9:
        # special test case for easy testing
        for folder in folder_list:
            if 'Random' in folder and 'BP_on' in folder:
                sub_list.append(folder)
    return sub_list
    """
    

def check_modulized_yet(data_dir):
    """
    This function checks whether this folder has been modulized or not (Has it run NA/modulized_eval for BP and FF yet. By going through all the files in the folder and check if there are name with modulized in any of the file name, if there is, then return True, if none of the files in the folder has modulized, return False
    """
    for file in os.listdir(data_dir):
        if 'modulized' in file:
            return True
    return False
        

def duplicate_off_off_base_folders():
    """
    The function that calls cp -r in bash script to copy the folders so that there only need to be one set of evaluation generated.
    """
    for init in initializer_list:
        for opti in optimizer_list_full:
            for fil in filter_list_full:
                dest_path = os.path.join(create_directory_folder, init + '_' + opti + '_' + fil)
                src_path = os.path.join(create_directory_folder, init + '_BP_off_FF_off') 
                # If this is already copied, skip this folder
                if os.path.isdir(dest_path):
                    print("skipping copying from:", src_path, " to dir:", dest_path)
                    continue
                try:
                    print("Now, copying from:", src_path, " to dir:", dest_path)
                    shutil.copytree(src_path, dest_path)
                except shutil.Error as e:
                    print('Directory not copied. Error: %s' % e, dest_path)
                except OSError as e:
                    print('Directory not copied. Error: %s' % e, dest_path)
    

def move_across_ICML_exp(dest_dir, src_dir):
    """
    The function to move the experiments of ICML around
    :param dest_dir: The destination of the moving folders
    :param scr_dir: The source of moving folders
    """
    # Only move the listed folders
    dataset_sublist = ["ballistics", "robotic_arm"]
    # Get the folder list
    folder_list = get_folder_modulized()
    for dataset in dataset_sublist:
        for folder in folder_list:
            print("folder =", folder)
            print("removing front part")
            folder = folder.split(create_directory_folder)[-1]
            print("folder =", folder)
            # Set up the source and destination first
            src_path = os.path.join(src_dir, folder, dataset)
            dest_path = os.path.join(dest_dir, folder, dataset)
            print("src_path = ", src_path)
            print("dest_path = ", dest_path)
            # Warn user if the destination exist and abort
            if os.path.isdir(dest_path):
                print("In utils move across ICML exp function, your destination exist! Therefore we are aborting your attempt to move the folder!")
                exit()
            # Clear to move folder
            try:
                print("Now, copying from:", src_path, " to dir:", dest_path)
                shutil.copytree(src_path, dest_path)
            except shutil.Error as e:
                print('Directory not copied. Error: %s' % e, dest_path)
            except OSError as e:
                print('Directory not copied. Error: %s' % e, dest_path)
    


def main():
    # Only activate this line if you finished creating base inference
    if os.path.isdir(os.path.join(create_directory_folder, 'MDN_BP_off_FF_off')):
        duplicate_off_off_base_folders()
        return
    
    # Main function of create folder
    for init in initializer_list:
        for opti in optimizer_list_base:
            for fil in filter_list_base:
                # Create the method_crossed folder
                path = os.path.join(create_directory_folder, init + '_' + opti + '_' + fil)
                if not os.path.exists(path):
                    os.makedirs(path)
                # create the dataset folders
                for data in dataset_list:
                    data_set_path = os.path.join(path, data)
                    if not os.path.exists(data_set_path):
                        os.makedirs(data_set_path)


if __name__ == '__main__':
    #folders = get_folder_modulized(gpu=2, off_only=False)
    #for fod in folders:
    #    print(fod)

    main()
   

   # move_across_ICML_exp(dest_dir='/data/users/ben/ICML_mm/',src_dir='/data/users/ben/ICML_exp')



