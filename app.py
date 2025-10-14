"""
Main entry point 
"""
from flask import Flask
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from routes.trips_routes import trips_bp
from routes.insights_routes import insights_bp

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(trips_bp, url_prefix='/api/trips')
    app.register_blueprint(insights_bp, url_prefix='/api/insights')
    
    # Simple home route
    @app.route('/')
    def home():
        return {
            "message": "Welcome to NYC Mobility API",
            "endpoints": {
                "trips": "/api/trips",
                "insights": "/api/insights"
            }
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
