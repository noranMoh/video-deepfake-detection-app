import os
import cv2
from dataPreprocessing.env import PREPRO_DIR
import numpy as np
import matplotlib.pyplot as plt
import spynet
import torch
from pathlib import Path
from tqdm import tqdm

dataSetCount = 1000
def calculateOpticalFlow(frame1, frame2):

    first_img = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    second_img = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    h, w = first_img.shape[:2]
    second_img = cv2.resize(second_img, (w, h))

    flow = cv2.calcOpticalFlowFarneback(np.array(first_img),
                                        np.array(second_img),
                                        None, 0.5, 3, 15, 3, 5, 1.2, 0)

    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    mask = np.zeros_like(frame1)
    mask[..., 1] = 255
    mask[..., 0] = angle * 180 / np.pi / 2
    mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    rgb_flow = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)

    return rgb_flow
def save_cv_flow(path,type):

    if not os.path.exists(os.path.join(path, '1.png')):
        return

    frame1 = cv2.imread(os.path.join(path, '1.png'))
    frame2 = cv2.imread(os.path.join(path, '2.png'))

    rgb_flow = calculateOpticalFlow(frame1, frame2)

    Path(PREPRO_DIR + '/' + type).mkdir(parents=True, exist_ok=True)

    path_to_save = str(path).rsplit('/',2)
    #plt.savefig(PREPRO_DIR + '/' + type + '/' + path_to_save[-2] + '_' + path_to_save[-1] + '.png')
    path_to_save = PREPRO_DIR + '/' + type + '/' + path_to_save[-2] + '_' + path_to_save[-1]

    cv2.imwrite(f"{path_to_save}.png", rgb_flow)

def save_spynet_flow(path):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = spynet.SpyNet.from_pretrained('flying-chair')
    model.to(device)
    model.eval()

   # flow = predict([taxi1], [taxi2])[0]

"""def save_spynet_flow(path):
    
    if not os.path.exists(os.path.join(path, '1.png')):
        return

    first_img = cv2.cvtColor(cv2.imread(os.path.join(path, '1.png')), cv2.COLOR_BGR2RGB)
    second_img = cv2.cvtColor(cv2.imread(os.path.join(path, '2.png')), cv2.COLOR_BGR2RGB)

    model = spynet.SpyNet.from_pretrained('sentinel')
    #model.eval()

    #flow = model((first_img, second_img))[0]
    #flow = spynet.flow.flow_to_image(flow)
    #Image.fromarray(flow).show()
"""

def main ():

    rootdir = os.path.expanduser("~/masterThesis/deepfakeDetection/dataPreprocessing/frames")
    img_type = 'Real'
    count_fake = 0
    count_real = 0

    for subdir, dirs, files in tqdm(os.walk(rootdir)):
        if 'Fake' in str(subdir):
            img_type = 'Fake'
            count_fake = count_fake + 1
            if count_fake > dataSetCount:
                continue
        else:
            img_type = 'Real'
            count_real = count_real + 1
            if count_real > dataSetCount:
                continue
        save_cv_flow(os.path.join(subdir),img_type)
        #save_spynet_flow(os.path.join(subdir))

if __name__ == "__main__":
    main()
