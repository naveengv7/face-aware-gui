# from fileinput import filename
# from glob import glob
import imp
from tkinter import *
from tkinter import messagebox
# from turtle import color, left, right
from PIL import Image, ImageTk
# from click import command
import cv2
import os
from datetime import datetime
from check_image_quality import check_image_quality
from imx477_example import gstreamer_pipeline


cap = None
fps = 10
camera_panel = None
capture_identifier = None
frame_cleared =False
image_list = []
original_image_list = []
subject_directory = None
capture_count = 0

data_directory = "data/"


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

    print("remove camera frame child")
    for widgets in camera_frame.winfo_children():
        print(widgets)
        widgets.destroy()

    camera_panel=None



# save image on click image
def click_on_image(img_index):
    now = datetime.now() 
    image_name = now.strftime("%m_%d_%Y_%H_%M_%S.jpg")
    print("image name saved:",image_name)
    cv2.imwrite(subject_directory+image_name,original_image_list[int(img_index)])
    messagebox.showinfo("Image Saved", "Thank You, Image Saved")
    remove_cameraframe_child()




def scan():
    print("calling")
    global cap,fps,capture_identifier,camera_panel,image_list,original_image_list,capture_count
    ret, img = cap.read()

    if ret:

        orginal_img = img.copy()
        check_img = img.copy()

        #for display and grid
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(img)
        img = img.resize((150,150)) # new width & height
        img = ImageTk.PhotoImage(image=img)
        #for display and grid

        #display frame on gui 
        camera_panel.config(image=img)
        camera_panel.tkimg = img #

        if check_image_quality(check_img):
            image_list.append(img)
            original_image_list.append(orginal_img)
            capture_count= capture_count + 1
            message_label.config(text="Look at the camera please, captured: "+str(capture_count),bg="green")

        if len(image_list)>5:
            print("image more than 5")
            stop_scan()

        if camera_panel:
            capture_identifier = camera_panel.after(fps, scan) # change 25 to other value to adjust FPS


def start_camera_capture():
    global cap,camera_panel,capture_count
    

    if not check_input_field():
        return 0

    message_label.config(text="Look at the camera please...",bg="green")
    create_folder_for_subject()
    remove_cameraframe_child()
    
    #clear capture variable
    capture_count=0
    image_list.clear()
    original_image_list.clear()
    
    #add new camera panel
    camera_panel = Label(camera_frame)
    camera_panel.pack()


    if cap is None:
        #cap = cv2.VideoCapture(0)
        print(gstreamer_pipeline(flip_method=0))
        cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
        # scan() # start the capture loop
    else:
        print('capture already started')
    
    scan()



def plot_grid_image():

    message_label.config(text="Select image you want to save...")
    
    i=0
    col=1 # start from column 1
    row=3 # 3 images in a row

    for img in image_list:
        b1 = Button(camera_frame, text="Apple",command=lambda m=str(i): click_on_image(m))
        b1.grid(row=row,column=col)
        b1.image = img
        b1['image']=img # garbage collection 
         
        if(col==3):   
            row=row+1 
            col=1     
        else:         
            col=col+1   

        i=i+1
    



def stop_scan():

    global cap,camera_panel,capture_identifier,capture_count
    message_label.config(text="Fill out the information and click start...")
    
    #if camera_panel:
    #camera_panel.after_cancel(capture_identifier)
    remove_cameraframe_child()

    if cap is not None:
        #cap.release()
        #cap = None
        print('capture stop') 
        plot_grid_image()
        
    else:
        print('capture not started')  

    #clear capture variable
    capture_count=0
    image_list.clear()
    original_image_list.clear()



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
Button(form_frame,text="Start" ,command=start_camera_capture).pack(side=RIGHT)
#form frame end


# camera frame start 
camera_frame =Frame(root,bg="gray")
camera_frame.pack()

#add new camera panel
camera_panel = Label(camera_frame)
camera_panel.pack()

#camera frame end


root.mainloop()

if cap:
    cap.release()