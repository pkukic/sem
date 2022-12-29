from generative_tree import GenerativeTree
from scope import Scope
from scope_structure import ScopeStructure
from FunctionType import FunctionType
from consts import *
import sys


# INPUT_FILE_PATH = "/home/filip/Work/FER/5_semestar/ppj/labosi/sem/lab3_teza/03_niz_znakova/test.in"
# INPUT_FILE_PATH = "/home/filip/Work/FER/5_semestar/ppj/labosi/sem/temp.txt"


def main():
    # with open(INPUT_FILE_PATH, 'r') as file:
        # input = [line.rstrip() for line in file.readlines()]
    input = [line.rstrip() for line in sys.stdin.readlines()]
    # make the generative tree from the input
    global_scope = Scope(None, GLOBAL)
    scope_structure = ScopeStructure(global_scope)
    gen_tree = GenerativeTree(input, scope_structure)
    error = gen_tree.root_node.provjeri()
    if error:
        print(error)
    defs = gen_tree.root_node.scope_structure.all_functions_declarations()
    decs = gen_tree.root_node.scope_structure.all_functions_declarations()
    required_main = ('main', FunctionType([VOID], INT))
    if required_main not in defs.items() or required_main not in decs.items():
        print('main')
    if defs != decs:
        print('funkcija')
            

if __name__ == '__main__':
    main()