# ******************************PYTHON LIBRARIES******************************

# ******************************EXTERNAL LIBRARIES****************************
import spacy
from flask import (
                    flash, 
                    request, 
                    Blueprint,
                    render_template, 
                    )
# ******************************OWN LIBRARIES*********************************
from db import dbPostgres
from src.forms import PoemForm
from src.models import PoemModel
from src.functions import (
                            countPoemTags,
                            getPoemEntities,
                            getPoemSentiment,
                            createPoemRender,
                            getPoemSentences,
                            getPoemMainWords,
                            getPoemTagsByWord,
                            getPoemNounChunks,
                            getPoemKeywordMatches,
                            createPoemsCollection,
                            )
# ****************************************************************************
blp = Blueprint("poems", __name__, template_folder="../templates", static_folder="../static")

@blp.route("/home", methods=["GET", "POST"])
def home():
    form = PoemForm()
    
    if form.validate_on_submit():
        data = {key:value for key, value in form.data.items() if key not in ["submit", "csrf_token"]}
        poem = PoemModel(**data)
        dbPostgres.session.add(poem)
        dbPostgres.session.commit()
        
        counter = PoemModel.query.count()
        
        form = PoemForm(formdata=None)
        
        flash(f"Poem successfully added! | Total poems: {counter}")
        
        return render_template("home.html", form=form)
    
    return render_template("home.html", form=form)

@blp.route("/poemsList")
def poemsList():

    # Creates a list of dictionaries with each poem data
    poemsCollection = createPoemsCollection(dbModel=PoemModel)
    
    # Spacy instance
    Spacy = spacy.load("es_core_news_sm")
    
    # Spacy spanish model's stop words
    stopWords = [ word for word in Spacy.Defaults.stop_words ]
    
    try:
        poemID = request.args.get("poemID")
        selectedPoem = PoemModel.query.get_or_404(poemID)
        poemText = selectedPoem.poem        

        # New Spacy's document creation
        poem = Spacy(poemText)

        # Get document's entities
        poemEntities = getPoemEntities(poem=poem)
        
        # Display document's graphic render
        poemRender = createPoemRender(poem=poem)
        
        # Document tags by word
        poemTags = getPoemTagsByWord(poem=poem)

        # Count document's tags
        poemTagsCounter = countPoemTags(poem=poem)
        
        # Get document's sentencess
        poemSentences = getPoemSentences(poem=poem)
        
        # Get document's noun-chunks
        poemNounChunks = getPoemNounChunks(poem=poem)
        
        # Get poem keyword matches
        poemKeywordMatches = getPoemKeywordMatches(
                                                    poem=poem, 
                                                    spacyVocab=Spacy.vocab, 
                                                    poemKeywords=selectedPoem.keywords.lower().split(", ")
                                                    )
        
        # Get poem sentiment calification
        poemSentiment = getPoemSentiment(poem=poem)
        
        # Get poems topics & top 3 main words
        poemMainWords = getPoemMainWords(poem=poemText, stopwords=stopWords)

        return render_template("analizer.html",
                                poemText=poemText,
                                poemTags=poemTags,
                                poemRender=poemRender,
                                poemEntities=poemEntities,
                                poemMainWords=poemMainWords,
                                poemSentiment=poemSentiment,
                                poemSentences=poemSentences,
                                poemNounChunks=poemNounChunks,
                                poemTagsCounter=poemTagsCounter,
                                poemsCollection=poemsCollection,
                                poemKeywordMatches=poemKeywordMatches, 
                                )

    except:
        return render_template("analizer.html", poemsCollection=poemsCollection)