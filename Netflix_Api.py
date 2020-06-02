#Imports
from tkinter import Label, StringVar, Button, Entry, Tk, Frame, messagebox, Menu
from PIL import Image, ImageTk
from bson.objectid import ObjectId
from pymongo import MongoClient
from functools import partial
import redis

def Store_cache(db, cache, cache_key, reset=True, limit=1000):
    if reset:
       cache.delete(cache_key)
    #Window
    window = Tk()
    window.title("Netflix")
    window.iconbitmap('N.ico')
    window.maxsize(1010, 610)
    window.config(bg = "black")
    menubar = Menu(window, bg = 'gray17', fg = 'gray63')
    window.config(menu = menubar)

    #Variables
    right_display = StringVar()
    right_display.set('NETFLIX')

    #Left_Frame_design and Right_Frame_design and center
    center_frame_1 = Frame(window, width = 990, height = 590, bg='red')
    center_frame_1.grid(row = 0, column = 0, padx = 10, pady = 10)
    left_frame = Frame(center_frame_1, width = 290, height = 570, bg='black')
    left_frame.grid(row = 0, column = 0, padx = 10, pady = 10)
    right_frame = Frame(center_frame_1, width = 650, height = 570, bg='gray10')
    right_frame.grid(row = 0, column = 1, padx = 10, pady = 10)

    #Menu
    search = Menu(menubar, tearoff = 0, bg = 'gray17', fg = 'gray63')
    search.add_command(label = "ID", command = partial(id_s,right_display,right_frame,db,cache,cache_key))
    search.add_command(label = "Type", command = partial(type_s,right_display,right_frame,db,cache,cache_key))
    search.add_command(label = "Title", command = partial(title_s,right_display,right_frame,db,cache,cache_key))
    search.add_command(label = "Director", command = partial(director_s,right_display,right_frame,db,cache,cache_key))
    search.add_command(label = "Cast", command = partial(cast_s,right_display,right_frame,db,cache,cache_key))
    search.add_command(label = "Country", command = partial(country_s,right_display,right_frame,db,cache,cache_key))
    search.add_command(label = "Realease year", command = partial(realease_year_s,right_display,right_frame,db,cache,cache_key))
    search.add_command(label = "Rating", command = partial(rating_s,right_display,right_frame,db,cache,cache_key))
    search.add_command(label = "Search and have the statistics", command = partial(search_s_S,right_display,right_frame,db,cache,cache_key))
    menubar.add_cascade(label = "Search", menu = search)

    modify = Menu(menubar, tearoff = 0, bg = 'gray17', fg = 'gray63')
    modify.add_command(label = "Edit", command = partial(edit_m,right_display,right_frame,db,cache,cache_key))
    modify.add_command(label = "Add", command = partial(add_m,right_display,right_frame,db,cache,cache_key))
    modify.add_command(label = "Delete", command = partial(delete_m,right_display,right_frame,db,cache,cache_key))
    menubar.add_cascade(label = "Modify Database", menu = modify)

    #Left_Frame_design
    load = Image.open("Netflix.png")
    render = ImageTk.PhotoImage(load)
    img = Label(left_frame, image = render, bg = "black").grid(row = 0, column = 0, padx = 0, pady = 0)
    in_1 = Label(left_frame, text = "INSTRUCTIONS", bg = "black", fg = "white", font = ("Verdana", 24)).grid(row = 1, column = 0, padx = 5, pady = 5)
    in_2 = Label(left_frame, text = "Select the type of your search", bg = "black", fg = "white", font = ("Verdana", 12)).grid(row = 2, column = 0, padx = 5, pady = 5)
    in_3 = Label(left_frame, text = "or if you prefer", bg = "black", fg = "white", font = ("Verdana", 12)).grid(row = 3, column = 0, padx = 5, pady = 5)
    in_4 = Label(left_frame, text = "to add, edit or delete someting \n on the", bg = "black", fg = "white", font = ("Verdana", 12)).grid(row = 4, column = 0, padx = 5, pady = 5)
    in_3 = Label(left_frame, text = "DATABASE", bg = "black", fg = "white", font = ("Verdana", 16)).grid(row = 5, column = 0, padx = 5, pady = 5)

    #Right_Frame_design
    an_1 = Label(right_frame, text = "Welcome to the app", bg = "gray10", fg = "gray55", font = ("Verdana", 24)).grid(row = 0, column = 0, padx = 5, pady = 5)
    an_2 = Label(right_frame, textvariable = right_display, bg = "gray10", fg = "gray55", font = ("Verdana", 18)).grid(row = 1, column = 0, padx = 5, pady = 5)

    window.mainloop()

def Query_data(db, cache, cache_key):
    columns=["show_id","type","title","director","cast","country","date_added","release_year","rating","duration","listed_in","description"]
    query={'show_id':'80163890'}
    if not cache.sismember(cache_key, str(query)):
        print("Searching in the mongo database...")
        cursor=db.find(query).limit(1000)
        for doc in cursor:
            cache.hmset("query:{}".format(str(query)),{"show_id":doc['show_id'],"type":doc['type'],"title":doc['title'],"director":doc['director'],"cast":doc['cast'],"country":doc['country'],"date_added":doc['date_added'],"release_year":doc['release_year'],"rating":doc['rating'],"duration":doc['duration'],"listed_in":doc['listed_in'],"description":doc['description']})
            print("Search result: ")
            print("         ",cache.hget("query:{}".format(str(query)), "title").decode("UTF-8"))
            cache.sadd(cache_key, str(query))
            cache.expire(cache_key, MAX_EXPIRE_DURATION)
    else:
        print("Searching in the cache...")
        print("Search result: ")
        for col in columns:
            print(col,": ",cache.hget("query:{}".format(str(query)), col).decode("UTF-8"))

