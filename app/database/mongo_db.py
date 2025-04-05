from pymongo import MongoClient
from bson.objectid import ObjectId
from config import Config
import json

client = MongoClient(Config.MONGO_URI) # creates a connection to MongoDB Atlas cluster using username + PW

db = client["VeggieTalesDB"] # selects my database from the cluster
collection = db["Batches"] # selects the collection of product_batches from the database

# Custom JSON encoder to handle MongoDB ObjectId
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

def find_batch_by_ID(batch_id):
   # Find the object within our database with the specified batch_id
   result = collection.find_one({"_id": ObjectId(batch_id)})
   return result