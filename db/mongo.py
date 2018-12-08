from pymongo import MongoClient

client = MongoClient()
db = client.color_correction
all = db.example.find()
for each in all:
    print(each)
