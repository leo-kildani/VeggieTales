from flask import Blueprint

gemini_api_bp = Blueprint('gemini_api', __name__)

@gemini_api_bp.route('/info', methods=['GET'])
def get_info():
    # Logic to interact with Gemini API
    return "Data from Gemini API" 