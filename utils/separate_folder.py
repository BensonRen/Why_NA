import os
import shutil
# The program for NA_compare

dataset_list = ['ballistics','robotics']

for folder in os.listdir('.'):
    print("current folder: ", folder)
    # Skip if this is not a folder
    if not os.path.isdir(folder):
        continue;
    for dataset in dataset_list:
        # Skip if this has no dataset name inside
        if dataset not in folder:
            continue;
        # If there is, take the first part and make a folder
        print("moving")
        first_part = folder.split(dataset)[0]
        shutil.move(folder, os.path.join(first_part+'_NA', dataset))
