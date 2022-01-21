from tkinter import *
from PIL import Image,ImageTk
from matplotlib.patches import FancyArrow
from sklearn.feature_extraction import image

#from matplotlib.font_manager import _Weight

cap = None

def click_on_image(f):
    print(f)

def plot_images(parent_name):
    filename = ['landscape1.png','landscape2.png','landscape3.png','landscape3.png','landscape3.png']
    col=1 # start from column 1
    row=3 # start from row 3 
    i = 0
    for f in filename:
        img=Image.open(f) # read the image file
        img=img.resize((200,200)) # new width & height
        img=ImageTk.PhotoImage(img)
        #e1 =Label(parent_name)
        
        e1 = Button(parent_name, text="Apple",
            command=lambda m="It is an apple"+str(i): click_on_image(m))

        e1.grid(row=row,column=col)
        e1.image = img
        e1['image']=img # garbage collection 
         
         
        if(col==3): # start new line after third column
            row=row+1# start wtih next row
            col=1    # start with first column
        else:       # within the same row 
            col=col+1 # increase to next column  

        i= i+1


root = Tk()
root.title('CITER FACE QUALITY ASSESMENT')
# root.geometry('600x600')
# root.attributes('-fullscreen', True)

#getting screen width and height of display
width= root.winfo_screenwidth() 
height= root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))


#frame define
left_frame = Frame(root)
right_frame = Frame(root)

left_frame.grid(row=0, column=0,sticky="nsew")
right_frame.grid(row=0, column=1,sticky="nsew")

root.grid_columnconfigure(0, weight=1, uniform="group1")
root.grid_columnconfigure(1, weight=2, uniform="group1")
root.grid_rowconfigure(0, weight=1)
#frame defien end

plot_images(right_frame)
#plot_multiple_images(right_frame)



root.mainloop()
if cap:
    cap.release()