import sys
import cv2


cap = cv2.VideoCapture("v4l2src num-buffers=300 ! video/x-raw,format=UYVY,width=1280,height=720,framerate=30/1 ! videoconvert ! video/x-raw,format=BGR ! appsink  ")

w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
#cap.set(cv2.CAP_PROP_BRIGHTNESS,200)
#cap.set(cv2.CAP_PROP_AUTO_EXPOSURE,1)
#cap.set(cv2.CAP_PROP_EXPOSURE,1000)
fps = cap.get(cv2.CAP_PROP_FPS)
ex = cap.get(cv2.CAP_PROP_BRIGHTNESS)
print('Src opened, %dx%d @ %d fps ex:%d' % (w, h, fps,ex))

#gst_out = "appsrc ! video/x-raw, format=BGR ! queue ! videoconvert ! video/x-raw,format=BGRx ! nvvidconv ! nvv4l2h264enc ! h264parse ! matroskamux ! filesink location=test.mkv "
#out = cv2.VideoWriter(gst_out, cv2.CAP_GSTREAMER, 0, float(fps), (int(w), int(h)))
#if not out.isOpened():
#    print("Failed to open output")
#    exit()

if cap.isOpened():
    while True:
        ret_val, img = cap.read();
        if not ret_val:
            break;
         
        cv2.imshow('frame',img)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break
else:
    print ("pipeline open failed")

print("successfully exit")
cap.release()


