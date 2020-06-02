#Imports
from tkinter import Label, StringVar, Button, Entry, Tk, Frame, messagebox
from PIL import Image, ImageTk
from bson.objectid import ObjectId
from pymongo import MongoClient
import redis

def Store_cache(db, cache, cache_key, reset=True, limit=1000):
    #if reset:
        #cache.delete(cache_key)
    #Query_data(db,cache,cache_key)
    #Query_statistics(db,cache,cache_key)
    #Insert_in_database(db,cache,cache_key)
    #Delete_of_database(db,cache,cache_key)
    Update_in_database(db,cache,cache_key)

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

def Insert_in_database(db, cache, cache_key):
    query={'show_id':'01010101','title':'SuperHot','director':"Diego Ramirez",'cast': "Victor, Omar",'country':'Mexico','date_added':"June 1, 2020",'release_year':'2020','rating':'TV-PG','duration':'75 min','listed_in':"A girl comes by and said oye estas muy guapo and then everything changed...",} 
    db.insert_one(query)
    print("Inserted in the database :")
    print(" ",query)

def Delete_of_database(db, cache, cache_key):
    query={'title':'SuperHotRELOADED'} 
    db.delete_one(query)
    print("Deleted from the database :")
    print(" ",query)

def Update_in_database(db, cache, cache_key):
    old_query={'show_id':'01010101','title':'SuperHot','director':"Diego Ramirez",'cast': "Victor, Omar",'country':'Mexico','date_added':"June 1, 2020",'release_year':'2020','rating':'TV-PG','duration':'75 min','listed_in':"A girl comes by and said oye estas muy guapo and then everything changed...",}
    new_query={'show_id':'01010101','title':'SuperHot RELOADED','director':"Diego Ramirez",'cast': "Victor, Omar",'country':'Mexico','date_added':"June 1, 2020",'release_year':'2020','rating':'TV-PG','duration':'75 min','listed_in':"A girl comes by and said oye hace tiempo que no hablamos and then everything changed...again...for the last time...",}
    db.update(old_query,new_query,True)
    print("Updated from the database :")
    print(" ",new_query)

if __name__ == '__main__':

    #Connections
    client = MongoClient()
    db = client.Netflix
    col = db.Titles
    cache = redis.from_url('redis://localhost:6379', db=0)
    cache_key = "cache_set"
    MAX_EXPIRE_DURATION = 24 * 3600
    #Busqueda y almacenamiento de queries
    Store_cache(col, cache, cache_key)
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