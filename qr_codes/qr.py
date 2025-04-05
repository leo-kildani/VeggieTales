from pymongo import MongoClient
import qrcode
import os
import sys

# Print current working directory to see where we're running from
current_dir = os.getcwd()
print(f"Current working directory: {current_dir}")

# Use absolute path for QR codes directory
qr_codes_dir = os.path.join(current_dir, "qr_codes_output")
print(f"QR codes will be saved to: {qr_codes_dir}")

# Create directory for QR codes if it doesn't exist
if not os.path.exists(qr_codes_dir):
    os.makedirs(qr_codes_dir)
    print(f"Created directory: {qr_codes_dir}")
else:
    print(f"Directory already exists: {qr_codes_dir}")

try:
    # Connect to MongoDB
    print("Connecting to MongoDB...")
    client = MongoClient("mongodb+srv://veggietales_user:veggietales123@veggietalescluster.51yfrzk.mongodb.net/?retryWrites=true&w=majority&appName=VeggieTalesCluster", serverSelectionTimeoutMS=5000)
    
    # Check connection
    client.server_info()
    print("Successfully connected to MongoDB")
    
    # Get collection
    collection = client["VeggieTalesDB"]["Batches"]
    
    # Count documents
    doc_count = collection.count_documents({})
    print(f"Found {doc_count} documents in collection")
    
    if doc_count == 0:
        print("No documents found in collection. Cannot generate QR codes.")
        sys.exit(1)
    
    # Base URL for QR code
    BASE_URL = "http://vegeetales.tech/"
    
    # Generate a QR code for each batch in the collection
    print("Starting QR code generation...")
    for batch in collection.find():
        batch_id = str(batch["_id"])
        print(f"Generating QR code for batch ID: {batch_id}")
        qr = qrcode.make(f"{BASE_URL}/{batch_id}")
        file_path = os.path.join(qr_codes_dir, f"batch_{batch_id}.png")
        qr.save(file_path)
        print(f"✅ QR code saved as {file_path} for {BASE_URL}/{batch_id}")
    
    print("QR code generation completed.")
    print(f"QR codes are saved in: {qr_codes_dir}")

except Exception as e:
    print(f"Error: {str(e)}")