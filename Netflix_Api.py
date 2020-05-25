#Imports
from tkinter import Label, StringVar, Button, Entry, Tk, Frame, messagebox
from PIL import Image, ImageTk

#Definitions

#Main
window = Tk()
window.title("Netflix")
window.maxsize(1010, 610)
window.config(bg = "black")

#Left_Frame_design and Right_Frame_design and center
center_frame_1 = Frame(window, width = 990, height = 590, bg='red')
center_frame_1.grid(row = 0, column = 0, padx = 10, pady = 10)
left_frame = Frame(center_frame_1, width = 290, height = 570, bg='black')
left_frame.grid(row = 0, column = 0, padx = 10, pady = 10)
right_frame = Frame(center_frame_1, width = 650, height = 570, bg='black')
right_frame.grid(row = 0, column = 1, padx = 10, pady = 10)

#Left_Frame_design
load = Image.open("Netflix.png")
render = ImageTk.PhotoImage(load)
img = Label(left_frame, image = render, bg = "black").grid(row = 0, column = 0, padx = 0, pady = 0)

#Right_Frame_design

window.mainloop()