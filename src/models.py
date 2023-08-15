# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from flask import Flask
# ******************************OWN LIBRARIES*********************************
from db import dbPostgres
# ****************************************************************************
class PoemModel(dbPostgres.Model):
    __tablename__ = "poems"
    
    id = dbPostgres.Column(dbPostgres.Integer, primary_key=True, nullable=False)
    keywords = dbPostgres.Column(dbPostgres.String, unique=False, nullable=False)
    title = dbPostgres.Column(dbPostgres.String, unique=False, nullable=False)
    poem = dbPostgres.Column(dbPostgres.String, unique=True, nullable=False)
    

