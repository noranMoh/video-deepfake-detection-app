import os
from env import PREPRO_DIR
import json


def get_image_path(dataset, compression, split):
    with open(os.path.join('dataloader', 'splits', '{}.json'.format(split))) as f:
        data = json.load(f)

    if dataset == 'Fake_set':
        subpath = 'Fake_set'
        dir_set = set([element for sublist in data for element in sublist])
    else:
        subpath = 'manipulated_sequences'
        dir_set = set(['{}_{}'.format(a, b) for a, b in data] + ['{}_{}'.format(b, a) for a, b in data])

    compression_path = os.path.join(PREPRO_DIR, subpath, dataset, compression)
    video_name_list = sorted(os.listdir(compression_path))

    ret_path = []
    for video_name in video_name_list:
        if video_name not in dir_set:
            continue

        path_to_video_name = os.path.join(compression_path, video_name)

        frame_number_list = sorted(os.listdir(path_to_video_name))
        for frame_number in frame_number_list:
            frame_path = os.path.join(path_to_video_name, frame_number)
            ret_path.append(frame_path)

    print('The number of consecutive frames of [{}|{}|{}]: {}'.format(dataset, compression, split, len(ret_path)))
    return ret_path