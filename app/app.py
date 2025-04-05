import json
import markdown
from flask import Flask, render_template, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix
from bson.errors import InvalidId

from database.mongo_db import find_batch_by_ID, MongoJSONEncoder, update_batch
from service.gemini import get_gemini_summary_rating

# Create the Flask application instance
app = Flask(__name__)
# Handle reverse proxies like Heroku
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

@app.route('/favicon.ico')
def favicon():
    """
    Serve the favicon.ico file to prevent it from being treated as a batch_id parameter.
    """
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
@app.route('/<string:batch_id>')
def home(batch_id=None):
    """
    Renders the home page with batch information and analysis.
    
    Args:
        batch_id (str, optional): The ID of the batch to retrieve. Defaults to None.
        
    Returns:
        str: Rendered HTML template with batch data and analysis.
    """
    # Get batch data from database
    batch_json_dict = None
    try:
        if batch_id:
            batch_json_dict = find_batch_by_ID(batch_id)
    except InvalidId:
        app.logger.warning(f"Invalid batch ID format: {batch_id}")
    
    # Set default values
    gemini_response = None
    analysis_html = ""
    produce = "Produce"
    
    if batch_json_dict:
        # Extract produce from batch data if available
        if 'produce' in batch_json_dict:
            produce = batch_json_dict['produce']
            
        # Convert batch data to JSON string for API calls if needed
        batch_json_str = json.dumps(batch_json_dict, cls=MongoJSONEncoder)
        
        # Check if batch already contains analysis data
        if all(key in batch_json_dict for key in ['story', 'score', 'analysis']):
            # Use existing analysis data
            gemini_response = {
                "story": batch_json_dict['story'],
                "score": batch_json_dict['score'],
                "analysis": batch_json_dict['analysis']
            }
        else:
            # Generate new analysis using Gemini API
            try:
                gemini_response = get_gemini_summary_rating(batch_json_str)
                
                # Update database with new analysis data
                if gemini_response:
                    update_result = update_batch(batch_id, gemini_response)
                    app.logger.debug(f"Database update result: {update_result}")
            except Exception as e:
                app.logger.error(f"Error generating Gemini response: {str(e)}")
    
    # Convert markdown analysis to HTML if available
    if gemini_response and gemini_response.get('analysis'):
        analysis_html = markdown.markdown(gemini_response['analysis'])

    return render_template('index.html', gemini_response=gemini_response, 
                          analysis_html=analysis_html, produce=produce)

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=True for development; set to False in production
