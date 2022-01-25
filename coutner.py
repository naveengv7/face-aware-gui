import tkinter

def button_countdown(i, label):
    if i > 0:
        i -= 1
        label.set(i)
        root.after(1000, lambda: button_countdown(i, label))
    else:
        close()

def close():
    root.destroy()

root = tkinter.Tk()

counter = 10
button_label = tkinter.StringVar()
button_label.set(counter)
tkinter.Button(root, textvariable=button_label, command=close).pack()
button_countdown(counter, button_label)

root.mainloop()