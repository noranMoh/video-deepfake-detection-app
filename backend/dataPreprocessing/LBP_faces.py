from mtcnn import MTCNN

# Initialize MTCNN detector
detector = MTCNN()


def get_faces(frame, scaleFactor=1.1, minNeighbors=5):
    results = detector.detect_faces(frame)
    # List to store cropped face images
    face_images = []

    # Loop through detected faces
    for result in results:
        x, y, width, height = result['box']
        face_image = frame[y:y + height, x:x + width]
        face_images.append(face_image)

    return face_images
