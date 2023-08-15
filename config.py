# ******************************PYTHON LIBRARIES******************************
import os
# ******************************EXTERNAL LIBRARIES****************************

# ******************************OWN LIBRARIES*********************************

# ****************************************************************************
class AppConfiguration:
    '''This class contains all
    the app's general configuration
    settings and parameters.'''
    
    SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://postgres:3132@localhost/app_poemAnalizer"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY=os.getenv("SECRET_KEY")