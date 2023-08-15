# ******************************PYTHON LIBRARIES******************************
import os
# ******************************EXTERNAL LIBRARIES****************************
from pymongo import MongoClient
from flask_sqlalchemy import SQLAlchemy
# ******************************OWN LIBRARIES*********************************

# ****************************************************************************
class MongoDBConnection:
    '''This class creates an instance
    of a Mongo DB database connection
    to an specific collection.'''
    def __init__(self, dbName) -> None:
        self.client = MongoClient(os.getenv("MONGO_URL"))
        self.db = self.client[dbName]
        
    def createCollection(self, collectionName, schema=False):
        try:
            collection = self.db.create_collection(collectionName)
            return collection
        except:
            pass
        
        if schema:
            self.db.command("collMod", collectionName, validator=schema)
        
        return self.db[collectionName]

class PostgresDBConnection:
    '''This class creates an instance
    of a Postgres database.'''
    def __init__(self) -> None:
        self.db = SQLAlchemy()
