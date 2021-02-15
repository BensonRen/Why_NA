import os
from create_folder_modulized import get_folder_modulized
import shutil

# This function moves the ICML_exp_mm meta-material dataset back into ICML_exp
# In the create_folder_modulized you need to have ICML_exp_mm to have
if __name__ == '__main__':
    folders = get_folder_modulized()
    for folder in folders:
        print(folder)
        if 'ICML_exp_mm' in folder:
            target_folder = folder.replace('_mm', '')
            print('moving from ', folder, 'to folder ', target_folder)
            #shutil.move(os.path.join(target_folder), os.path.join(folder, 'meta_material'))
            shutil.move(os.path.join(folder, 'meta_material'), os.path.join(target_folder))

        

