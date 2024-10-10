from flask_smorest import Api
from models import tables
from flask import Flask
import os

from db import db, migrate

from resources.student import blp as StudentBlueprint
from resources.teacher import blp as TeacherBlueprint
from resources.supervisor import blp as SupervisorBlueprint
from resources.coordinator import blp as CoordinatorBlueprint

import os

def create_app():
    """
    Create and configure the Flask application.

    Returns:
        app (Flask): The configured Flask application.
    """
    app = Flask(__name__)

    # Configuration settings for the Flask application
    app.config["API_TITLE"] = "Imperial College API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/documentation"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.path.dirname(__file__), "db", "imperialcollege_db.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database and migration objects with the Flask app
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize the API object with the Flask app
    api = Api(app)

    # Create all database tables within the application context
    with app.app_context():
        db.create_all()

    # List of blueprints to register with the API
    blueprints = [StudentBlueprint, 
                  TeacherBlueprint, 
                  SupervisorBlueprint,
                  CoordinatorBlueprint] 

    # Register each blueprint with the API
    for blueprint in blueprints:
        api.register_blueprint(blueprint)

    return app
