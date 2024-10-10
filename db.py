from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the SQLAlchemy object
db = SQLAlchemy()

# Initialize the Migrate object
migrate = Migrate()
