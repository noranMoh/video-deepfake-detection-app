import os
import cv2
import numpy as np
from dataPreprocessing.env import DOWNLOAD_DIR
from dataPreprocessing.opticalFlow import calculateOpticalFlow

def detect_faces_haar(frame):
    # Load the pre-trained Haar Cascade model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert frame to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    face_images = []
    for (x, y, w, h) in faces:
        face = frame[y:y + h, x:x + w]
        face_images.append(face)
    return face_images


def extract_frames(video_path):
    """Given the video path, extract every frame from video."""
    print(video_path)
    reader = cv2.VideoCapture(video_path)
    frameCount = int(reader.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(reader.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(frameCount)
    buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))

    frame_num = 0
    while reader.isOpened():
        success, image = reader.read()
        if not success:
            break
        buf[frame_num] = image
        frame_num += 1
    reader.release()

    return buf


def process(path, video_type, num_frames, offset, saved_dir):
    """Save consecutive frames.
    """
    np.random.seed(0)

    if not path.endswith('.mp4'):
        return

    # extract frames from videos
    frames = extract_frames(path)

    # if video has the number of frames <= 1, skip
    if len(frames) > 1:

        sel_indices = np.random.choice(len(frames) - 1, min(num_frames, len(frames) - 1), replace=False)
        #print(len(sel_indices))
        for i, idx in enumerate(sel_indices):
            #saved_path = os.path.join(saved_dir, str(idx))

            if not os.path.exists(saved_dir):
                os.makedirs(saved_dir)

            save_path = saved_dir + '/' + video_type

            if not os.path.exists(save_path):
                os.makedirs(save_path)

            split_path = path.rsplit('/', 2)

            save_path = save_path + '/' + split_path[-2]

            if not os.path.exists(save_path):
                os.makedirs(save_path)

            prev_faces = detect_faces_haar(frames[idx])
            next_faces = detect_faces_haar(frames[idx + offset])

            # Calculate optical flow on each detected face
            for i, (prev_face, next_face) in enumerate(zip(prev_faces, next_faces)):
                rgb_flow = calculateOpticalFlow(prev_faces[0], next_faces[0])
                cv2.imwrite(os.path.join(save_path, split_path[-1][:-4] + '_' + str(idx) + '_' + str(i) + '.png'), rgb_flow)

            #rgb_flow = calculateOpticalFlow(frames[idx],  frames[idx + offset])
            #print(save_path)
            #np.save(os.path.join(save_path, split_path[-1][:-4] + '_' + str(idx)), rgb_flow)


           # cv2.imwrite(os.path.join(save_path, split_path[-1][:-4] + '_' + str(idx) + '.png'), rgb_flow)

            #cv2.imwrite(os.path.join(save_path, '1.png'), frames[idx])
            #cv2.imwrite(os.path.join(save_path, '2.png'), frames[idx + offset])


def main():

    data_sets = ['training_set','validation_set']
    types = ['Real','Fake']
    progress = 0
    for dataset in data_sets:
        for videoType in types:
            path = DOWNLOAD_DIR + '/' + dataset
            path = path + '/' + videoType + '_set'

            for subdir, dirs, files in os.walk(path):
                for file in files:
                    process(os.path.join(subdir, file), videoType, num_frames=30, offset=1,saved_dir='OpticalFLow' + dataset)
                    progress = progress + 1
                    print(progress)
if __name__ == "__main__":
    main()
