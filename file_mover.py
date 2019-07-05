import pandas as pd
import os, shutil

# Path of folder containing video files
video_folder_path = '/Volumes/PS4 MyPassp/PS4/SHARE/Video Clips/Madden NFL 19'

# Creating dataframe of hand labelled data
hand_label_df = pd.read_csv('csv/type_dataset.csv', index_col=0)
hand_label_df.columns = ['filename', 'play_type', 'side']
hand_label_df['by_hand'] = 1

# Dataframe of videos with predicted labels
pred_df = pd.read_csv('csv/final_predictions.csv', index_col=0)
pred_df['by_hand'] = 0

# Combining hand-labelled and predicted dataframes
df = pd.concat([hand_label_df, pred_df], axis=0, sort=True).reset_index(drop=True)
df['video_file'] = df['filename'].str.split('-frame').apply(lambda x: x[0]).str.split('/').apply(lambda x: x[-1] + '.mp4')
df.to_csv('csv/final_labelled_data.csv')

# Get list of all available videos in video folder
video_files = os.listdir(video_folder_path)

# Iterate through and make sure subfolders are created, if not create them
for suffix in ['pass', 'run', 'fake']:
    if not os.path.isdir(os.path.join(video_folder_path, suffix)):
        os.mkdir(os.path.join(video_folder_path, suffix))

# Using shutil to move files to specified subfolder
for entry in df.iterrows():
    play = entry[1][2]
    filename = entry[1][4]
    try:
        shutil.move(os.path.join(video_folder_path, filename), os.path.join(os.path.join(video_folder_path, play)))
    except:
        print('-')