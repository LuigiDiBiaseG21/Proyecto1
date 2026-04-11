import os
from app import create_app

application = create_app()

if __name__ == "__main__":
    # Use environment variables for production, defaults for development
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    
    application.run(host=host, port=port, debug=debug)