# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
import spacy
from spacy import displacy
from dataclasses import asdict
from spacy.matcher import Matcher
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
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
    poemRender = displacy.render(poem, jupyter=False)
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

def getPoemSentences(poem) -> list:
    '''This function creates an array
    with all the detected sentencess
    of a poem.'''
    poemSentences = [sentence for sentence in poem.sents]
    return poemSentences

def getPoemNounChunks(poem) -> list:
    '''This function creates a list
    with all the nouns founded into
    a poem'''
    poemNounChunks = [nounChunk.text for nounChunk in poem.noun_chunks]
    return poemNounChunks

def getPoemKeywordMatches(poem, spacyVocab, poemKeywords) -> dict:
    '''This function crates a poem's keywords 
    dictionary with a list of the position
    where that keyword is founded into the
    poem'''
    # 'Matcher' instance with the needed vocabulary
    poemMatcher = Matcher(spacyVocab)
    
    # Pattern creation
    pattern = [{"LOWER": {"IN": poemKeywords}}]
    
    # Agreggation of the pattern to the 'Matcher' object
    poemMatcher.add("POEM_KEYWORDS", [pattern])
    
    # Look for matches
    matches = poemMatcher(poem)
    
    # Creation of a word's matches list
    wordsList = [(poem[start].text, start) for wordID, start, end in matches]
    
    # Keyword matches dictionary
    matchesDictionary = {}
    
    # Dictionary construction process
    for word, position in wordsList:
        matchesDictionary.setdefault(word.lower(), []).append(position)
    
    # Final dictionary
    return matchesDictionary

def getPoemSentiment(poem) -> str:
    '''This function determines a 
    poem general sentiment in 
    positive, negative or neutral'''
    sentimentAnalyzer = SentimentIntensityAnalyzer()
    poemSentiment = sentimentAnalyzer.polarity_scores(poem.text)
    if poemSentiment["compound"] > 0.05:
        sentiment = "positive"
    elif poemSentiment["compound"] < -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return sentiment

def getPoemMainWords(poem, stopwords) -> list:
    vectorizer = CountVectorizer(max_df=1.0, min_df=0.0, stop_words=stopwords)
    data = vectorizer.fit_transform([poem])
    model = LatentDirichletAllocation(n_components=2, random_state=90)
    model.fit(data)
    components = model.components_
    for index, tema in enumerate(components):
        wordsSorted = tema.argsort()[-3:]
        poemTopWords = [vectorizer.get_feature_names_out()[word] for word in wordsSorted]
    return poemTopWords

