from consts import *
from utils import *
from scope_structure import ScopeStructure


class Node():

    name = ""
    parent_node = None
    children = []
    leaf_node = False
    scope_structure = None

    # params for semantic analysis
    tip = None
    l_izraz = None


    def __init__(self, name: str, parent_node, scope_structure: ScopeStructure):
        self.name = name
        self.parent_node = parent_node
        self.scope_structure = scope_structure
        self.children = list()
        # node
        if self.name.startswith("<"):
            self.leaf_node = False
        # leaf
        else:
            self.name = name.split(' ')[0]
            self.line = name.split(' ')[1]
            self.lex = name.split(' ')[2]
            self.leaf_node = True
        
        self.tip = None
        self.l_izraz = None
        return
    

    def add_child(self, child_node):
        self.children.append(child_node)
        return
    

    def __str__(self):
        return self.name
    

    def __repr__(self):
        return self.name


    def print(self, depth: int):
        print(" " * depth + self.name)
        for child in self.children:
            child.print(depth + 1)
        return
    

    # very important function!!
    # call it if an error is spotted
    # terminate further analysis
    def error(self):
        output_string = self.name + " ::="
        for child in self.children:
            output_string += (" " + child.name)
            if (child.leaf_node):
                output_string += (f"({child.line},{child.lex})")
        output_string += "\n"
        return output_string
    

    def provjeri(self):
        output = ""
        if (self.name == PRIMARNI_IZRAZ):
            output = self.primarni_izraz()
        elif (self.name == POSTFIKSNI_IZRAZ):
            output = self.postfiksni_izraz()
        return output
    

    # <primarni_izraz>
    def primarni_izraz(self):
        if (self.children[0].name == IDN):
            if not self.scope_structure.idn_name_in_scope(self.children[0].lex):
                return self.error()
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz

        elif (self.children[0].name == BROJ):
            # value is in int range
            if not (-2147483648 <= int(self.children[0].lex) <= 2147483647):
                return self.error()
            self.tip = INT
            self.l_izraz = 0

        elif (self.children[0].name == ZNAK):
            if not check_char(self.children[0].lex):
                return self.error()
            self.tip = CHAR
            self.l_izraz = 0

        elif (self.children[0].name == NIZ_ZNAKOVA):
            if not check_string(self.children[0].lex):
                return self.error()
            self.tip = NIZ_CONST_CHAR
            self.l_izraz = 0

        elif (self.children[0].name == L_ZAGRADA and
              self.children[1].name == IZRAZ and
              self.children[2].name == D_ZAGRADA):
            error = self.children[1].provjeri()
            if error:
                return error
            self.tip = self.children[1].tip
            self.l_izraz = self.children[1].l_izraz
            
        return ""
    

    # <postfiksni_izraz>
    def postfiksni_izraz(self):
        ...
