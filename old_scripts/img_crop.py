import random
from tkinter import image_names
import cv2
import numpy as np
from scipy import rand
from imutils import face_utils
#from dlib import get_frontal_face_detector,shape_predictor
import time
import numpy as np
from scipy.spatial import distance as dist
from imutils import face_utils
import math
from PIL import Image
from shapely import geometry
from numpy.linalg import norm

from encrypt_aes import encrypt,add_metadata
from dlib import get_frontal_face_detector,shape_predictor



  
def crop_square_by_nose(img, size,x,y, interpolation=cv2.INTER_AREA):
    h, w = img.shape[:2]
    print("h_w",h,w)
    min_size = np.amin([h,w])
    
    h=w/2
    w=w/2

    up= int(.35*h)
    down = int(.65*h)

    left = int(w/2)
    right = int(w/2)
    
    crop_img = img[int(y-up):int(y+down), int(x-left):int(x+right)]
    print(int(abs(y-up)),int(y+down), int(x-left),int(x+right))
    return crop_img


def check_image_quality(image,image_name,detector,predictor):
    # cv2.imwrite('tmp/'+temp_image_name+'.jpg',image)
    print("\n========================")
    print("Image Name : ", image_name)

    #image  = crop_square(image,224)
    #image = cv2.resize(image, (224, 224))
    image2 = image.copy()

    #Convert image to graysale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # shape predictor 
    start_time = time.monotonic()
    
    
    #(mStart, mEnd)  = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
    #(lStart, lEnd)  = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    #(rStart, rEnd)  = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (jStart,jEnd)   = face_utils.FACIAL_LANDMARKS_IDXS["jaw"]
    #(reStart,reEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]
    #(leStart,leEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]
    (nStart,nEnd)   = face_utils.FACIAL_LANDMARKS_IDXS["nose"]

    jaw = None
    rects = detector(image, 0)
    for rect in rects:
        print('#68_landmark_detection_time_seconds:: ', time.monotonic() - start_time)
        shape = predictor(image, rect)
        shape1 = shape
        shape = face_utils.shape_to_np(shape)
        #leftEye = shape[lStart:lEnd]
        #rightEye = shape[rStart:rEnd]
        jaw = shape[jStart:jEnd]
        #right_eyebrow = shape[reStart:reEnd]
        #left_eyebrow = shape[leStart:leEnd]
        nose = shape[nStart:nEnd]
        #mouth= shape[mStart:mEnd]
        print("nose",nose[0][0],nose[0][1])
        x = nose[0][0]
        y = nose[0][1]

        crop_imag = crop_square_by_nose(image,1200,x,y)
        cv2.imwrite('data/crop.jpg',crop_imag)



#image = cv2.imread('data/test_subject/baset_good.jpg')
image = cv2.imread('data/test_subject/nav_good.jpg')
#image = cv2.imread('data/test_subject/2022_01_28_12_43_47_967241.jpg')

#2022_03_07_12_30_42_294251

image_name = 'data/crop.jpg'
detector = get_frontal_face_detector()
predictor = shape_predictor("shape_files/shape_predictor_68_face_landmarks.dat")

check_image_quality(image,image_name,detector,predictor)

