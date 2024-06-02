import pandas as pd
import os

def concatenate(folder_path):
    # read all the csv files in the folder and concatenate them into a single dataframe by column
    files = os.listdir(folder_path)
    # skip the folders in the directory
    files = [file for file in files if '.csv' in file]
    # get the name of the folder
    folder_name = folder_path.split('/')[-2]
    data = pd.DataFrame()
    if folder_name == 'walk_data':
        temp_data_list = []
        # loop through the folders in the walk_data folder
        for folder in os.listdir(folder_path):
            # loop through the files in the subfolder
            subfolder_path = os.path.join(folder_path, folder)
            subfolder_files = os.listdir(subfolder_path)
            subfolder_files = [file for file in subfolder_files if '.csv' in file]
            # get the name of the subfolder
            subfolder_name = folder
            subfolder_data = pd.DataFrame()
            for file in subfolder_files:
                file_path = os.path.join(subfolder_path, file)
                subfolder_data = pd.concat([subfolder_data, pd.read_csv(file_path)], axis=1)
            temp_data_list.append(subfolder_data)
        
        # concatenate all subfolder dataframes
        data = pd.concat(temp_data_list, axis=0)
        
        # save the concatenated dataframe to a csv file
        data.to_csv(folder_name + '.csv', index=False)
        
    else:
        for file in files:
            data = pd.concat([data, pd.read_csv(os.path.join(folder_path, file))], axis=1)
        # save the concatenated dataframe to a csv file
        data.to_csv(folder_name + '.csv', index=False)

concatenate('data/relaxed_data/')
concatenate('data/run_data/')
concatenate('data/stairs_data/')
concatenate('data/walk_data/')
