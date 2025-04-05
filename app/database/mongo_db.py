from pymongo import MongoClient
from bson.objectid import ObjectId
from config import Config
import json
import qrcode




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

#def generate_QR_Code(batch_id):
#    qr = qrcode.QRCode(
#        version=1,
#        error_correction=qrcode.constants.ERROR_CORRECT_H,
#        box_size=10,
#        border=4,
#    )
 #   qr.add_data(batch_id)
 #   qr.make(fit=True)
 #   img = qr.make_image(fill_color="black", back_color="white")
 #   img_path = f"qr_code_{batch_id}.png"
 #   img.save(img_path)
 #   return img_path

#test = generate_QR_Code("67f096d6828f7d3c901cc7cb")
#print(test)