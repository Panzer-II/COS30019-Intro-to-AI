from Sentence import Sentence
from HornForm import HornForm


class KnowledgeBase:
    """Used to store propositional statements and symbols."""
    def __init__(self, sentences, type):
        ## fields ##
        self.sentences = []        # sentences contained in knowledge base
        self.symbols = []          # all found unique symbols in sentences
        if type == 'HF' or 'GS':   # check if type is valid
            self.type = type
        else:
            raise Exception("Unknown sentence type.")
        for sentence in sentences: # add sentences
            self.tell(sentence)

    # tell knowledge base a sentence
    def tell(self, sentence):
        # create sentence of chosen type 
        if self.type == 'HF':
            new = HornForm(sentence)
        elif self.type == 'GS':
            new = Sentence(sentence)    # general sentences            
        # add sentence to knowledge base
        self.sentences.append(new)
        # add new symbols to knowledge base if found
        for symbol in new.symbols:
            if symbol not in self.symbols:
                self.symbols.append(symbol)

