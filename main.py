from app import create_app
import os
import logging

# Configure logging for deployment
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create the Flask application
app = create_app()

# Ensure the app binds to any host for deployment compatibility
app.config['SERVER_NAME'] = None  # Allow any host for deployment

if __name__ == "__main__":
    # Run the Flask application with proper port handling for deployment
    # This ensures compatibility with both Replit (default 5000) and DigitalOcean (dynamic PORT)
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
