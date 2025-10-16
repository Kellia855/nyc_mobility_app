"""
Main entry point 
"""
from flask import Flask
from flask_cors import CORS
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from routes.trips_routes import trips_bp
from routes.insights_routes import insights_bp

def create_app():
    """Create and configure the Flask application"""
    # Set template and static folders to the frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    app = Flask(__name__, 
                template_folder=frontend_dir,
                static_folder=os.path.join(frontend_dir, 'static'))
    
    # Enable CORS for all routes
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(trips_bp, url_prefix='/api/trips')
    app.register_blueprint(insights_bp, url_prefix='/api/insights')
    
    # Serve the frontend
    from flask import render_template
    
    @app.route('/')
    def home():
        return render_template('index.html')
    
    # API info route
    @app.route('/api')
    def api_info():
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

