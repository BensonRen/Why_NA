# This function aims to get the pairwise distance of the geometry (controlable parameter) of the inverse solutions at T for each dataset and plot them
import os
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from utils.create_folder_modulized import get_folder_modulized
from sklearn.metrics import pairwise_distances
from utils.helper_functions import get_index_from_dataset_name

ds_list = ['ball','sine','robo','meta']

# This color dict is extracted from the plotsAnalysis.py file next door
color_dict = {"VAE": "blueviolet","cINN":"crimson", 
                        "INN":"cornflowerblue", "Random": "limegreen","MDN": "darkorange"}
def get_Xpred_mat_from_folder(data_dir):
    """
    This function gets the Xprediction map from the giant folderthat contains all the multi_eval files.
    Due to the data structure difference of NA storing, all subfolders with ('NA' or 'on' in name) would be specially handled
    :param data_dir: The directory where the data is stored
    """
    Xt = pd.read_csv(os.path.join(data_dir, 'Xtruth.csv'), header=None, delimiter=' ').values
    l, w = np.shape(Xt)     # l is the number of target spectra, w is the dimension of x
    num_trails = 50
    Xpred_mat = np.zeros([l, num_trails, w])
    if 'NA' in data_dir or 'on' in data_dir: 
        check_full = np.zeros(l)                                     # Safety check for completeness
        for files in os.listdir(data_dir):
            if '_Xpred_' in files:
                Xp = pd.read_csv(os.path.join(data_dir, files), header=None, delimiter=' ').values
                #print("shape of Xpred file is", np.shape(Xp))
                # Truncating to the top num_trails inferences
                if len(Xp) != num_trails:
                    Xp = Xp[:num_trails,:]
                number = int(files.split('inference')[-1][:-4])
                Xpred_mat[number, :, :] = Xp
                check_full[number] = 1
        assert np.sum(check_full) == l, 'Your list is not complete'
    else:
        index = 0
        for files in os.listdir(data_dir):
            if 'Xpred' in files:
                Xp = pd.read_csv(os.path.join(data_dir, files), header=None, delimiter=' ').values
                Xpred_mat[:, index, :] = Xp
                index += 1
                if index >= num_trails:
                    break
    return Xpred_mat


def from_Xpred_mat_calculate_pairwise_distance(Xpred_mat, n_jobs=20):
    """
    Like its name, this function calculates the average pairwise distance from the huge Xpred matrix
    
    ###This funciton calls the sklearn function: 
    https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html
    Look into details from this website of reference if needed.

    :param: Xpred_mat: The huge Xpred matrix that is of shape [num_targets, num_trails, dim_x] 
    """
    # Get the shape of Xpred mat 
    print('shape of Xpred_mat is: {}'.format(np.shape(Xpred_mat)))
    num_target, num_trails, dim_x = np.shape(Xpred_mat)
    # place holder for list of average pairwise distance
    avg_pair_wise_dis_list = np.zeros([num_target, 1])
    # Loop over the target dimension
    for i in range(num_target):
        # calling the function in sklearn and returning a function of n_sample x n_sample
        pair_wise_distance = pairwise_distances(X=Xpred_mat[i, :, :], Y=Xpred_mat[i, :, :],
                                                n_jobs=n_jobs)
        # Get the average of these
        avg_distrance = np.mean(pair_wise_distance)
        avg_pair_wise_dis_list[i] = avg_distrance
    
    return np.mean(avg_pair_wise_dis_list)


def get_all_avg_pwdis_in_table(big_dir):
    """
    This function get the table of avg_pw_distance from a big directory like ICML_exp folder structure 
    :param big_dir: The starting directory, usually containing all the subfolders where multi_eval named by dataset name
    """
    # init the dataframe
    df = pd.DataFrame()
    df_row_name_list = []

    for folder in os.listdir(big_dir):
        cur_folder = os.path.join(big_dir, folder)
        
        # Work only on folders (something like cINN_BP_off_FF_off etc.)
        if not os.path.isdir(cur_folder):
            continue

        # record the folder name for row name
        df_row_name_list.append(folder)
        
        # place holder for avg pairwise distance 
        avg_pwdis_dataset_row = np.zeros([1, 4])

        for dataset in os.listdir(cur_folder):
            dataset_subfolder = os.path.join(cur_folder, dataset)
            # only get the dataset folders
            if not os.path.isdir(dataset_subfolder):
                continue
            # Check thats a dataset folder by getting its index
            ds_ind = get_index_from_dataset_name(dataset)
            
            # Get the avg pw distance
            Xpred_mat = get_Xpred_mat_from_folder(dataset_subfolder)
            avg_dist = from_Xpred_mat_calculate_pairwise_distance(Xpred_mat)
            
            # record this distance
            avg_pwdis_dataset_row[0, ds_ind] = avg_dist
        
        # append this avg_pwdis to the dataframe
        df = df.append(pd.DataFrame(avg_pwdis_dataset_row))
    
    df.columns = ds_list
    df.index= df_row_name_list

    return df


def plot_pw_dist(pw_dist_mat_file, save_dir):
    """
    The pairwise distance plotting function
    :param pw_dist_mat_file: The csv file of the average pairwise distance 
        with row names being the methods and coloumn names being the dataset
    """
    # Read the csv matrix
    df = pd.read_csv(pw_dist_mat_file, index_col=0)
    # Set some list
    ds_list = ['ball','sine','robo','meta']
    method_list = ['Random','cINN','INN','VAE','MDN']
    BP_FF_list = ['BP_off_FF_off','BP_off_FF_on','BP_on_FF_off','BP_on_FF_on']

    # Loop over the dataset
    for ds in ds_list:
        print('dataset=', ds)
        BP_off_FF_off, BP_off_FF_on, BP_on_FF_off, BP_on_FF_on = [], [], [], []
        # baseline normalizer is random init
        base = df[ds]['Random_BP_off_FF_off']
        for method in method_list:
            for BP_FF in BP_FF_list:
                row_index = method + '_' + BP_FF
                eval(BP_FF).append(df[ds][row_index]/base)
        
        print(BP_off_FF_off)
        # Drawing
        f = plt.figure(figsize=[6,3])
        ax = plt.gca()
        X = np.arange(len(method_list))
        offset = 0
        for BP_FF in BP_FF_list:
            ax.bar(X + offset, eval(BP_FF), width=0.2, label=BP_FF)
            offset += 0.2
        #plt.legend()
        plt.xticks(0.3+X, method_list)
        colors = [color_dict[method] for method in method_list]
        # Set color 
        for xtick, color in zip(ax.get_xticklabels(), colors):
            print(xtick)
            xtick.set_color(color)
        #plt.ylabel('avg pair-wise distance')
        #plt.title('{} avg pair-wise distance for initializer'.format(ds))
        plt.savefig(os.path.join(save_dir, '{}_avg_pw_distance.png'.format(ds)))


if __name__ == '__main__':
    #Xpred_mat = get_Xpred_mat_from_folder('/home/sr365/ICML_exp/cINN_BP_off_FF_off/robotic_arm')
    #avg_dist = from_Xpred_mat_calculate_pairwise_distance(Xpred_mat)
    #print(avg_dist)
    # print(np.shape(Xpred_mat))

    big_dir = '/home/sr365/ICML_exp'
    #df = get_all_avg_pwdis_in_table(big_dir)
    #print(df)
    csv_save_name = os.path.join(big_dir, 'avg_pw_dist_mat.csv')
    #df.to_csv(csv_save_name)

    # Plotting this csv file down
    plot_pw_dist(csv_save_name, big_dir)
