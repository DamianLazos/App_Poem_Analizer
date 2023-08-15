# ******************************PYTHON LIBRARIES******************************
from dataclasses import dataclass
# ******************************EXTERNAL LIBRARIES****************************

# ******************************OWN LIBRARIES*********************************

# ****************************************************************************
@dataclass
class PoemIndividual:
    _id: str
    keywords: str
    title: str
    poem: str