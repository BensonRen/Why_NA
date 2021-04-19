import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import MinMaxScaler, normalize



#########################################################################################################################
# Empirical proof of NA T=1 Performance
#Use # init as x-axis and MSE as y-axis and show that the NA T=1 performance converges to the forward model MSE
############################################################################################################################
dataset_list = ['ballistics','robotic_arm','sine_wave','meta_material']
#dataset_list = ['meta_material']
folder_mother_name = '/home/sr365/Why_NA/NA_loss_surface/NA_true_SGD_30k_init'
trail = 2
log_scale = False
for dataset in dataset_list:
    print("entering dataset : ", dataset)
    folder = os.path.join(folder_mother_name, dataset) 
    mse_mat = pd.read_csv(os.path.join(folder, 'mse_mat.csv'), header=None, sep=' ').values
    # The shape should be [#init, #test]
    print("shape of the MSE_MAT=", np.shape(mse_mat))
    
    num_init, num_test = np.shape(mse_mat)
    trail_mse_plot_mat = np.zeros([num_init, trail])
    for trail_ind in range(trail):
        # Use the fact that this MSE mat is internally ranked by the internal fake MSE,
        # we can shuffle the results and then take them as 
        mse_shuffle_mat = np.zeros_like(mse_mat)
        
        for i in range(num_test):
            random_index = np.random.permutation(num_init)
            # go through each t step
            for j in range(num_init):
                best_chosen = np.min(random_index[:j+1])
                mse_shuffle_mat[j, i] = mse_mat[best_chosen, i]
        mse_vs_num_init_list = np.mean(mse_shuffle_mat, axis=1)
        trail_mse_plot_mat[:, trail_ind] = mse_vs_num_init_list
    
    f = plt.figure()
    plt.plot(np.mean(trail_mse_plot_mat, axis=1))
    plt.savefig('/home/sr365/Why_NA/NA_loss_surface/data/{} MSE vs init.png'.format(dataset))
    print('T=1 performance is: ', np.mean(mse_mat[0,:]))
    #plt.yscale('log')
