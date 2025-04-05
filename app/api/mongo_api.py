from flask import Blueprint

mongo_api_bp = Blueprint('mongo_api', __name__)

@mongo_api_bp.route('/data', methods=['GET'])
def get_data():
    # Logic to interact with MongoDB
    return "Data from MongoDB" 