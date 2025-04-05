from flask import Flask, render_template, json
from database.mongo_db import find_batch_by_ID, MongoJSONEncoder, update_batch
from service.gemini import get_gemini_summary_rating
import json
import markdown
from werkzeug.middleware.proxy_fix import ProxyFix

# Create the Flask application instance
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)  # For handling reverse proxies like Heroku

@app.route('/')
@app.route('/<string:batch_id>')
def home(batch_id=None):
    batch_data = find_batch_by_ID(batch_id)
    batch_json = json.dumps(batch_data, cls=MongoJSONEncoder) if batch_data else None

    # Check if the batch already contains the required fields
    if batch_data and all(key in batch_data for key in ['story', 'score', 'analysis']):
        gemini_response = {
            "story": batch_data['story'],
            "score": batch_data['score'],
            "analysis": batch_data['analysis']
        }
    else:
        # Generate the Gemini response if fields are missing
        gemini_response = get_gemini_summary_rating(batch_json) if batch_json else None

        if gemini_response:
            # Update the batch with the new Gemini response
            update_result = update_batch(batch_id, gemini_response)
            app.logger.debug(update_result)

    analysis_html = markdown.markdown(gemini_response['analysis']) if gemini_response and gemini_response.get('analysis') else ""

    return render_template('index.html', gemini_response=gemini_response, analysis_html=analysis_html)

if __name__ == '__main__':
    app.run(debug=True)
