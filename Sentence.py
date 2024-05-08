import re   # for regular expressions
import sys

class Sentence:
    """Implementation of General Sentence Structure for a General Knowledge Base.
       Formats passed propositional logic in text to a structure that can be 
       solved using models.
    """

    def __init__(self, sentence):
        ## fields ##
        self.symbols = []   # symbols within the sentence
        self.root = []      # root atomic sentence which child atomic sentences branch from
        self.atomic = {}    # dictionary of atomic sentences within sentence, keys are used to link atomic sentences

        # separate connectives and symbols
        original = re.split("(=>|&|\(|\)|~|\|\||<=>)",sentence)
        # remove empty strings from sentence
        while "" in original: 
            original.remove("") 
        self.original = original.copy()
        # use regular expressions to extract symbols from sentence
        symbols = re.split("=>|&|\(|\)|~|\|\||<=>",sentence)
        while "" in symbols: # remove any empty symbols
            symbols.remove("") 
        self.symbols = list(set(symbols))  # remove duplicate symbols
        # extract atomic sentences from original sentence
        self.root = self.__parse(original) # final atomic sentence is the root sentence

    # used to recursively format the sentence into smaller atomic sentences
    def __parse(self, sentence):
        # parse atomic sentences within brackets first
        while '(' in sentence:
            #index of left bracket in sentence
            left_index = sentence.index('(')
            # used for counting number of left and right brackets
            left_count = 1
            right_count = 0
           
            #search sentence for index of matching right bracket
            right_index = 0
            for i in range(left_index+1, len(sentence)):
                if sentence[i] == '(':
                    left_count+=1
                elif sentence[i] == ')':
                    right_count+=1
                # when counts match, the matching right bracket is found
                if left_count == right_count:
                    right_index = i
                    break
            if (right_index == 0): # if the right brack is not found
                raise Exception("Incorrect brackets format in sentence: ", sentence)
            # get section of sentence contained inside brackets
            section = sentence[left_index+1:right_index]
            # recursively call __parse till no brackets left
            section = self.__parse(section)
            # replace section of sentence with name of atomic sentence
            if len(section) == 1:
                sentence[left_index] = section[0]
                del sentence[left_index+1:right_index+1]
            else:
                raise Exception("Incorrect senction format: ", section)

        ## create atomic sentences in order of precedence ##
        # negation
        while '~' in sentence:
            index = sentence.index('~')
            sentence = self.__add_atom(index, sentence, '~')
        # conjunction and disjunction, left most atomic sentence is chosen first
        while ('&' or '||') in sentence:
            if '&' in sentence:
                index = sentence.index('&')
            if '||' in sentence:
                if sentence.index('||') < index:
                    index = sentence.index('||')
            sentence = self.__add_atom(index, sentence, '&||')
        # implication
        while ('=>') in sentence:
            index = sentence.index('=>')
            sentence = self.__add_atom(index, sentence, '=>')
        # biconditional
        while ('<=>') in sentence:
            index = sentence.index('<=>')
            sentence = self.__add_atom(index, sentence, '<=>')

        return sentence

    # finds atomic sentence(atom) at an index and replaces with a key.
    # key, atom pair is added to atomic dictionary,
    # where the key is of the format atom[n]
    # e.g. {'atom1' : ['a', '&', 'b']}
    def __add_atom(self, index, sentence, connective):
        # negation is different as only has 2 elements
        # e.g. ~ a
        if connective == '~':
            atom = [sentence[index],
                    sentence[index+1]]
            # create key from atomic sentence
            atom_key = "atom"+str(len(self.atomic)+1)
            # add atomic sentence to dictionary
            self.atomic.update({atom_key:atom})
            # add reference to atomic sentence in main sentence
            # and delete remaining symbols
            sentence[index] = atom_key
            del sentence[index+1]
        else:
            # other atomic sentences of other logic operator have 3 elements
            # e.g. a & b
            atom = [sentence[index-1],
                    sentence[index],
                    sentence[index+1]]
            atom_key = "atom"+str(len(self.atomic)+1)
            self.atomic.update({atom_key:atom})
            sentence[index-1] = atom_key
            del sentence[index:index+2]
        # sentence with atom replaced with key is returned
        return sentence

    # solves the sentence using the passed in model
    def solve(self, model):
        bool_pairs = {}     # symbol and boolean pairs
        # check if model has truth value for all symbols in sentence
        for symbol in self.symbols:
            if symbol in model:
                # add symbol and its boolean value to dictionary (bool_pairs)
                bool_pairs.update({symbol:model[symbol]})
            else:
                raise Exception("No boolean for all symbols.")

        # solves each atomic sentence and updates dictionary with its key and resulting boolean
        for key in self.atomic:
            if len(self.atomic[key]) == 2:
                # solve negation
                right = bool_pairs[self.atomic[key][1]] # get truth value of symbol right of negation
                bool_pairs.update({key: not right})     # update dictionary with atom key and result of negation
            elif len(self.atomic[key]) == 3:
                left = bool_pairs[self.atomic[key][0]]  # get truth value left of logic operator
                right = bool_pairs[self.atomic[key][2]] # get truth value right of logic operator
                # solve conjunction
                if self.atomic[key][1] == '&':
                    bool_pairs.update({key: left and right })
                # solve disjunction
                elif self.atomic[key][1] == '||':
                    bool_pairs.update({key: left or right })
                # solve implication
                elif self.atomic[key][1] == '=>':
                    bool_pairs.update({key: not left or right})
                # solve biconditional
                elif self.atomic[key][1] == '<=>':
                    bool_pairs.update({key: left == right})
            else:
                raise Exception("Atomic sentence in incorrect format: ", self.atomic[key])

        # return root atomic sentence which contains solution
        return bool_pairs[self.root[0]]