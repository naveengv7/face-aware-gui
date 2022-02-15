from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import os,time
from datetime import datetime
from check_image_quality import check_image_quality

#remove all file from tmp
# dir = 'tmp/'
# for f in os.listdir(dir):
#     os.remove(os.path.join(dir, f))
# only for test


CAMERA_PORT = 0
IMAGEWIDTH = 3840
IMAGEHEIGHT = 2160

#Propriedades de configuracao da camera
# 3 = width da camera, 4 = height da camera
CAMERA_PROP_WIDTH = 3
CAMERA_PROP_HEIGHT = 4


#capture = cv2.VideoCapture()
#capture.open(1 + cv2.CAP_DSHOW)

#fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
#capture.set(cv2.CAP_PROP_FOURCC, fourcc)
#capture.set(cv2.CAP_PROP_FPS, 30)
#capture.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
#capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)


cap = None
fps = 3
camera_panel = None
capture_identifier = None
frame_cleared =False
image_list = []
original_image_list = []
image_name_list=[]
subject_directory = None
capture_count=0
button_click = False
overall_processing_time = 0

data_directory = "./data/"


# Resizes a image and maintains aspect ratio
def maintain_aspect_ratio_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # Grab the image size and initialize dimensions
    dim = None
    (h, w) = image.shape[:2]

    # Return original image if no need to resize
    if width is None and height is None:
        return image

    # We are resizing height if width is none
    if width is None:
        # Calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # We are resizing width if height is none
    else:
        # Calculate the ratio of the 0idth and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # Return the resized image
    return cv2.resize(image, dim, interpolation=inter)

def check_input_field():
    if sub_name_var.get() and sub_id_var.get():
        return True
    else : 
        messagebox.showinfo("Required", "Subject Name and Id Required")
        return False

#create new folder if not exist
def create_folder_for_subject():
    global subject_directory,data_directory

    n =sub_name_var.get()
    if not os.path.exists(data_directory+n):
        os.mkdir(data_directory+n)

    subject_directory = data_directory+n+'/'


# remove all child in camera frame
def remove_cameraframe_child():
    global camera_panel

    #print("remove camera frame child")
    for widgets in camera_frame.winfo_children():
        widgets.destroy()

    camera_panel=None



# save image on click image
def click_on_image(img_index):
    print("image name saved:",image_name_list[int(img_index)])
    cv2.imwrite(subject_directory+image_name_list[int(img_index)],original_image_list[int(img_index)])
    #image = maintain_aspect_ratio_resize(image, width=IMAGEWIDTH)
    #cv2.imwrite(subject_directory+image_name,maintain_aspect_ratio_resize(original_image_list[int(img_index)],width=IMAGEWIDTH))
    messagebox.showinfo("Image Saved", "Thank You, Image Saved")
    remove_cameraframe_child()
    stop_scan()

def draw_box(image):
    height,width,depth = image.shape

    # start_x = 200
    # start_y = 70

    # end_x = 500
    # end_y = 400

    start_x = int(width*30/100)
    start_y = int(height*15/100)

    end_x = int(width*70/100)
    end_y = int(height*80/100)


    #print(height,width)
    #print(start_x,start_y,end_x,end_y)

    color = (255, 0, 0)
    return cv2.rectangle(image,(start_x,start_y), (end_x,end_y), color, 4)


def scan():
    print("calling")
    global cap,fps,capture_identifier,camera_panel,image_list,original_image_list,capture_count,button_click
    ret, img = cap.read()

    now = datetime.now() 
    image_name = now.strftime("%Y_%m_%d_%H_%M_%S_%f.jpg")

    if ret:

        orginal_img = img.copy()
        check_img = img.copy()

        img = maintain_aspect_ratio_resize(img,150)
        img = draw_box(img)

        #for display and grid
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(img)
        #img = img.resize((150,150)) # new width & height
        img = ImageTk.PhotoImage(image=img)
        #for display and grid

        #display frame on gui 
        camera_panel.config(image=img)
        camera_panel.tkimg = img #

        if button_click is True:
            start_time = time.monotonic()
            if check_image_quality(check_img,image_name):
                print("adding----")
                image_list.append(img)
                original_image_list.append(orginal_img)
                image_name_list.append(image_name)
                capture_count= capture_count + 1
                message_label.config(text="Look at the camera please, captured: "+str(capture_count)+" out of 4",bg="green")
            print('##per_image_quality_check_time_seconds: ', time.monotonic() - start_time)

        if len(image_list)>1:
            print("image more than 5")
            stop_scan()

        if camera_panel:
            capture_identifier = camera_panel.after(fps, scan) # change 25 to other value to adjust FPS


