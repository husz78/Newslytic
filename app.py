import os
from flask import Flask
from newslytic.routes.main import main_bp

def create_app():
    app = Flask(__name__)

    # Register the blueprints
    app.register_blueprint(main_bp)

    # Load the default configuration
    app.config.from_pyfile('config.py', silent=True)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
