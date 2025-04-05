from flask import Flask, render_template
from database.mongo_db import find_batch
from service.gemini import get_gemini_summary_rating
import json
from bson import ObjectId

# Create the Flask application instance
app = Flask(__name__)

# Define a function to handle MongoDB ObjectId serialization
def json_encoder(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

# Define the route for the root URL
@app.route('/')
# Root URL with parameter `batch_id` to redirect to the home page with a default value
@app.route('/<string:batch_id>')
def home(batch_id=None):
    """
    Render the produce page.
    """
    batch_data = find_batch(batch_id)
    batch_json = json.dumps(batch_data, default=json_encoder) if batch_data else None
    gemini_response = get_gemini_summary_rating(batch_json) if batch_json else None
    return render_template('index.html', gemini_response=gemini_response)

if __name__ == '__main__':
    # Run the Flask app in debug mode for development
    app.run(debug=True)