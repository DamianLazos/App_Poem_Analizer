# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask import (Flask)
from dotenv import load_dotenv
# ******************************OWN LIBRARIES*********************************
from config import AppConfiguration
from db import dbPostgres
from src.routes import blp as PoemsBlueprint
from src.models import PoemModel
# ****************************************************************************
load_dotenv()


def create_app():
    
    # App instance
    app = Flask(__name__)
    
    # App configuration settings
    app.config.from_object(AppConfiguration)
    dbPostgres.init_app(app)
    
    # SQL database context
    with app.app_context():
        dbPostgres.create_all()
        
    # Blueprints registration
    app.register_blueprint(PoemsBlueprint)

    return app