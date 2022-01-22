import random
import cv2
from dlib import get_frontal_face_detector,shape_predictor
import numpy as np
from scipy import rand
from imutils import face_utils
from dlib import get_frontal_face_detector,shape_predictor
import time
import numpy as np
from scipy.spatial import distance as dist
from imutils import face_utils
import math
from PIL import Image,ImageStat
from shapely import geometry
from numpy.linalg import norm


#functions start

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))

def dist_ratio(jaw,nose):
    A = dist.euclidean(jaw[0], nose[0])
    B = dist.euclidean(nose[0], jaw[16])	
   
    if B == 0:
      return 0
    else:
      return A/B


def get_dist_ratio(a,b,c,d):
    A = dist.euclidean(a,b)
    B = dist.euclidean(c,d)	
    if B == 0:
      return 0
    else:
      return A/B

def face_dist_ratio(a,b,c,d):
    A = dist.euclidean(a,b)
    B = dist.euclidean(c,d)	
    if B == 0:
      return 0
    else:
      return A/B
 
def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    #return ang + 360 if ang < 0 else ang
    return ang



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


def face_detector_plot_rect(i):
    face_area = 0 
    face_cascade = cv2.CascadeClassifier('face_detector.xml')
    # Convert into grayscale
    gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        # cv2.rectangle(i, (x, y), (x+w, y+h), (255, 0, 0), 2)  # Draw the rectange around the face
        face_area = w*h

    print("Face area",face_area)

    reso = i.shape
    total_area = i.shape[0] * i.shape[1] 
    print("Resolution:", reso[0],'X',reso[1])
    print("total area: ",total_area)
    print("Face area percentage: ",face_area*100/total_area)
    # face area calculation end

def get_area_of_polygon(arr_of_tuple):
    poly = geometry.Polygon(arr_of_tuple)
    return poly.area


def glasses_detector(imag,rect,predictor):
    # glass detection start
    sp = predictor(imag, rect)
    landmarks = np.array([[p.x, p.y] for p in sp.parts()])
    nose_bridge_x = []
    nose_bridge_y = []

    for i in [28,29,30,31,33,34,35]:
        nose_bridge_x.append(landmarks[i][0])
        nose_bridge_y.append(landmarks[i][1])

    ### x_min and x_max
    x_min = min(nose_bridge_x)
    x_max = max(nose_bridge_x)

    ### ymin (from top eyebrow coordinate),  ymax
    y_min = landmarks[20][1]
    y_max = landmarks[30][1]

    img2 = imag[y_min:y_max,x_min:x_max]
    img_blur = cv2.GaussianBlur(np.array(img2),(3,3), sigmaX=0, sigmaY=0)
    #cv2_imshow(img_blur)
    edges = cv2.Canny(image =img_blur, threshold1=100, threshold2=200)
    edges_center = edges.T[(int(len(edges.T)/2))]

    if 255 in edges_center:
        print("Glass detected")
        return 1
    else:
        print("No Glass detected")
        return 0


def cv2_to_PIL(imgOpenCV): 
    return Image.fromarray(cv2.cvtColor(imgOpenCV, cv2.COLOR_BGR2RGB))


# required pil image so converted from cv2 first
def check_background_color_white(cv2_image):

    #im = Image.open(image_path)

    # convert cv2 image to pil
    im = cv2_to_PIL(cv2_image)

    #Setting the points for cropped image
    left = 0
    top = 0
    right = im.width
    bottom = im.height-im.height * 97/100 #take only 3% from top

    # # Cropped image of above dimension
    # # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))

    n,rgb = max(im1.getcolors(im1.size[0]*im1.size[1]))
    print("Background color max",rgb)

    if rgb[0] > 200 and rgb[1] > 200 and rgb[2] > 200:
        print("Background is White")
        return 1
    else:
        print("Background is Not White")
    return 0



def detect_red_eye(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # Load HAAR cascade
    eyesCascade = cv2.CascadeClassifier("haarcascade_eye.xml")
    # Detect eyes
    eyes = eyesCascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(120, 120))
    
    # For every detected eye
    for (x, y, w, h) in eyes:
        # Extract eye from the image
        eye = img[y:y+h, x:x+w]
        # Split eye image into 3 channels
        b = eye[:, :, 0]
        g = eye[:, :, 1]
        r = eye[:, :, 2]
        # Add the green and blue channels.
        bg = cv2.add(b, g)
        # Simple red eye detector.
        mask = (r > 170) &  (r > bg)
        # Convert the mask to uint8 format.
        mask = mask.astype(np.uint8)*255
       
        mask_size = mask.size
        n_zeros = np.count_nonzero(mask==0)

        if  n_zeros < mask_size :
            print("Red Eye detected")
            return 1
        else:
            print("No red eye detected")
            return 0


