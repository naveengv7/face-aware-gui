import random
import cv2
import dlib
import numpy as np

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_files/shape_predictor_68_face_landmarks.dat')

from numpy.linalg import norm
def get_brightness(img):
    if len(img.shape) == 3:
        # Colored RGB or BGR (*Do Not* use HSV images with this function)
        # create brightness with euclidean norm
        return np.average(norm(img, axis=2)) / np.sqrt(3)
    else:
        # Grayscale
        return np.average(img)


#blur check need gray scale image
def blur_photo_check(grey_img):
 # img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
  laplacian_var = cv2.Laplacian(grey_img, cv2.CV_64F).var()
  print("blur value:",laplacian_var)
  return laplacian_var

def crop_square(img, size, interpolation=cv2.INTER_AREA):
    h, w = img.shape[:2]
    min_size = np.amin([h,w])

    # Centralize and crop
    crop_img = img[int(h/2-min_size/2):int(h/2+min_size/2), int(w/2-min_size/2):int(w/2+min_size/2)]
    resized = cv2.resize(crop_img, (size, size), interpolation=interpolation)
    return resized







def check_image_quality(image):
    image = cv2.resize(image, (224, 224))


    #brightness = get_brightness(image)
    #rint("brightness =====",bright)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    print("blur check: ",blur_photo_check(gray))
    

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


