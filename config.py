import os
import logging

# Configure logging for deployment debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    """Base configuration for the application."""
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev_key')
    
    # Mail settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('SMTP_EMAIL', os.environ.get('MAIL_USERNAME', 'your-email@gmail.com'))
    MAIL_PASSWORD = os.environ.get('SMTP_PASSWORD', os.environ.get('MAIL_PASSWORD', 'your-password'))
    MAIL_DEFAULT_SENDER = os.environ.get('SMTP_EMAIL', os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@antidote.com'))
    
    # File Upload Configuration
    # Set maximum content length to 50MB for face analysis images (50 * 1024 * 1024 bytes)
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    
    # SQLAlchemy database configuration - Using Supabase with deployment error handling
    @staticmethod
    def get_database_uri():
        """Get database URI with proper error handling for deployment."""
        database_url = os.environ.get('DATABASE_URL')
        
        # Debug logging for deployment troubleshooting
        if database_url:
            logger.info("✅ DATABASE_URL found in environment")
            # Log partial URL for debugging (hide password)
            masked_url = database_url.replace(database_url.split('@')[0].split(':')[-1], '***') if '@' in database_url else database_url[:50] + '...'
            logger.info(f"Database URL (masked): {masked_url}")
        else:
            logger.error("❌ DATABASE_URL not found in environment variables")
            # List available environment variables for debugging
            env_vars = [key for key in os.environ.keys() if 'DATABASE' in key.upper() or 'DB' in key.upper()]
            logger.error(f"Available database-related env vars: {env_vars}")
            
            # Fallback - try alternative environment variable names that DigitalOcean might use
            alternative_vars = ['SQLALCHEMY_DATABASE_URI', 'DATABASE_URI', 'DB_URL', 'POSTGRES_URL']
            for var in alternative_vars:
                alt_url = os.environ.get(var)
                if alt_url:
                    logger.info(f"✅ Found alternative database URL in {var}")
                    return alt_url
                    
            # If no database URL found, provide a helpful error message
            raise ValueError(
                "Database configuration error: DATABASE_URL environment variable not found. "
                "Please ensure DATABASE_URL is set in your DigitalOcean environment variables. "
                f"Current environment has these database-related variables: {env_vars}"
            )
        
        return database_url
    
    # Set the database URI using the robust method
    SQLALCHEMY_DATABASE_URI = None  # Will be set after class definition
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Optimized configuration for Supabase connection pooling
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 600,          # 10 minutes - longer for Supabase pooler
        'pool_pre_ping': True,        # Test connections before use
        'pool_timeout': 60,           # 60 seconds - more time for Supabase pooler
        'pool_size': 10,              # Larger pool for concurrent requests
        'max_overflow': 15,           # Higher overflow for traffic spikes
        'connect_args': {
            'sslmode': 'require',     # Require SSL for Supabase connections
            'sslcert': None,          # Disable client certificates
            'sslkey': None,           # Disable client keys
            'sslrootcert': None,      # Use system CA certificates
            'connect_timeout': 30,    # 30 seconds for initial connection
            'application_name': 'antidote_flask_app',  # Connection tracking
            'keepalives_idle': 600,   # Keep connections alive
            'keepalives_interval': 30,
            'keepalives_count': 3
        }
    }
    
    # Debug configuration
    DEBUG = True

# Set the database URI after class definition
Config.SQLALCHEMY_DATABASE_URI = Config.get_database_uri()
