from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk,ImageDraw
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
fps = 10
camera_panel = None
capture_identifier = None
frame_cleared =False
image_list = []
original_image_list = []
image_name_list=[]
subject_directory = None
capture_count=0
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


    print(height,width)
    print(start_x,start_y,end_x,end_y)

    color = (255, 0, 0)
    return cv2.rectangle(image,(start_x,start_y), (end_x,end_y), color, 4)



def draw_box_pil(img):
    w, h = 150, 150
    shape = [(40, 40), (w - 10, h - 10)]
    
    img = ImageDraw.Draw(img)
    return img.rectangle(shape, outline ="red")
    
    #img1.rectangle(shape, fill ="# ffff33", outline ="red")


def scan():
    print("calling")
    global cap,fps,capture_identifier,camera_panel,image_list,original_image_list,capture_count
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

        start_time = time.monotonic()
        if check_image_quality(check_img,image_name):
            image_list.append(img)
            original_image_list.append(orginal_img)
            image_name_list.append(image_name)
            capture_count= capture_count + 1
            message_label.config(text="Look at the camera please, captured: "+str(capture_count)+" out of 4",bg="green")
        print('##per_image_quality_check_time_seconds:: ', time.monotonic() - start_time)

        if len(image_list)>3:
            print("image more than 5")
            stop_scan()

        if camera_panel:
            capture_identifier = camera_panel.after(fps, scan) # change 25 to other value to adjust FPS


def start_camera_capture():
    global cap,camera_panel,capture_count,overall_processing_time

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
    image_name_list.clear()
    
    #add new camera panel
    camera_panel = Label(camera_frame)
    camera_panel.pack()


    if cap is None:
        #cap = cv2.VideoCapture(2)
        cap = cv2.VideoCapture(CAMERA_PORT)
        #cap.set(CAMERA_PROP_WIDTH, IMAGEWIDTH)
        #cap.set(CAMERA_PROP_HEIGHT, IMAGEHEIGHT)
        scan() # start the capture loop
    else:
        print('capture already started')




def plot_grid_image():

    message_label.config(text="Select image you want to save...")
    
    i=0
    col=1 # start from column 1
    row=2 # 2 images in a row

    for img in image_list:
        b1 = Button(camera_frame, text="select image",command=lambda m=str(i): click_on_image(m))
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

    global cap,camera_panel,capture_identifier,capture_count
    message_label.config(text="Fill out the information and click start...")
    
    #if camera_panel:
    #camera_panel.after_cancel(capture_identifier)
    remove_cameraframe_child()

    if cap is not None:
        cap.release()
        cap = None
        print('capture stop') 
        plot_grid_image()
    else:
        print('capture not started')  
    
    #clear capture variable
    capture_count=0
    image_list.clear()



###########################
### GUI START
###########################

root =Tk()
root.geometry("900x600")
root.title('CITER FACE QUALITY ASSESMENT')
root.configure(bg = "#FFFFFF")

sub_name_var=StringVar()
sub_id_var=StringVar()

#Create left canvas for start page
left_canvas = Canvas(
	root,
	bg = "#FFFFFF",
	height = 600,
	width = 360,
	bd = 0,
	highlightthickness = 0,
	relief = "ridge"
)
left_canvas.place(x=0,y=0)

#Citer logo
citer_img = ImageTk.PhotoImage(file='asset/CITeR-logo.png')
left_canvas.create_image(
	0, 
	0, 
	image=citer_img, 
	anchor=NW
)

left_canvas.create_text(
	0,
	90,
	anchor="nw",
	text="Welcome",
	fill="#4A5568",
	font=("Roboto", 24 * -1)
)

left_canvas.create_text(
	0,
	130,
	anchor="nw",
	text="Fill out the form and\nclick start button to start",
	fill="#1A202C",
	font=("RobotoRoman SemiBold", 24 * -1)
)

left_canvas.create_text(
	0,
	200,
	anchor="nw",
	text="Subject name",
	fill="#4A5568",
	font=("Roboto", 24 * -1)
)

left_canvas.create_text(
	0,
	300,
	anchor="nw",
	text="Subject ID",
	fill="#4A5568",
	font=("Roboto", 24 * -1)
)

entry_1 = Entry(
	bd=0,
	bg="#FFFFFF",
	font=("Roboto", 24 * -1),
	highlightthickness=1,
	textvariable=sub_name_var
)
entry_1.place(
	x=0,
	y=245,
	width=360,
	height=40
)

entry_2 = Entry(
	bd=0,
	bg="#FFFFFF",
	font=("Roboto", 24 * -1),
	highlightthickness=1,
	textvariable=sub_id_var
)
entry_2.place(
	x=0,
	y=345,
	width=360,
	height=40
)

start_button = Button(
	bd=0,
	bg="#04C35C",
	fg="#FFFFFF",
	text="Start",
	font=("Roboto", 30 * -1),
	borderwidth=0,
	highlightthickness=0,
	command=start_camera_capture,
	relief="solid"
)
start_button.place(
	x=0,
	y=410,
	width=360,
	height=50
)

stop_button = Button(
	bd=0,
	bg="#1B1D1C",
	fg="#FFFFFF",
	text="Stop",
	font=("Roboto", 30 * -1),
	borderwidth=0,
	highlightthickness=0,
	command=stop_scan,
	relief="solid"
)

stop_button.place(
	x=0,
	y=480,
	width=360,
	height=50
)	

right_canvas1 = Canvas(
	root,
	bg = "#545151",
	height = 300,
	width = 270,
	bd = 0,
	highlightthickness = 3,
	relief = "ridge"
)

#Create right side canvas for camera frames
right_canvas1.place(x=360,y=0)

camera_frame=Frame(right_canvas1)
camera_frame.pack()
camera_panel=Label(camera_frame)
camera_panel.pack()

#first frame start
message_frame = Frame(right_canvas1)
message_frame.pack()

message_label=Label(message_frame, text="",font=('Aerial 15 bold'))
message_label.grid(row=0, column=2,pady=10,sticky="nsew")
#first frame end


#main loop
root.resizable(False,False)
root.mainloop()

if cap:
    cap.release()