from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register blueprints or routes
    from .api.mongo_api import mongo_api_bp
    from .api.gemini_api import gemini_api_bp

    app.register_blueprint(mongo_api_bp, url_prefix='/api/mongo')
    app.register_blueprint(gemini_api_bp, url_prefix='/api/gemini')

    return app 