def Query_statistics(db, cache, cache_key):
    query={'release_year':'2019','duration':'90 min','rating':'TV-PG'}
    if not cache.sismember(cache_key, str(query)):
        print("Searching in the mongo database...")
        cursor=db.find(query).limit(1000).count()
        cache.hmset("query:{}".format(str(query)),{"result":cursor})
        print("Search result: ")
        print("         ",cache.hget("query:{}".format(str(query)), "result").decode("UTF-8"))
        cache.sadd(cache_key, str(query))
        cache.expire(cache_key, MAX_EXPIRE_DURATION)
    else:
        print("Searching in the cache...")
        print("Search result: ")
        print("         ",cache.hget("query:{}".format(str(query)), "result").decode("UTF-8"))

def id_s(right_display, right_frame, db,cache,cache_key):
    right_display.set("Search by ID")
    an_2 = Label(right_frame, textvariable = right_display, bg = "gray10", fg = "gray55", font = ("Verdana", 18)).grid(row = 1, column = 0, padx = 5, pady = 5)

def type_s(right_display, right_frame, db,cache,cache_key):
    right_display.set("Search by TYPE")
    an_2 = Label(right_frame, textvariable = right_display, bg = "gray10", fg = "gray55", font = ("Verdana", 18)).grid(row = 1, column = 0, padx = 5, pady = 5)

def title_s(right_display, right_frame, db,cache,cache_key):
    right_display.set("Search by TITLE")
    an_2 = Label(right_frame, textvariable = right_display, bg = "gray10", fg = "gray55", font = ("Verdana", 18)).grid(row = 1, column = 0, padx = 5, pady = 5)

def director_s(right_display, right_frame, db,cache,cache_key):
    right_display.set("Search by DIRECTOR")
    an_2 = Label(right_frame, textvariable = right_display, bg = "gray10", fg = "gray55", font = ("Verdana", 18)).grid(row = 1, column = 0, padx = 5, pady = 5)

def cast_s(right_display, right_frame, db,cache,cache_key):
    right_display.set("Search by CAST")
    an_2 = Label(right_frame, textvariable = right_display, bg = "gray10", fg = "gray55", font = ("Verdana", 18)).grid(row = 1, column = 0, padx = 5, pady = 5)

def country_s(right_display, right_frame, db,cache,cache_key):
    right_display.set("Search by COUNTRY")
    an_2 = Label(right_frame, textvariable = right_display, bg = "gray10", fg = "gray55", font = ("Verdana", 18)).grid(row = 1, column = 0, padx = 5, pady = 5)

def realease_year_s(right_display, right_frame, db,cache,cache_key):
    right_display.set("Search by REALEASE YEAR")
    an_2 = Label(right_frame, textvariable = right_display, bg = "gray10", fg = "gray55", font = ("Verdana", 18)).grid(row = 1, column = 0, padx = 5, pady = 5)

def rating_s(right_display, right_frame, db,cache,cache_key):
    right_display.set("Search by RATING")
    an_2 = Label(right_frame, textvariable = right_display, bg = "gray10", fg = "gray55", font = ("Verdana", 18)).grid(row = 1, column = 0, padx = 5, pady = 5)

def search_s_S(right_display, right_frame, db,cache,cache_key):
    right_display.set("Search by STATISTIC")
    an_2 = Label(right_frame, textvariable = right_display, bg = "gray10", fg = "gray55", font = ("Verdana", 18)).grid(row = 1, column = 0, padx = 5, pady = 5)
    Query_statistics(db,cache,cache_key)

def edit_m(right_display, right_frame, db,cache,cache_key):
    right_display.set("EDIT something to the database")
    an_2 = Label(right_frame, textvariable = right_display, bg = "gray10", fg = "gray55", font = ("Verdana", 18)).grid(row = 1, column = 0, padx = 5, pady = 5)

def add_m(right_display, right_frame, db,cache,cache_key):
    right_display.set("ADD something to the database")
    an_2 = Label(right_frame, textvariable = right_display, bg = "gray10", fg = "gray55", font = ("Verdana", 18)).grid(row = 1, column = 0, padx = 5, pady = 5)

def delete_m(right_display, right_frame, db,cache,cache_key):
    right_display.set("DELETE something to the database")
    an_2 = Label(right_frame, textvariable = right_display, bg = "gray10", fg = "gray55", font = ("Verdana", 18)).grid(row = 1, column = 0, padx = 5, pady = 5)

if __name__ == '__main__':
    #Connections
    client = MongoClient()
    db = client.Netflix
    col = db.Titles
    cache = redis.from_url('redis://localhost:6379', db=0)
    cache_key = "cache_set"
    MAX_EXPIRE_DURATION = 24 * 3600
    Store_cache(col, cache, cache_key)