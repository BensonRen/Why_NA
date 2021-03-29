###
# The function to swipe through the Forward Filtering (FF) Strength
# The FF strength is controlled by a parameter called FF_ratio in plotsAnalysis.MeanAvgnMinMSEvsTry where
# It plots the MSE_Min and MSE_AVG plots. 
###

import utils.plotsAnalysis as PA
import os
from math import ceil,floor

# Set up some hyper-params
swipe_folder = '/home/sr365/FF_ratio_swipe/'
FF_ratio_list = [0.05, 0.1, 0.2, 0.25]
data_dir = '/home/sr365/ICML_exp_mm/' 
algo_list = ['cINN','INN','VAE','MDN','Random']
#datasets = ['robotic_arm','ballistics']
#datasets = ['robotic_arm','sine_wave','ballistics','meta_material']
datasets = ['sine_wave','meta_material']


def move_plots_to_dir(FF_ratio):
    """
    Function that moves plots to the FF_ratio_folder and change names accordingly
    """
    save_folder = os.path.join(swipe_folder, str(FF_ratio))
    # Create the folder if does not exist
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    
    # Loop over the algos
    for algo in algo_list:
        algo_dir = os.path.join(data_dir, algo)
        # Loop files within each algo directory and find the plots
        for file in os.listdir(algo_dir):
            if file.endswith('.png'):
                os.rename(os.path.join(algo_dir, file), 
                    os.path.join(save_folder, 'FF_ratio_' + str(FF_ratio) + algo + file))
    

def get_resolution(num_points):
    """
    Hard coding the resolution using this function
    """
    if num_points < 100:
        return ceil(num_points/5)
    elif num_points < 500:
        return ceil(num_points/10)
    else:
        return ceil(num_points/20)

if __name__ == '__main__':
    
    ### Step 1: Set up the folder
    # Create folder if not exist
    if not os.path.exists(swipe_folder):
        os.mkdir(swipe_folder)
    
    
    ### Step 2 Loop through the FF_ratio list, plot the plot and move plot to result folder
    for FF_ratio in FF_ratio_list:
        
        # Step 2.0 Delete all the mse* files
        for subdir, dirs, files in os.walk(data_dir):
            for file in files:
                if 'mse' in file:
                    os.remove(os.path.join(subdir, file))

        # Step 2.1 Loop through FF_ratio list, generate plots under each folder
        for algo in algo_list:
            PA.MeanAvgnMinMSEvsTry_all(os.path.join(data_dir, algo), FF_ratio=FF_ratio)
            for dataset in datasets:
                plot_points = floor(2048*FF_ratio)
                PA.DrawAggregateMeanAvgnMSEPlot(os.path.join(data_dir, algo), dataset, 
                                        plot_points=plot_points, resolution=get_resolution(plot_points))
        
        # Step 2.2 Change directory of those generated plots
        move_plots_to_dir(FF_ratio)
