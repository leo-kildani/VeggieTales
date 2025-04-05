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
   return (result)

def update_batch(batch_id, gemini_data):
    """
    Update the batch with its corresponding batch ID in the VeggieTales database
    with the summary, analysis, and rating.
    """
    # Prepare the update data
    update_data = {
        "story": gemini_data.get("story"),
        "score": gemini_data.get("score"),
        "analysis": gemini_data.get("analysis")
    }
    
    # Update the document in the collection
    result = collection.update_one(
        {"_id": ObjectId(batch_id)},  # Find the document by batch_id
        {"$set": update_data}         # Set the new data
    )
    
    # Check if the update was successful
    if result.matched_count > 0:
        return {"message": "Batch updated successfully"}
    else:
        return {"error": "Batch not found"}, 404