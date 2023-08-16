# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
from dataclasses import asdict
# ******************************OWN LIBRARIES*********************************
from src.classes import PoemIndividual
# ****************************************************************************
def createPoemsCollection(dbModel):
    '''This function creates a list of
    dictionaries with each poem data
    from a SQL model.'''
    poems = dbModel.query.all()
    poemsCollection = []
    for poem in poems:
        currentPoem = PoemIndividual(
                                        _id=poem.id, 
                                        poem=poem.poem,
                                        title=poem.title, 
                                        keywords=poem.keywords, 
                                    )
        poemsCollection.append(asdict(currentPoem))
    return poemsCollection