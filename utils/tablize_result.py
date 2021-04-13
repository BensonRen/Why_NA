# This script outputs a table of the ICML modulized result

import pandas as pd 
import numpy as np 
import os 
#from utils.create_folder_modulized import get_folder_modulized

ds_list = ['ballistics','sine_wave','robotic_arm','meta_material']
method_list = ['Random','cINN','INN','VAE','MDN']
BP_FF_list = ['BP_off_FF_off','BP_off_FF_on','BP_on_FF_off','BP_on_FF_on']
index_name_list = ['Raw initializer','Filter only','Finetune only','Finetune + filter']
def get_min_mse_list(folder, ds):
    """
    Returns the mse_min_list of certain folder of certain dataset (ds)
    """
    mse_list = pd.read_csv(os.path.join(folder, ds, 'mse_min_list.txt'),header=None).values
    #print(np.shape(mse_list))
    return mse_list


def get_table(big_dir, t):
    """
    Get the table of the mse_min value of T=t value for all ds and dataset from big_dir
    """
    pd.options.display.float_format = '{:.2e}'.format
    df_list = []
    for ds in ds_list:
        # Creat the table here
        table_value = np.zeros([len(BP_FF_list), len(method_list)])
        for ind_m, method in enumerate(method_list):
            for ind_bpff, BP_FF in enumerate(BP_FF_list):
                # Get the mse_list
                data_folder = os.path.join(big_dir, method+'_'+BP_FF)
                mse_list = get_min_mse_list(data_folder, ds)
                # assign the value to the table
                table_value[ind_bpff, ind_m] = mse_list[t-1]    # t-1 because the list starts from 0 however t starts from 1
        print("current dataset is: ", ds, "t = ", t)
        df = pd.DataFrame(table_value, index=index_name_list, columns=method_list)
        #print(df)
        #df_list.append(df)
        if t == 1:
            print(df.to_latex())
        elif t==50:
            print(df.to_latex(index=None))
    return df_list


def get_multiple_t_table(big_dir, t_list):
    """
    Calling the get_table function with a list of t values
    """
    for t in t_list:
        print("T = ", t)
        df_list = get_table(big_dir, t)


if __name__ == '__main__':
    big_dir = '/home/sr365/ICML_exp'
    #get_table(big_dir, t=1)
    get_multiple_t_table(big_dir, [1, 50])
