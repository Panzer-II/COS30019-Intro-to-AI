from KnowledgeBase import KnowledgeBase
from Sentence import Sentence
from HornForm import HornForm

class BackwardChaining:
    """Implementation of Backward Chaining Algorithm"""
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def bc_entails(self, query):
        agenda = [query]  # Initialize agenda with the query
        inferred = {}  # Dictionary to keep track of inferred symbols
        chain = []  # List to keep track of the result of backward chaining

        def is_fact(symbol):
            """Check if a symbol is a known fact (without premises) in the knowledge base."""
            for sentence in self.kb.sentences:
                if isinstance(sentence, HornForm) and len(sentence.conjuncts) == 0 and sentence.head == symbol:
                    return True
            return False

        def infer(symbol):
            """Recursively infer a symbol using backward chaining."""
            if symbol in inferred:
                return inferred[symbol]
            if is_fact(symbol):
                inferred[symbol] = True
                chain.append(symbol)
                return True

            inferred[symbol] = False  # Assume it cannot be inferred unless proven otherwise
            for sentence in self.kb.sentences:
                if isinstance(sentence, HornForm) and sentence.head == symbol:
                    premises = sentence.conjuncts
                    if all(infer(premise) for premise in premises):
                        inferred[symbol] = True
                        chain.append(symbol)
                        return True

            return False

        result = infer(query)
        return result, chain

    def solve(self, query):
        solution_found, chain = self.bc_entails(query)
        return "YES: " + ', '.join(chain) if solution_found else "NO"
