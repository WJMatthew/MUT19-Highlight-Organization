import cv2
import os
import pandas as pd
import numpy as np

RUN_INDEX = 5

video_folder_path = '/Volumes/PS4 MyPassp/PS4/SHARE/Video Clips/Madden NFL 19'
frame_path = 'saved_frames'
user_path = 'users'
play_path = 'saved_plays'

for path in [frame_path, user_path, play_path]:
    if not os.path.isdir(path):
        os.mkdir(path)


def extract_final_frame(video_file, path=frame_path):
    video_path = os.path.join(video_folder_path, video_file)

    # Opens the Video file
    cap = cv2.VideoCapture(video_path)
    i = 0
    frame_holder = None

    while (cap.isOpened()):
        ret, frame = cap.read()

        if ret:
            frame_holder = frame
        else:
            break
        i += 1

    save_prefix = video_file.rstrip('.mp4')
    save_filename = f'{path}/{save_prefix}-frame{i}.jpg'
    cv2.imwrite(save_filename, frame_holder)
    cap.release()
    cv2.destroyAllWindows()

    #
    suffix = video_file.rstrip('.mp4').split('_')[-1]
    entry = {'video_file': video_file,
             'cap_file': save_filename,
             'date': suffix
             }
    return entry


def get_todo_filenames():
    # TODO: change this..
    clip_file = f'may19_caps_{RUN_INDEX-1}.csv'
    if os.path.isfile(clip_file):
        all_clips = pd.read_csv(clip_file)
        all_clips = all_clips[pd.isnull(all_clips['cap_file'])]
        todo_files = all_clips['video_file'].values
    else:
        print('ERROR')

    return todo_files


def add_dates():
    df['date'] = df['video_file'].str.split('Madden NFL 19_').apply(lambda x: x[1]).str[:8]
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d', errors='coerce')
    df.sort_values('date', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def make_train_data(limit=None):
    # Get File Names
    filenames = get_todo_filenames()

    df = pd.DataFrame({'video_file': filenames})
    df = add_dates(df)

    #
    filenames = df['video_file'].values

    # File limit
    if limit:
        stop_idx = min(400, len(filenames))
    else:
        stop_idx = len(filenames)
    print(f'{len(filenames)} video files available... extracting {stop_idx}.')

    # Extracting Screen Caps
    data_entries = [extract_final_frame(file) for file in filenames[:stop_idx]]
    df = pd.DataFrame(data_entries)

    newdf = pd.concat([df2, df], axis=1).iloc[:, :-2]
    newdf.to_csv(os.path.join('csv', 'train_data.csv'))


class ImageCropper:

    def __init__(self, root_dir='image_data', kind='test'):
        self.x = 0
        self.y = 25
        self.h = 140 - self.y
        self.w = 1280
        self.play_width = 347
        self.play_height = 206
        self.play_loc_r = (423, 821)
        self.play_loc_l = (423, 94)
        self.root_dir = root_dir
        self.kind_path = os.path.join(root_dir, kind)
        self.user_path = os.path.join(root_dir, kind, 'users')
        self.play_path = os.path.join(root_dir, kind, 'saved_plays')
        self.check_for_folders()

    def check_for_folders(self):
        for path in [self.root_dir, self.kind_path, self.user_path, self.play_path]:
            if not os.path.isdir(path):
                os.mkdir(path)

    def crop_image_top(self, img_name):
        # Open Image
        image = cv2.imread(img_name)
        # Crop Image
        crop_img = image[self.y:self.y + self.h, :]

        left = crop_img[:, 72:262]
        right = crop_img[:, 1015:1208]

        # Combine
        concat_img = np.concatenate([left, right], axis=1)
        fn = self.save_file(concat_img, img_name.split('/')[-1], self.user_path, 'top')
        return fn

    def crop_image_play(self, img_name):
        # Open Image
        image = cv2.imread(img_name)
        # Crop Image
        left = image[self.play_loc_l[0]: self.play_loc_l[0] + self.play_height,
               self.play_loc_l[1]: self.play_loc_l[1] + self.play_width]
        right = image[self.play_loc_r[0]: self.play_loc_r[0] + self.play_height,
                self.play_loc_r[1]: self.play_loc_r[1] + self.play_width]
        # Combine
        concat_img = np.concatenate([left, right], axis=1)  #
        fn = self.save_file(concat_img, img_name.split('/')[-1], self.play_path, 'bottom')
        return fn

    def save_file(self, item, filename, save_path, kind):
        filename = filename.lstrip('saved_frames/')
        save_filename = f'{save_path}/{filename.rstrip(".jpg")}-{kind}.jpg'
        cv2.imwrite(save_filename, item)
        return save_filename