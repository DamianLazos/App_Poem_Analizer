# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired
# ******************************OWN LIBRARIES*********************************

# ****************************************************************************
class PoemForm(FlaskForm):
    keywords = StringField("Palabra(s) claves", validators=[InputRequired()])
    title = StringField("Titulo")
    poem = TextAreaField("Poema", validators=[InputRequired()])
    submit = SubmitField("submit")
    
