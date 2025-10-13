"""
Backend package initialization
"""
from flask import Flask
from .routes.trips_routes import trips_bp
from .routes.insights_routes import insights_bp

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
