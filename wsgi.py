"""
WSGI entry point for DigitalOcean App Platform
This ensures the app starts correctly regardless of configuration issues
"""
from main import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)