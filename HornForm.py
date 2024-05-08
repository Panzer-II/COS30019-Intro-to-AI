# Horn-form sentence class
import re #for regular expressions

class HornForm:
    """Implementation of Horn Form Clause sentence structure for Chaining Alogorithms.
       Splits left and right side of Horn Clause into conjuncts and head for use in
       algorithms.
    """
    def __init__(self, sentence):
        ## fields ##
        self.clause = []        # whole horn form clause passed
        self.symbols = []       # symbols within sentence
        self.head = ""          # symbol right side of implication
        self.conjuncts = []     # symbols in conjunction on left side of implication

        # separate connectives and symbols
        self.clause = re.split("(=>|&|\(|\)|~|\|\||<=>)",sentence)
        # remove empty string
        while("" in self.clause) : 
            self.clause.remove("") 
        # remove brackets
        while("(" in self.clause) : 
            self.clause.remove("(") 
        while(")" in self.clause) : 
            self.clause.remove(")") 
        # check horn form connectives
        if ('~' or '||' or '<=>') in self.clause:
            raise Exception("Sentence is not in horn form ", self.clause)
        
        # if clause only one symbol get head symbol
        if len(self.clause) == 1:
            self.head = self.clause[0]
        else:
            index = self.clause.index('=>')
            right = self.clause[index+1:]     # symbols right of implication
            if (len(right) > 1):
                raise Exception("Error horn form format", self.clause)
            self.head = right[0]              # get head symbol
            left = self.clause[:index]        # symbols left of implication
            if (left[0] or left[-1]) == '&':  # if left side start or ends with conjunction
                raise Exception("Error horn form format", self.clause)
            for i in range(len(left)-1):      # loop checks for conjunctions next to each other   
                if left[i] == left[i+1]:
                    raise Exception("Error horn form format", self.clause)
            for ele in left:               # get conjuncts
                if ele != '&':         # if not conjunction, then is a symbol
                    self.conjuncts.append(ele)   
            self.symbols = self.conjuncts.copy()
        if self.head not in self.symbols:
            self.symbols.append(self.head)


