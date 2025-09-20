"""
WSGI entry point for DigitalOcean App Platform
This ensures the app starts correctly regardless of configuration issues
"""
import os
import sys
import logging

# Add current directory to Python path (important for buildpacks)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging for DigitalOcean
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - WSGI - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    logger.info("🚀 WSGI: Starting app import...")
    from main import app
    logger.info("✅ WSGI: App imported successfully")
    
    # Test route registration
    routes_count = len(list(app.url_map.iter_rules()))
    logger.info(f"✅ WSGI: {routes_count} routes registered")
    
    # Check if root route exists
    root_route_exists = any(rule.rule == '/' for rule in app.url_map.iter_rules())
    logger.info(f"✅ WSGI: Root route (/) exists: {root_route_exists}")
    
except Exception as e:
    logger.error(f"❌ WSGI: Failed to import app: {e}")
    import traceback
    logger.error(f"❌ WSGI: Traceback: {traceback.format_exc()}")
    raise

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🚀 WSGI: Running app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)