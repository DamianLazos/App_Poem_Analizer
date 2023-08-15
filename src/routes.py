# ******************************PYTHON LIBRARIES******************************
import json
from dataclasses import asdict
# ******************************EXTERNAL LIBRARIES****************************
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
from src.classes import PoemIndividual
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
    poems = PoemModel.query.all()
    poemsCollection = []
    for poem in poems:
        currentPoem = PoemIndividual(
                                        _id=poem.id, 
                                        poem=poem.poem,
                                        title=poem.title, 
                                        keywords=poem.keywords, 
                                    )
        poemsCollection.append(asdict(currentPoem))
        
    try:
        poemID = request.args.get("poemID")
        selectedPoem = PoemModel.query.get_or_404(poemID)
        poemText = selectedPoem.poem
        print("Se vino para el try")
        return render_template("analizer.html", poemsCollection=poemsCollection, poemText=poemText)

    except:
        print("Se vino para el except")
        return render_template("analizer.html", poemsCollection=poemsCollection)

# @blp.route("/readPoem")
# def readPoem():
#     poemID = request.args.get("poemID")
#     poem = PoemModel.query.get_or_404(poemID)
#     return redirect(url_for(".poemsList"))

@blp.route("/poemAnalizer")
def poemAnalizer():
    
    return "Hello world"