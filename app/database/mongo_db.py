from pymongo import MongoClient
from config import Config
from bson import ObjectId

client = MongoClient(Config.MONGO_URI)

db = client["VeggieTalesDB"]
collection = db["Batches"]

def find_batch(batch_id):
    """
    Find a batch by its ID.
    """
    batch = collection.find_one({"batch_id": ObjectId(batch_id)})
    return batch