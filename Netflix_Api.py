#Imports
from tkinter import Label, StringVar, Button, Entry, Tk, Frame, messagebox
from PIL import Image, ImageTk
from bson.objectid import ObjectId
from pymongo import MongoClient
import redis

def store_cache(db, cache, cache_key, reset=True, limit=1000):
    #if reset:
        #cache.delete(cache_key)
    #query_data(db,cache,cache_key)
    query_statistics(db,cache,cache_key)

def query_data(db, cache, cache_key):
    columns=["show_id","type","title","director","cast","country","date_added","release_year","rating","duration","listed_in","description"]
    #query={'release_year':'2019','duration':'90 min','rating':'TV-PG'}
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

def query_statistics(db, cache, cache_key):
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

if __name__ == '__main__':

    #Connections
    client = MongoClient()
    db = client.Netflix
    col = db.Titles
    cache = redis.from_url('redis://localhost:6379', db=0)
    cache_key = "cache_set"
    MAX_EXPIRE_DURATION = 24 * 3600
    #Busqueda y almacenamiento de queries
    store_cache(col, cache, cache_key)
    #

    #Definitions

    #Main
    """window = Tk()
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


    

window.mainloop()"""