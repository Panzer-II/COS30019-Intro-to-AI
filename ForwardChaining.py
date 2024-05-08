from KnowledgeBase import KnowledgeBase
from Sentence import Sentence

class ForwardChaining:
    """Implementation of Forward Chaining Algorithm"""
    def __init__(self, knowledge_base):
        self.kb= knowledge_base

    # forward chaining algorithm to check if kb entails query
    # algorithm starts from symbols known to be true and makes way through premises of clauses
    # until the query is reached
    