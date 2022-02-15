from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk,ImageDraw
import cv2
import os,time
from datetime import datetime

def stop_scan():
    pass

def start_camera_capture():
    pass

###########################
### GUI START
###########################

root = Tk()
root.title('CITER FACE QUALITY ASSESMENT')
root.geometry('1000x600')
# root.attributes('-fullscreen', True)

#getting screen width and height of display
#width= root.winfo_screenwidth() 
#height= root.winfo_screenheight()

# #setting tkinter window size
#root.geometry("%dx%d" % (width, height))

root.geometry("%dx%d" % (900, 600))


left_frame = Frame(root)
left_frame.pack(side=LEFT,anchor=NW)
#left_frame.place(x=0,y=0)
right_frame = Frame(root)
right_frame.pack(side=RIGHT)
#right_frame.place(x=1,y=0)


#show logo
bg = PhotoImage(file = 'asset/CITeR-logo.png')
logo=Label(left_frame, image=bg)
logo.pack(side=TOP)
#show logo end


#first frame start
message_frame = Frame(left_frame)
message_frame.pack()

message_label=Label(message_frame, text="Fill out the form and \nclick start button to start",font=('Aerial 15 bold'))
message_label.pack()
#message_label.grid(row=0, column=2,pady=10,sticky="nsew")
#first frame end


#form frame start
form_frame =Frame(left_frame)
form_frame.pack()

sub_name_var=StringVar()
sub_id_var=StringVar()
sub_name_var.set("test_subject")
sub_id_var.set("1") 

Label(form_frame,text="Subject Name").pack()
subject_name = Entry(form_frame,textvariable=sub_name_var).pack(padx=5)
Label(form_frame,text="Subject Id").pack(padx=5)
subject_id   = Entry(form_frame,textvariable=sub_id_var).pack(padx=5)

#Button(form_frame,text='Stop',command=stop_scan).pack()
#Button(form_frame,text="Start" ,command=start_camera_capture).pack()

#Start button
start_button = Button(bd=0,bg="#04C35C",fg="#FFFFFF",text="Start",font=("Roboto", 30 * -1),borderwidth=0,
                        highlightthickness=0,command=start_camera_capture,relief="groove")
start_button.place(x=0,y=410,width=360,height=50)

#Stop button
stop_button = Button(bd=0,bg="#1B1D1C",fg="#FFFFFF",text="Stop",font=("Roboto", 30 * -1),borderwidth=0,highlightthickness=0,
                        command=stop_scan,relief="raised")
stop_button.place(x=0,y=480,width=360,height=50)

#form frame end


# camera frame start 
camera_frame =Frame(right_frame,bg="gray")
camera_frame.pack()

#add new camera panel
camera_panel = Label(camera_frame)
camera_panel.pack()

#camera frame end

#root.iconbitmap('/home/baset/Activity/clarkson/gui/final/icon.ico')
root.iconphoto(False, PhotoImage(file='asset/icon.png'))
root.mainloop()