def start_camera_capture(button_clk=False):
    global cap,camera_panel,capture_count,button_click,overall_processing_time
    button_click = button_clk

    if button_clk is True:
        overall_processing_time = time.monotonic()

    if not check_input_field():
        return 0

    message_label.config(text="Look at the camera please...",bg="green")
    create_folder_for_subject()
    remove_cameraframe_child()
    
    #clear variable
    capture_count=0
    image_list.clear()
    original_image_list.clear()
    
    #add new camera panel
    #if camera_frame is None:
    camera_panel = Label(camera_frame)
    camera_panel.pack()


    if cap is None:
        #cap = cv2.VideoCapture(2)
        cap = cv2.VideoCapture(CAMERA_PORT)
        #cap.set(CAMERA_PROP_WIDTH, IMAGEWIDTH)
        #cap.set(CAMERA_PROP_HEIGHT, IMAGEHEIGHT)
        
    else:
        print('capture already started')

    scan() # start the capture loop




def plot_grid_image():
    
    global overall_processing_time
    message_label.config(text="Select image you want to save...")
    
    i=0
    col=1 # start from column 1
    row=2 # 3 images in a row

    for img in image_list:
        b1 = Button(camera_frame, text="Apple",command=lambda m=str(i): click_on_image(m))
        b1.grid(row=row,column=col)
        b1.image = img
        b1['image']=img # garbage collection 
         
        if(col==2):   
            row=row+1 
            col=1     
        else:         
            col=col+1   

        i=i+1
    
    print('##overall_process_time_seconds: ', time.monotonic() - overall_processing_time)

def stop_scan():

    global cap,camera_panel,capture_identifier,button_click,capture_count
    message_label.config(text="Fill out the information and click start...")
    
    #if camera_panel:
    #camera_panel.after_cancel(capture_identifier)
    remove_cameraframe_child()

    if cap is not None:
        cap.release()
        cap = None
        print('capture stop') 
        if button_click is True:
            plot_grid_image()
            return 1
    else:
        print('capture not started')  
    
    #clear capture variable
    capture_count=0
    image_list.clear()
    
    start_camera_capture(False)



###########################
### GUI START
###########################

root = Tk()
root.title('CITER FACE QUALITY ASSESMENT')
root.geometry('1000x600')
# root.attributes('-fullscreen', True)

#getting screen width and height of display
width= root.winfo_screenwidth() 
height= root.winfo_screenheight()

# #setting tkinter window size
root.geometry("%dx%d" % (width, height))


#first frame start
message_frame = Frame(root)
message_frame.pack()

message_label=Label(message_frame, text="Fill out the form and click start button to start",font=('Aerial 15 bold'))
message_label.grid(row=0, column=2,pady=10,sticky="nsew")
#first frame end


#form frame start
form_frame =Frame(root)
form_frame.pack(pady=5)

sub_name_var=StringVar()
sub_id_var=StringVar()
sub_name_var.set("test_subject")
sub_id_var.set("1") 

Label(form_frame,text="Subject Name").pack(side=LEFT)
subject_name = Entry(form_frame,textvariable=sub_name_var).pack(side=LEFT,padx=5)
Label(form_frame,text="Subject Id").pack(side=LEFT,padx=5)
subject_id   = Entry(form_frame,textvariable=sub_id_var).pack(side=LEFT,padx=5)

Button(form_frame,text='Stop',command=stop_scan).pack(side=LEFT)
Button(form_frame,text="Start" ,command=lambda x = True:start_camera_capture(x)).pack(side=RIGHT)
#form frame end


# camera frame start 
camera_frame =Frame(root,bg="gray")
camera_frame.pack()

#add new camera panel
#camera_panel = Label(camera_frame)
#camera_panel.pack()

#camera frame end

start_camera_capture(False)

#root.iconbitmap('/home/baset/Activity/clarkson/gui/final/icon.ico')
root.iconphoto(False, PhotoImage(file='asset/icon.png'))
root.mainloop()

if cap:
    cap.release()