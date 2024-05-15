from KnowledgeBase import KnowledgeBase
from itertools import product

class TruthTable:
    """Implementation of Truth Table Entailment Method."""
    def __init__(self, knowledge_base, query):
        self.kb = knowledge_base
        self.query = query
        self.symbols = self.kb.symbols  # Assuming KnowledgeBase has a property `symbols` that lists all unique symbols

    def generate_truth_assignments(self):
        """Generate all possible truth assignments for the symbols."""
        return list(product([False, True], repeat=len(self.symbols)))

    def evaluate_kb(self, model):
        """Evaluate the truth value of all sentences in the KB for a given model."""
        # Assume each sentence in KB can evaluate itself given a model
        return all(sentence.solve(model) for sentence in self.kb.sentences)

    def check_entailment(self):
        """Check if the query is entailed by the knowledge base using truth table method."""
        truth_assignments = self.generate_truth_assignments()
        models_count = 0
        entailed_in_all_models = True

        for assignment in truth_assignments:
            model = dict(zip(self.symbols, assignment))
            if self.evaluate_kb(model):
                models_count += 1
                if not model.get(self.query, False):
                    entailed_in_all_models = False
                    break

        return entailed_in_all_models, models_count

    def solve(self):
        """Run the truth table check and return the appropriate result format."""
        entailed, models_count = self.check_entailment()
        if entailed:
            return f"YES: {models_count}"
        else:
            return "NO"
