# Import required Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2

# Create an instance of TKinter Window or frame
win = Tk()

# Set the size of the window
win.geometry("700x350")

# Create a Label to capture the Video frames
label =Label(win)
label.grid(row=0, column=0)
# canvas = Canvas(win, width = 300, height = 300)  
# canvas.pack()  
# img = ImageTk.PhotoImage(Image.open("icon.png"))  
# image_on_canvas = canvas.create_image(20, 20, anchor=NW, image=img) 

cap= cv2.VideoCapture(0)

# Define function to show frame
def show_frames():
   # Get the latest frame and convert into Image
    cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   
    start_point = (5, 5)
    end_point = (220, 220)
    color = (255, 0, 0)
    cv2image = cv2.rectangle(cv2image, start_point, end_point, color, 2)

    img = Image.fromarray(cv2image)
   # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image = img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
   # Repeat after an interval to capture continiously

    #canvas.itemconfig(image_on_canvas, image =imgtk)


    label.after(20, show_frames)

show_frames()
win.mainloop()