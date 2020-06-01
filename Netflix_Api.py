#Imports
from tkinter import Label, StringVar, Button, Entry, Tk, Frame, messagebox, Menu
from PIL import Image, ImageTk
from bson import ObjectId
from pymongo import MongoClient
import redis

#Definitions

if __name__ == '__main__':

    #Main
    window = Tk()
    window.title("Netflix")
    window.iconbitmap('N.ico')
    window.maxsize(1010, 610)
    window.config(bg = "black")
    menubar = Menu(window, bg = 'gray17', fg = 'gray63')
    window.config(menu = menubar)

    #Menu
    search = Menu(menubar, tearoff = 0, bg = 'gray17', fg = 'gray63')
    search.add_command(label = "ID")
    search.add_command(label = "Type")
    search.add_command(label = "Title")
    search.add_command(label = "Director")
    search.add_command(label = "Cast")
    search.add_command(label = "Country")
    search.add_command(label = "Realease year")
    search.add_command(label = "Rating")
    search.add_command(label = "Search and have \n the statistics")
    menubar.add_cascade(label = "Search", menu = search)
    
    modify = Menu(menubar, tearoff = 0, bg = 'gray17', fg = 'gray63')
    modify.add_command(label = "Edit")
    modify.add_command(label = "Add")
    modify.add_command(label = "Delete")
    menubar.add_cascade(label = "Modify Database", menu = modify)

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
    in_1 = Label(left_frame, text = "INSTRUCTIONS", bg = "black", fg = "white", font = ("Verdana", 24)).grid(row = 1, column = 0, padx = 5, pady = 5)
    in_2 = Label(left_frame, text = "Select the type of your search", bg = "black", fg = "white", font = ("Verdana", 12)).grid(row = 2, column = 0, padx = 5, pady = 5)
    in_3 = Label(left_frame, text = "or if you prefer", bg = "black", fg = "white", font = ("Verdana", 12)).grid(row = 3, column = 0, padx = 5, pady = 5)

    #Right_Frame_design

    window.mainloop()