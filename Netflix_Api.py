#Imports
from tkinter import Label, StringVar, Button, Entry, Tk, Frame, messagebox
from PIL import Image, ImageTk
from bson import ObjectId
from pymongo import MongoClient
import redis

#def cache_ids(col, cache, cache_key, reset=True, limit=1000):
def cache_ids():
    """if reset:
        # O(M) where M = number of items in key
        cache.delete(cache_key)"""
        #Query
    query={'title':"Norm of the North: King Sized Adventure"}
    projection={'_id':0, 'director':1} # show x but not show _id
    cursor=col.find(query,projection)#.limit(limit)
    for doc in cursor:
        print(doc)
    # O(N) where N is the number of IDs to be cached
    for doc in cursor:
        cache.sadd(cache_key, unicode(doc['_id']))

if __name__ == '__main__':

    #Connections
    client = MongoClient()
    db = client.Netflix
    col = db.Titles
    cache = redis.from_url('redis://localhost:6379', db=0)
    cache_key = 'id_set'
    """cache_ids(db, cache, cache_key)"""
    cache_ids()

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

    """# Random ID determination? Redis SRANDMEMBER!
    _id = cache.srandmember(cache_key)
    
    # Random doc
    doc = db[COLLECTION].find_one({'_id': ObjectId(_id)})
    
    # Need N random IDs? Redis SRANDMEMBER still!
    _ids = [ObjectId(_id) for _id in cache.srandmember(cache_key, N)]
    
    # Random docs
    docs = db[COLLECTION].find({'_id': {'$in': _ids}})"""

    

window.mainloop()