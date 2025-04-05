from flask import Blueprint, jsonify #
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import Config


client = MongoClient(Config.MONGO_URI) # creates a connection to MongoDB Atlas cluster using username + PW


db = client["VeggieTalesDB"] # selects my database from the cluster
collection = db["Batches"] # selects the collection of product_batches from the database



def find_batch_by_ID(batch_id):
   # Find the object within our database with the specified batch_id
   result = collection.find_one({"_id": ObjectId(batch_id)})
  
   if result:
       # Convert ObjectId to string for JSON serialization
       result["_id"] = str(result["_id"])
       return (result)
   else:
       return ({"error": "Batch not found"}), 404