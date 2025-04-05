from flask import Flask, render_template, json
from database.mongo_db import find_batch_by_ID, MongoJSONEncoder
from service.gemini import get_gemini_summary_rating
from bson import ObjectId
import json
import markdown

# Create the Flask application instance
app = Flask(__name__)
app.logger.setLevel('DEBUG')

@app.route('/')
@app.route('/<string:batch_id>')
def home(batch_id=None):
    batch_data = find_batch_by_ID(batch_id)
    batch_json = json.dumps(batch_data, cls=MongoJSONEncoder) if batch_data else None
    gemini_response = get_gemini_summary_rating(batch_json) if batch_json else None

    analysis_html = markdown.markdown(gemini_response['analysis']) if gemini_response and gemini_response.get('analysis') else ""

    return render_template('index.html', gemini_response=gemini_response, analysis_html=analysis_html)

if __name__ == '__main__':
    app.run(debug=True)
