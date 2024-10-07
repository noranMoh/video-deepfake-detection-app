import cv2
import numpy as np
import tensorflow as tf
from videoKeyframeDetector.KeyFrameDetector.key_frame_detector import keyframeDetection
from dataPreprocessing.opticalFlow import calculateOpticalFlow
from dataPreprocessing.LBP_faces import get_faces
from skimage import img_as_ubyte
from skimage.feature import local_binary_pattern

# settings for LBP
gaussian_kernel_size = (5, 5)  # Kernel size for Gaussian blur
sigma = 1.0  # Standard deviation for Gaussian kernel

radius = 1
n_points = 8 * radius
METHOD = 'uniform'


def predict_image(model, img, target_size=(299, 299)):
    img = cv2.resize(img, target_size)  # Resize the image to the target size

    img_array = tf.keras.preprocessing.image.img_to_array(img)  # convert to image array
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize the image

    prediction = model.predict(img_array, verbose=0)

    return prediction[0][0]


def predict(filepath, inception_optical, dense_optical, xception_lbp, dense_lbp, meta_classifier):
    # Extract keyframes from video
    indices, frames = keyframeDetection(filepath, 0.3)

    print('frames extracted')

    predictions_1 = []
    predictions_2 = []
    predictions_3 = []
    predictions_4 = []

    for i in range(1, len(indices)):
        # Preprocess frames for optical flow detection
        prev_frame = frames[i - 1]
        next_frame = frames[i]
        rgb_flow = calculateOpticalFlow(prev_frame, next_frame)

        prediction = predict_image(inception_optical, rgb_flow, target_size=(299, 299))
        predictions_1.append(prediction)
        prediction = predict_image(dense_optical, rgb_flow, target_size=(224, 224))
        predictions_2.append(prediction)
        # Only assess 30 keyframes
        if i > 30:
            break

    print('optical Flow predictions done')

    for i in range(0, len(indices)):
        # Preprocess frames for LBP

        frame = frames[i]
        faces = get_faces(frame)

        for face_idx, face in enumerate(faces):

            blurred_frame = cv2.GaussianBlur(face, gaussian_kernel_size, sigma)

            if len(blurred_frame.shape) == 3:
                gray_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)
            else:
                gray_frame = blurred_frame

            lbp = local_binary_pattern(gray_frame, n_points, radius, METHOD)

            lbp_image = img_as_ubyte(lbp / lbp.max())

            lbp_image = cv2.cvtColor(lbp_image, cv2.COLOR_GRAY2BGR)

            prediction = predict_image(xception_lbp, lbp_image, target_size=(299, 299))
            predictions_3.append(prediction)
            prediction = predict_image(dense_lbp, lbp_image, target_size=(224, 224))
            predictions_4.append(prediction)

        # Only assess 30 keyframes
        if i > 30:
            break

    print('LBP predictions done')

    video_prediction = [np.mean(predictions_1), np.mean(predictions_2), np.mean(predictions_3),
                        np.mean(predictions_4)]

    # Load meta classifier

    video_prediction = np.array(video_prediction)

    # Reshape the input to (1, 4) to match the expected input shape
    video_prediction = video_prediction.reshape(1, -1)

    final_prediction = meta_classifier.predict(video_prediction, verbose=0)

    if final_prediction > 0.5:
        return True

    return False
