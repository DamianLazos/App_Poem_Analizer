# ******************************PYTHON LIBRARIES******************************
import json
from dataclasses import asdict
# ******************************EXTERNAL LIBRARIES****************************
import nltk
import spacy
import pandas
from spacy import displacy
from spacy.matcher import Matcher
from flask import (
                    flash, 
                    request, 
                    url_for,
                    redirect,
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
                            createPoemRender,
                            getPoemSentences,
                            getPoemTagsByWord,
                            getPoemNounChunks,
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

    try:
        poemID = request.args.get("poemID")
        selectedPoem = PoemModel.query.get_or_404(poemID)
        poemText = selectedPoem.poem
        
        # Individual poem process
        for poemIndividual in poemsCollection:
            poemText = poemIndividual["poem"]
            
            # New Spacy's document training
            poem = Spacy(poemText)
            
            # Get document's entities
            poemEntities = getPoemEntities(poem=poem)
            
            # Display document's graphic render
            poemRender = createPoemRender(poem=poem)
            
            # Document tags
            poemTags = getPoemTagsByWord(poem=poem)
        
            # Count document's tags
            poemTagsCounter = countPoemTags(poem=poem)
            
            # Get document's sentencess
            poemSentences = getPoemSentences(poem=poem)
            
            # Get document's noun-chunks
            poemNounChunks = getPoemNounChunks(poem=poem)
            
            # Get poem
            poemMatches = Matcher(Spacy.vocab)
            
        
        
        
        
        return render_template("analizer.html", 
                                poemText=poemText,
                                poemTags=poemTags,
                                poemRender=poemRender,
                                poemEntities=poemEntities,
                                poemSentences=poemSentences,
                                poemNounChunks=poemNounChunks,
                                poemTagsCounter=poemTagsCounter,
                                poemsCollection=poemsCollection, 
                                )

    except:
        return render_template("analizer.html", poemsCollection=poemsCollection)

@blp.route("/poemAnalizer")
def poemAnalizer():
    
    return "Hello world"

