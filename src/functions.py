# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
import spacy
from spacy import displacy
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

def getPoemEntities(poem) -> dict:
    ''' This function creates a dictionary
    with every entity detected and the
    texts related to it.'''
    tuplesArray = []
    for entity in poem.ents:
        tuplesArray.append((entity.label_, entity.text))
    
    entities = {}
    for entity, text in tuplesArray:
        entities.setdefault(entity, []).append(text)
    return entities

def createPoemRender(poem) -> object:
    '''This method creates a displayed
    graphic render representation of 
    and specific SpaCy document.'''
    poemRender = displacy.render(
                                poem, 
                                jupyter=False, 
                                page=True, 
                                minify=True
                                )
    return poemRender

def getPoemTagsByWord(poem) -> list:
    '''This function gets all the tags
    of every token of a poem'''
    poemTags = []
    for word in poem:
        poemTags.append((word.text, word.tag_))
    return poemTags

def countPoemTags(poem) -> dict:
    '''This function counts the tags
    frecuency within a document.'''
    counter = poem.count_by(spacy.attrs.POS)
    poemTagsCounter = [(poem.vocab[index].text, value) for index, value in counter.items()]
    return poemTagsCounter





