from KnowledgeBase import KnowledgeBase
from HornForm import HornForm
from Sentence import Sentence

class ForwardChaining:
    def __init__(self, KB):
        self.KB = KB

    def fc_entails(self, query):
        chain = []  # List to keep track of the result of forward chaining
        count = {}  # Dictionary to keep count of the number of unsatisfied premises of each clause
        inferred = {}  # Dictionary to keep track of inferred symbols
        agenda = []  # List of symbols known to be true
        clauses = {}  # Dictionary to keep track of which clauses a symbol appears in

        # Initialize agenda, count, inferred, and clauses
        for sentence in self.KB.sentences:
            if isinstance(sentence, HornForm):
                if not sentence.conjuncts:
                    agenda.append(sentence.head)
                else:
                    count[sentence] = len(sentence.conjuncts)
                    for conjunct in sentence.conjuncts:
                        if conjunct not in inferred:
                            inferred[conjunct] = False
                        if conjunct not in count:
                            count[conjunct] = 0
                        if conjunct not in clauses:
                            clauses[conjunct] = []
                        clauses[conjunct].append(sentence)
                # Ensure all symbols are in inferred dictionary
                if sentence.head not in inferred:
                    inferred[sentence.head] = False

        entailed_symbols = []

        print(f"Initial Agenda: {agenda}")
        print(f"Initial Count: {count}")
        print(f"Initial Inferred: {inferred}")
        print(f"Clauses: {clauses}")

        # Main loop of the forward chaining algorithm
        while agenda:
            p = agenda.pop(0)
            if p not in chain:
                chain.append(p)
            if p == query:
                inferred[p] = True
                continue
            if not inferred[p]:
                inferred[p] = True
                for clause in clauses.get(p, []):
                    count[clause] -= 1
                    if count[clause] == 0:
                        agenda.append(clause.head)
                        if clause.head not in inferred:
                            inferred[clause.head] = False

            print(f"Processed: {p}")
            print(f"Updated Agenda: {agenda}")
            print(f"Updated Count: {count}")
            print(f"Updated Inferred: {inferred}")

        return query in inferred and inferred[query], chain

    def solve(self, query):
        solution_found, chain = self.fc_entails(query)
        return "YES: " + ', '.join(chain) if solution_found else "NO"