def mouth_aspect_ratio(mouth):
	# compute the euclidean distances between the two sets of
	# vertical mouth landmarks (x, y)-coordinates
	A = dist.euclidean(mouth[2], mouth[10]) # 51, 59
	B = dist.euclidean(mouth[4], mouth[8]) # 53, 57

	# compute the euclidean distance between the horizontal
	# mouth landmark (x, y)-coordinates
	C = dist.euclidean(mouth[0], mouth[6]) # 49, 55

	# compute the mouth aspect ratio
	mar = (A + B) / (2.0 * C)

	# return the mouth aspect ratio
	return mar



def check_image_quality(image):

    image  = crop_square(image,224)
    #image = cv2.resize(image, (224, 224))
    image2 = image.copy()

    # image brightness
    brightness = get_brightness(image)
    print("Brightness: ",brightness)

    #check background
    is_background_white = check_background_color_white(image)

    #Convert image to graysale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # blur value (laplacian) need gray image
    blur_value = blur_photo_check(gray)
    
    

    # shape predictor 
    detector = get_frontal_face_detector()
    predictor = shape_predictor("shape_files/shape_predictor_68_face_landmarks.dat")
    
    (mStart, mEnd)  = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
    (lStart, lEnd)  = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd)  = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (jStart,jEnd)   = face_utils.FACIAL_LANDMARKS_IDXS["jaw"]
    (reStart,reEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]
    (leStart,leEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]
    (nStart,nEnd)   = face_utils.FACIAL_LANDMARKS_IDXS["nose"]

    jaw = None
    rects = detector(gray, 0)
    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        jaw = shape[jStart:jEnd]
        right_eyebrow = shape[reStart:reEnd]
        left_eyebrow = shape[leStart:leEnd]
        nose = shape[nStart:nEnd]
        mouth= shape[mStart:mEnd]
        
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        jawHull = cv2.convexHull(jaw)
        right_eyebrowHull = cv2.convexHull(right_eyebrow)
        noseHull = cv2.convexHull(nose)
        left_eyebrowHull = cv2.convexHull(left_eyebrow)
        mouthHull = cv2.convexHull(mouth)
        

        cv2.line(image,tuple(jaw[0]),(jaw[16][0],jaw[0][1]), (255,255,0), 2) 
        d_ratio = dist_ratio(jaw,nose)
        print("Jaw to Eye distance Ratio:",d_ratio )
        jaw_angle = getAngle(tuple(jaw[16]),jaw[0], (jaw[16][0],jaw[0][1]))
        print("Face tilt angle: ",jaw_angle)
        print("Distance between eyes:",dist.euclidean(shape[39], shape[42]))
        left_eye_distance_ratio = get_dist_ratio(shape[42],shape[45],shape[43],shape[47])
        print("left_eye_width_height_ratio",left_eye_distance_ratio)
        right_eye_distance_ratio = get_dist_ratio(shape[36],shape[39],shape[37],shape[41])
        print("right_eye_width_height_ratio",right_eye_distance_ratio)
        mouth_distance_ratio = get_dist_ratio(shape[48],shape[54],shape[51],shape[57])
        print("mouth_width_height_ratio",mouth_distance_ratio)
        
        #is_glass = glasses_detector(image2,rect,predictor)
        #is_red_eye_detected = detect_red_eye(image_path)    

        #draw shapes on image
        cv2.drawContours(image, [leftEyeHull], 0, (255, 255, 255), 1)
        cv2.drawContours(image, [rightEyeHull], 0, (255, 255, 255), 1)
        cv2.drawContours(image, [jawHull], 0, (255, 255, 255), 1)
        cv2.drawContours(image, [right_eyebrowHull], 0, (255, 255, 255), 1)
        cv2.drawContours(image, [left_eyebrowHull], 0, (255, 255, 255), 1)
        cv2.drawContours(image, [noseHull], 0, (255, 255, 255), 1)
        cv2.drawContours(image, [mouthHull], 0, (255, 255, 255), 1)

        # temp_image_name = str(random.random())
        # cv2.imwrite('tmp/'+temp_image_name+'.jpg',image)
        # print("=========\n")
        # print("Image Name : ", temp_image_name)

        if jaw is None:
            print("--No face detected")
            return False
        elif blur_value < 5: #blur (laplacian) check
            print("--Not acceptable, Image is blurry")
            return False
        elif left_eye_distance_ratio > 6 or right_eye_distance_ratio > 6:
            print("--Not acceptable, Eye Closed") 
            return False
        elif d_ratio > 1.2 or d_ratio < .9:
            print("--Not acceptable, looking away")
            return False
        elif jaw_angle > 10 or jaw_angle < -10:
            print("--Not acceptable for tilted")
            return False
        elif brightness < 45 or brightness > 204:  # Based on histogram value
            print("--Not acceptable, Brightness issue")  
            return False
        elif is_background_white == 0:
            print("--Not acceptable, Background Color not white")
            return False

        # elif is_glass == 1:
        #     print("--Not acceptable, Glass detected")
        #     return False
        

        # elif is_red_eye_detected == 1:
        #     print("--Not acceptable, Red eye detected")
        #     return False

        else :
            print("No issue found, it's a good image")
            return True


        #return False
        #break

    

