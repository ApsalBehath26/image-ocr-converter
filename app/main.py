"""Application entry point"""

import os
from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Get configuration from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    # Run application
    app.run(host=host, port=port, debug=debug, threaded=True)
