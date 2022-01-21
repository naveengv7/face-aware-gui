import random
import cv2
import dlib
import numpy as np

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_files/shape_predictor_68_face_landmarks.dat')

def check_image_quality(image):
    image = cv2.resize(image, (224, 224))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect the face
    rects = detector(gray, 1)

    print(len(rects))

    # Detect landmarks for each face
    for rect in rects:
        return True
        # Get the landmark points
        #shape = predictor(gray, rect)

	    # Convert it to the NumPy Array
        # shape_np = np.zeros((68, 2), dtype="int")
        # for i in range(0, 68):
        #     shape_np[i] = (shape.part(i).x, shape.part(i).y)
        # shape = shape_np

    return False


