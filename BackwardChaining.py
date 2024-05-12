from KnowledgeBase import KnowledgeBase
from Sentence import Sentence
from HornForm import HornForm

class BackwardChaining:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def solve(self, query):
        processed = set()
        goal_stack = [(query, [query])]  # Include the initial query in the path
        successful_paths = []

        while goal_stack:
            goal, path = goal_stack.pop()
            print(f"Processing goal: {goal}, current path: {path}")

            # Only mark as processed if it fully contributes to a successful path
            found_applicable_rule = False
            for rule in self.kb.sentences:
                if isinstance(rule, HornForm) and rule.head == goal:
                    found_applicable_rule = True
                    new_path = path[:] + [goal] if goal not in path else path[:]
                    print(f"Applying rule: {rule.conjuncts} => {rule.head}, path: {new_path}")

                    if not rule.conjuncts:  # If no antecedents
                        if new_path not in successful_paths:
                            successful_paths.append(new_path)
                    else:
                        for antecedent in rule.conjuncts:
                            if antecedent not in processed:
                                goal_stack.append((antecedent, new_path))
                                print(f"Adding antecedent {antecedent} to stack with path: {new_path}")

            if not found_applicable_rule and goal not in path:
                successful_paths.append(path + [goal])

            # Delay marking as processed to explore all paths
            processed.add(goal)

        if successful_paths:
            successful_paths.sort(key=lambda x: len(x), reverse=True)  # Prefer longer paths
            longest_path = successful_paths[0]
            longest_path.reverse()
            result = "YES: " + ", ".join(longest_path)
            print(f"Successful path found: {result}")
            return result

        print("No successful paths found.")
        return "NO"




    #def is_fact(self, goal):
    #    """ Check if a goal is a fact based on having no antecedents """
    #    for sentence in self.kb.sentences:
    #        if isinstance(sentence, HornForm) and goal == sentence.head and not sentence.conjuncts:
    #            return True
    #        elif isinstance(sentence, Sentence) and goal in sentence.symbols and len(sentence.symbols) == 1:
    #            return True
    #    return False
