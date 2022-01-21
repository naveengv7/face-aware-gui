from fileinput import filename
from tkinter import *
from tkinter import messagebox
from turtle import left, right
from PIL import Image, ImageTk
from click import command
import cv2
import os
from datetime import datetime
from check_image_quality import check_image_quality


cap = None
fps = 1
camera_panel = None
capture_identifier = None
frame_cleared =False
image_list = []
original_image_list = []
subject_directory = None

data_directory = "data/"




def scan():
    print("calling")
    global cap,fps,capture_identifier,camera_panel,image_list,original_image_list
    ret, img = cap.read()
    if ret:

        orginal_img = img.copy()
        check_img = img.copy()

         
        #for display and grid
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(img)
        img = img.resize((224,224)) # new width & height
        img = ImageTk.PhotoImage(image=img)
        #for display and grid
        

        if check_image_quality(check_img):
            image_list.append(img)
            original_image_list.append(orginal_img)


        #tkimg = ImageTk.PhotoImage(img)
        camera_panel.config(image=img)
        camera_panel.tkimg = img #
     

    if len(image_list)>5:
        print("image more than 5")
        stopScan()

    if camera_panel:
        capture_identifier = camera_panel.after(fps, scan) # change 25 to other value to adjust FPS


def create_folder_for_subject():
    global subject_directory,data_directory

    n =sub_name_var.get()
    if not os.path.exists(data_directory+n):
        os.mkdir(data_directory+n)

    subject_directory = data_directory+n+'/'
    

def startScan():
    global cap,camera_panel,image_list,original_image_list

    messagebox.showinfo("Focus on Camera", "Please Focus on camera and wait")

    create_folder_for_subject()
    image_list.clear()
    original_image_list.clear()
    clear_grid_image()


    if cap is None:
        cap = cv2.VideoCapture(0)
        #clear_frame()
        
        if camera_panel is None:
            Label(right_frame,text="Capturing images.please focus on camera..").grid(row=0,column=0,columnspan=4)
            camera_panel = Label(right_frame,)
            camera_panel.grid(row=1,column=0,columnspan=4)

        scan() # start the capture loop
    else:
        print('capture already started')

def stopScan():
    global cap,camera_panel,capture_identifier
    if cap is not None:
        cap.release()
        cap = None
        
        camera_panel.after_cancel(capture_identifier)
        clear_grid_image()
        clear_frame()
        plot_images(right_frame)
        print('capture stop')   
    else:
        print('capture not started')   
     

def clear_frame():
    global camera_panel
    for widgets in right_frame.winfo_children():
        widgets.destroy()
    camera_panel = None

def clear_grid_image():
    for widgets in right_frame.winfo_children():
        widgets.destroy()


def click_on_image(img_index):
    now = datetime.now() 
    image_name = now.strftime("%m_%d_%Y_%H_%M_%S.jpg")
    print("image name saved:",image_name)
    cv2.imwrite(subject_directory+image_name,original_image_list[int(img_index)])
    messagebox.showinfo("Image Saved", "Thank you Image Saved")
    clear_grid_image()


def plot_images(parent_name):
    global image_list
    #filename = ['landscape1.png','landscape2.png','landscape3.png','landscape3.png','landscape3.png']
    #filename = image_list
    col=1 # start from column 1
    row=3 # start from row 3 
    i = 0

    Label(parent_name,text="Click any image you want to save").grid(row=0,column=0,columnspan=4)

    for img in image_list:
        
        #img=Image.open(f) # read the image file
        
        # img = Image.fromarray(img) 
        # img=img.resize((200,200)) # new width & height
        # img=ImageTk.PhotoImage(img)

        
        e1 = Button(parent_name, text="Apple",
            command=lambda m=str(i): click_on_image(m))

        e1.grid(row=row,column=col)
        e1.image = img
        e1['image']=img # garbage collection 
         
        if(col==3): # start new line after third column
            row=row+1# start wtih next row
            col=1    # start with first column
        else:       # within the same row 
            col=col+1 # increase to next column  

        i=i+1



###########################
### GUI START
###########################

root = Tk()
root.title('CITER FACE QUALITY ASSESMENT')
root.geometry('1000x600')
# root.attributes('-fullscreen', True)

#getting screen width and height of display
# width= root.winfo_screenwidth() 
# height= root.winfo_screenheight()

# #setting tkinter window size
# root.geometry("%dx%d" % (width, height))


#Label(root, text='Click on start button and focus on camera', padx=5, pady=5).grid(row=0,column=0)

#frame define
left_frame = Frame(root)
right_frame = Frame(root)

left_frame.grid(row=0, column=0, sticky="nsew")
right_frame.grid(row=0, column=1, sticky="nsew")

#root.grid_columnconfigure(1, weight=3, uniform="group1")
root.grid_columnconfigure(0, weight=1, uniform="group1")
root.grid_columnconfigure(1, weight=2, uniform="group1")
root.grid_rowconfigure(0, weight=1)
#frame defien end


#left frame content start
frame1 = Frame(left_frame, padx=5, pady=5)
frame1.grid(row=0, column=1)

frame2 = Frame(left_frame, padx=5, pady=5)
frame2.grid(row=0, column=2)

frame3 = Frame(left_frame, padx=5, pady=5,bg='red')
frame3.grid(row=1, column=0,columnspan=2)


# input start
Label(frame1, text='Subject Name', padx=5, pady=5).pack()
Label(frame1, text='Subject ID', padx=5, pady=5).pack()


sub_name_var=StringVar()
sub_id_var=StringVar()
sub_name_var.set("test_subject")
sub_id_var.set("1") 

subject_name = Entry(frame2,textvariable=sub_name_var).pack(padx=5, pady=5)
subject_id   = Entry(frame2,textvariable=sub_id_var).pack(padx=5, pady=5)

Button(frame3, text='Stop process', padx=3, pady=10,command=stopScan).pack(side=LEFT)
Button(frame3, text='Start process', padx=3, pady=10,command=startScan).pack(side=RIGHT)
#input end

#left frame content end

root.mainloop()

if cap:
    cap.release()