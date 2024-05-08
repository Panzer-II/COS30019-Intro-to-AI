import sys
from FileReader import FileReader
from KnowledgeBase import KnowledgeBase
from Sentence import Sentence
from TruthTable import TruthTable
from HornForm import HornForm
from ForwardChaining import ForwardChaining
from BackwardChaining import BackwardChaining

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Enter command in following format: iengine method filename")
        print("Methods: TT, FC and BC")
        exit(0)

    # get tell and ask from file of given name
    try:
        tell, ask = FileReader.read(sys.argv[2])
    except:
        print("File not found.")
        sys.exit(0)

    if len(tell) == 0:
        print("No tell found.")
        sys.exit(0)
    if not ask:
        print("No ask found.")
        sys.exit(0)

    method = sys.argv[1]
    # set up knowledge base and method based on chosen method
    # print solution using method and query (ask)
    if method == 'TT':
        kb = KnowledgeBase(tell, 'GS') # setup knowledge base with general sentences
        tt = TruthTable(kb)
        print(tt.solve(ask))
    elif method == 'FC':
        kb = KnowledgeBase(tell, 'HF') # setup knowledge base with horn form
        fc = ForwardChaining(kb)
        print(fc.solve(ask))
    elif method == 'BC':
        kb = KnowledgeBase(tell, 'HF')
        bc = BackwardChaining(kb)
        print(bc.solve(ask))
    else:
        print("Unknown method entered.")
    
