import tkinter as tk

root = tk.Tk()

framelist = []      # List to hold all the frames
frame_index = 0     # Frame index

while True:
    try:
        # Read a frame from GIF file
        part = 'gif -index {}'.format(frame_index)
        frame = tk.PhotoImage(file='face1.gif', format=part)
    except:
        last_frame = frame_index - 1    # Save index for last frame
        break               # Will break when GIF index is reached
    framelist.append(frame)
    frame_index += 1        # Next frame index

def animate(frame_number):
    print(len(framelist))
    if frame_number > last_frame:
        frame_number = 0
    label.config(image=framelist[frame_number]) 
    root.after(50, animate, frame_number+1)

label = tk.Label(root, bg="#000000")
label.pack()

animate(0)  # Start animation

root.mainloop()