from KnowledgeBase import KnowledgeBase
from Sentence import Sentence

class TruthTable:
    """Implementation of Truth Table Entailment Method"""
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.count = 0
