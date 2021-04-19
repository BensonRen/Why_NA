# This script outputs a table of the ICML modulized result

import pandas as pd 
import numpy as np 
import os 
#from utils.create_folder_modulized import get_folder_modulized

ds_list = ['ballistics','sine_wave','robotic_arm','meta_material']
method_list = ['Random','cINN','INN','VAE','MDN']
BP_FF_list = ['BP_off_FF_off','BP_off_FF_on','BP_on_FF_off','BP_on_FF_on']
index_name_list = ['Raw initializer','Filter only','Finetune only','Finetune + filter']
def get_min_mse_list(folder, ds, mse_file_name): 
    """
    Returns the mse_min_list of certain folder of certain dataset (ds)
    :param mse_file_name: Change to std or 25_percentile to get a latex table of that!
    """
    mse_list = pd.read_csv(os.path.join(folder, ds, mse_file_name),header=None).values
    #print(np.shape(mse_list))
    return mse_list


def get_table(big_dir, t, mse_file_name='mse_min_list.txt'):
    """
    Get the table of the mse_min value of T=t value for all ds and dataset from big_dir
    """
    pd.options.display.float_format = '{:.2e}'.format
    df_list = []
    for ds in ds_list:
        # Creat the table here
        table_value = np.zeros([len(BP_FF_list) , len(method_list)])
        for ind_m, method in enumerate(method_list):
            for ind_bpff, BP_FF in enumerate(BP_FF_list):
                # Get the mse_list
                data_folder = os.path.join(big_dir, method+'_'+BP_FF)
                mse_list = get_min_mse_list(data_folder, ds, mse_file_name)
                # assign the value to the table
                table_value[ind_bpff, ind_m] = mse_list[t-1]    # t-1 because the list starts from 0 however t starts from 1
        print("current dataset is: ", ds, "t = ", t)
        non_ball_method_list = ['','','','','']
        #print(df)
        #df_list.append(df)
        if 'ball' in ds:
            df = pd.DataFrame(table_value, index=index_name_list, columns=method_list)
        else:
            df = pd.DataFrame(table_value, index=index_name_list, columns=non_ball_method_list)
        if t == 1:
            print(df.to_latex())
        elif t==50:
            print(df.to_latex(index=None))
    return df_list


def get_worse_forward_model_table(big_dir_list, t, model_name_list, mse_file_name='mse_min_list.txt',normalize=False):
    """
    The function that gets the large table where all the worse model values are also printed on the large table
    :param: big_dir_list: The list of directories to plot
    :param: t: The time step t to take for getting the mse
    :param: model_name_list: The prefix to add at the first coloumn of the table
    :param: mse_file_name: The file name to extract the mse from, if it is "std_list.txt" then what we print in table is actually standard deviation
    :param: normalize: Normalize the rows by the baseline model
    """
    
    if normalize: # If normalize, they are all 1 to 100
        pd.options.display.float_format = '{:.1f}'.format
    else:
        pd.options.display.float_format = '{:.2e}'.format
    df_list = []
    num_dir = len(big_dir_list)
    for ds in ds_list:
        # Creat the table here
        table_shape = [len(BP_FF_list) * num_dir , len(method_list)]
        print('table shape = ', table_shape)
        table_value = np.zeros(table_shape)
        # Loop over method, dir and BPFF
        for ind_m, method in enumerate(method_list):
            for ind_bpff, BP_FF in enumerate(BP_FF_list):
                for ind_dir, big_dir in enumerate(big_dir_list):
                    # Get the mse_list
                    data_folder = os.path.join(big_dir, method+'_'+BP_FF)
                    mse_list = get_min_mse_list(data_folder, ds, mse_file_name)
                    # assign the value to the table
                    row_number = ind_bpff * num_dir + ind_dir # ind_dir * len(BP_FF_list) +
                    #print('dir index = {}, BPFF index = {}, row_number = {}'.format(ind_dir, ind_bpff, row_number))
                    table_value[row_number, ind_m] = mse_list[t-1]    # t-1 because the list starts from 0 however t starts from 1
        print("current dataset is: ", ds, "t = ", t)
        non_ball_method_list = ['','','','','']


        # Modify the index_list name
        big_index_name_list = []
        for index_name in index_name_list:
            for i in range(num_dir):
                big_index_name_list.append(index_name + model_name_list[i])

        #print(df)
        #df_list.append(df)
        if 'ball' in ds:
            df = pd.DataFrame(table_value, index=big_index_name_list, columns=method_list)
        else:
            df = pd.DataFrame(table_value, index=big_index_name_list, columns=non_ball_method_list)
        
        # Normalize the table using the baseline (1X) results for each row
        if normalize:
            print("Normalizing the rows now~~~")
            for i in range(len(BP_FF_list)):
                print("Normalizing the rows now~~~")
                df.iloc[i*num_dir:(i+1)*num_dir,:] /= df.iloc[i*num_dir,:]
        

        # Drop the duplicated rows of Raw initializer
        drop_index = big_index_name_list[1:num_dir]
        df = df.drop(index=drop_index)
        
        if normalize:
        #if t==50 or normalize:
            print(df.to_latex(index=None))
        #elif t == 1:
        else:
            print(df.to_latex())
        
    return df_list

def get_multiple_t_table(big_dir, t_list, mse_file_name):
    """
    Calling the get_table function with a list of t values
    """
    for t in t_list:
        print("T = ", t)
        df_list = get_table(big_dir, t)
        pd.options.display.float_format = '{:.2e}'.format
        df_list = []
        for ds in ds_list:
            # Creat the table here
            table_value = np.zeros([len(BP_FF_list), len(method_list)])
            for ind_m, method in enumerate(method_list):
                for ind_bpff, BP_FF in enumerate(BP_FF_list):
                    # Get the mse_list
                    data_folder = os.path.join(big_dir, method+'_'+BP_FF)
                    mse_list = get_min_mse_list(data_folder, ds, mse_file_name)
                    # assign the value to the table
                    table_value[ind_bpff, ind_m] = mse_list[t-1]    # t-1 because the list starts from 0 however t starts from 1
            print("current dataset is: ", ds, "t = ", t)
            non_ball_method_list = ['', '','','','']

            #print(df)
            #df_list.append(df)
            if 'ball' in ds:
                df = pd.DataFrame(table_value, index=index_name_list, columns=method_list)
            else:
                df = pd.DataFrame(table_value, index=index_name_list, columns=non_ball_method_list)
            if t == 1:
                print(df.to_latex())
            elif t==50:
                print(df.to_latex(index=None))
    return df_list

if __name__ == '__main__':
    # Part to get one big table of performance
    #big_dir = '/home/sr365/ICML_exp_worse_10_times'
    #get_table(big_dir, t=1)
    #get_multiple_t_table(big_dir, [1, 50], mse_file_name='mse_min_list.txt')

    # Part to compare different forward worse models
    big_dir_list = ['/home/sr365/ICML_exp_1st_full_March',
                    '/home/sr365/ICML_exp_worse_10_times',
                    '/home/sr365/ICML_exp_worse_50_times',
                    '/home/sr365/ICML_exp_worse_100_times']
    model_name_list = ['(1X)','(10X)','(50X)','(100X)']
    get_worse_forward_model_table(big_dir_list, 50 ,model_name_list, mse_file_name='mse_min_list.txt', normalize=False)
