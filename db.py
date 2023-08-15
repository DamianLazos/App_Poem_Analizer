# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************

# ******************************OWN LIBRARIES*********************************
from extensions import MongoDBConnection, PostgresDBConnection
# ****************************************************************************
dbMongo = MongoDBConnection('lyrics')
dbPostgres = PostgresDBConnection().db

