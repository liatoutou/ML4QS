import pandas as pd
import os

def concatenate(folder_path):
    #read all the csv files in the folder and concatenate them into a single dataframe by column
    files = os.listdir(folder_path)
    #skip the folders in the directory
    files = [file for file in files if '.csv' in file]
    #get the name of the folder
    folder_name = folder_path.split('/')[-2]
    data = pd.DataFrame()
    if folder_name == 'walk_data':
        #loop through the folders in the walk_data folder
        for folder in os.listdir(folder_path):
            #loop through the files in the subfolder
            files = os.listdir(folder_path + folder)
            files = [file for file in files if '.csv' in file]
            print(files)
            #get the name of the subfolder
            subfolder_name = folder
            subfolder_data = pd.DataFrame()
            for file in files:
                subfolder_data = pd.concat([subfolder_data, pd.read_csv(folder_path + folder + '/' + file)], axis=1)
            #save the concatenated dataframe to a csv file
            subfolder_data.to_csv('./data/walk_data/'+ subfolder_name + '.csv', index=False)
        #concatenate the csv files created from the subfolders
        files = os.listdir('./data/walk_data/')
        files = [file for file in files if '.csv' in file]
        data = pd.DataFrame()
        for file in files:
            data = pd.concat([data, pd.read_csv('./data/walk_data/' + file)], axis=0)
        #save the concatenated dataframe to a csv file
        data.to_csv('./data/' +folder_name+'.csv', index=False)      
    else:
        for file in files:
            data = pd.concat([data, pd.read_csv(folder_path + file)], axis=1)
        #save the concatenated dataframe to a csv file
    data.to_csv('./data/' +folder_name + '.csv', index=False)

def map_elapsed_to_system_time(elapsed_time, time_df):
    for i in range(len(time_df) - 1):
        if time_df.loc[i, 'experiment time'] <= elapsed_time < time_df.loc[i + 1, 'experiment time']:
            # Linear interpolation to find the system time
            start_time = time_df.loc[i, 'system time']
            end_time = time_df.loc[i + 1, 'system time']
            start_exp_time = time_df.loc[i, 'experiment time']
            end_exp_time = time_df.loc[i + 1, 'experiment time']
            system_time = start_time + (elapsed_time - start_exp_time) * (end_time - start_time) / (end_exp_time - start_exp_time)
            return system_time
    # If the elapsed time is beyond the last PAUSE event, use the last recorded system time
    return time_df.iloc[-1]['system time']

def add_actual_time(time_dataframe, experiment_dataframe,dataframe_name):
    ''' Function that adds the actual system time to the dataframe'''
    # Apply the function to each elapsed time in the dataframe
    experiment_dataframe['Actual System Time'] = experiment_dataframe['Time (s)'].apply(lambda x: map_elapsed_to_system_time(x, time_dataframe))
    # Convert the system time to a readable timestamp format
    experiment_dataframe['Actual System Time Text'] = pd.to_datetime(experiment_dataframe['Actual System Time'], unit='s', origin='unix')
    #localize the time to the timezone of the experiment UTC+2
    experiment_dataframe['Actual System Time Text'] = experiment_dataframe['Actual System Time Text'].dt.tz_localize('UTC').dt.tz_convert('Europe/Amsterdam')
    #save the dataframe to a csv file if the file exists replace it
    experiment_dataframe.to_csv('data/' + dataframe_name + '.csv', index=False)




def main():    
    concatenate('data/relaxed_data/')
    concatenate('data/run_data/')
    concatenate('data/stairs_data/')
    concatenate('data/walk_data/')

    walk1_df = pd.read_csv('data/walk_data/walk1.csv')
    time_df1 = pd.read_csv('data/walk_data/walk1/meta/time.csv')

    walk2_df = pd.read_csv('data/walk_data/walk2.csv')
    time_df2 = pd.read_csv('data/walk_data/walk2/meta/time.csv')

    run_df = pd.read_csv('data/run_data.csv')
    time_df3 = pd.read_csv('data/run_data/meta/time.csv')

    stairs_df = pd.read_csv('data/stairs_data.csv')
    time_df4 = pd.read_csv('data/stairs_data/meta/time.csv')

    relaxed_df = pd.read_csv('data/relaxed_data.csv')
    time_df5 = pd.read_csv('data/relaxed_data/meta/time.csv')

    add_actual_time(time_df1, walk1_df, 'walk1')
    add_actual_time(time_df2, walk2_df, 'walk2')
    add_actual_time(time_df3, run_df, 'run')
    add_actual_time(time_df4, stairs_df,  'stairs')
    add_actual_time(time_df5, relaxed_df, 'relaxed')


if __name__ == '__main__':
    main()