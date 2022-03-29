from tkinter import *
from PIL import ImageTk


root = Tk()
root.title('CITER FACE QUALITY ASSESMENT')
root.geometry('1000x600')
# root.attributes('-fullscreen', True)

#getting screen width and height of display
width= root.winfo_screenwidth() 
height= root.winfo_screenheight()

# #setting tkinter window size
root.geometry("%dx%d" % (width, height))

canvas = Canvas(width = width, height = height, bg = 'black')
canvas.pack(expand = YES, fill = BOTH)


image = ImageTk.PhotoImage(file = "face1.gif")
canvas.create_image(0,0,image = image,anchor=CENTER)


#form frame start
form_frame =Frame(canvas)
form_frame.pack(pady=5)

sub_name_var=StringVar()
sub_id_var=StringVar()
sub_name_var.set("test_subject")
sub_id_var.set("1") 

Label(form_frame,text="Subject Name").pack(side=LEFT)
subject_name = Entry(form_frame,textvariable=sub_name_var).pack(side=LEFT,padx=5)
Label(form_frame,text="Subject Id").pack(side=LEFT,padx=5)
subject_id   = Entry(form_frame,textvariable=sub_id_var).pack(side=LEFT,padx=5)

# Button(form_frame,text='Stop',command=stop_scan).pack(side=LEFT)
# Button(form_frame,text="Start" ,command=start_camera_capture).pack(side=RIGHT)
#form frame end

mainloop()