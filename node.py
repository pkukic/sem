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
    tipovi = []


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
        self.tipovi = []
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
    

    def right_side(self, *args):
        if len(args) != len(self.children):
            return False
        for i in range(len(self.children)):
            if self.children[i].name != args[i]:
                return False
        return True
    

    # very important function!!
    # call it if an error is spotted
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
        elif (self.name == POSTFIKS_IZRAZ):
            output = self.postfiks_izraz()
        elif (self.name == LISTA_ARGUMENATA):
            output = self.lista_argumenata()
        elif (self.name == UNARNI_IZRAZ):
            output = self.unarni_izraz()
        elif (self.name == CAST_IZRAZ):
            output = self.cast_izraz()
        elif (self.name == IME_TIPA):
            output = self.ime_tipa()
        elif (self.name == SPECIFIKATOR_TIPA):
            output = self.specifikator_tipa()
        elif (self.name == MULTIPLIKATIVNI_IZRAZ):
            output = self.multiplikativni_izraz()
        elif (self.name == ADITIVNI_IZRAZ):
            output = self.aditivni_izraz()
        elif (self.name == ODNOSNI_IZRAZ):
            output = self.odnosni_izraz()
        elif (self.name == JEDNAKOSNI_IZRAZ):
            output = self.jednakosni_izraz()
        elif (self.name == BIN_I_IZRAZ):
            output = self.bin_i_izraz()
        elif (self.name == BIN_XILI_IZRAZ):
            output = self.bin_xili_izraz()
        return output
    

    # <primarni_izraz>
    def primarni_izraz(self):
        if self.right_side(IDN):
            if not self.scope_structure.idn_name_in_scope(self.children[0].lex):
                return self.error()
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz

        elif self.right_side(BROJ):
            # value is in int range
            if not (-2147483648 <= int(self.children[0].lex) <= 2147483647):
                return self.error()
            self.tip = INT
            self.l_izraz = 0

        elif self.right_side(ZNAK):
            if not check_char(self.children[0].lex):
                return self.error()
            self.tip = CHAR
            self.l_izraz = 0

        elif self.right_side(NIZ_ZNAKOVA):
            if not check_string(self.children[0].lex):
                return self.error()
            self.tip = NIZ_CONST_CHAR
            self.l_izraz = 0

        elif self.right_side(L_UGL_ZAGRADA, IZRAZ, D_ZAGRADA):
            error = self.children[1].provjeri()
            if error:
                return error
            self.tip = self.children[1].tip
            self.l_izraz = self.children[1].l_izraz
        return ""
    

    # <postfiks_izraz>
    def postfiks_izraz(self):
        if self.right_side(PRIMARNI_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(POSTFIKS_IZRAZ, L_UGL_ZAGRADA, IZRAZ, D_UGL_ZAGRADA):
            # <postfiks_izraz>
            error = self.children[0].provjeri()
            if error:
                return error
            if not is_niz_x(self.children[0].tip):
                return self.error()
            # <izraz>
            error = self.children[2].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[2].tip, INT):
                return self.error()
            
            self.tip = remove_niz_from_niz_x(self.children[0].tip)
            if is_const(self.tip):
                self.l_izraz = 0
            else:
                self.l_izraz = 1

        elif self.right_side(POSTFIKS_IZRAZ, L_ZAGRADA, D_ZAGRADA):
            error = self.children[0].provjeri()
            if error:
                return error
            # TODO
            ...

        elif self.right_side(POSTFIKS_IZRAZ, L_ZAGRADA, LISTA_ARGUMENATA, D_ZAGRADA):
            error = self.children[0].provjeri()
            if error:
                return error
            error = self.children[2].provjeri()
            if error:
                return error
            # TODO
            ...

        elif self.right_side(POSTFIKS_IZRAZ, OP_INC):
            error = self.children[0].provjeri()
            if error:
                return error
            if self.children[0].l_izraz != 1:
                return self.error()
            if not implicit_cast(self.children[0].tip, INT):
                return self.error()
            self.tip = INT
            self.l_izraz = 0
            
        elif self.right_side(POSTFIKS_IZRAZ, OP_DEC):
            error = self.children[0].provjeri()
            if error:
                return error
            if self.children[0].l_izraz != 1:
                return self.error()
            if not implicit_cast(self.children[0].tip, INT):
                return self.error()
            self.tip = INT
            self.l_izraz = 0
        return ""
        
    
    # <lista_argumenata>
    def lista_argumenata(self):
        if self.right_side(IZRAZ_PRIDRUZIVANJA):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tipovi.append(self.children[0].tip)

        elif self.right_side(LISTA_ARGUMENATA, ZAREZ, IZRAZ_PRIDRUZIVANJA):
            error = self.children[0].provjeri()
            if error:
                return error
            error = self.children[2].provjeri()
            if error:
                return error
            self.tipovi = self.children[0].tipovi.copy()
            self.tipovi.append(self.children[2].tip)
        return ""
    

    # <unarni_izraz>
    def unarni_izraz(self):
        if self.right_side(POSTFIKS_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz

        elif self.right_side(OP_INC, UNARNI_IZRAZ):
            error = self.children[1].provjeri()
            if error:
                return error
            if self.children[1].l_izraz != 1:
                return self.error()
            if not implicit_cast(self.children[1].tip, INT):
                return self.error()
            self.tip = INT
            self.l_izraz = 0

        elif self.right_side(OP_DEC, UNARNI_IZRAZ):
            error = self.children[1].provjeri()
            if error:
                return error
            if self.children[1].l_izraz != 1:
                return self.error()
            if not implicit_cast(self.children[1].tip, INT):
                return self.error()
            self.tip = INT
            self.l_izraz = 0

        elif self.right_side(UNARNI_OPERATOR, CAST_IZRAZ):
            error = self.children[1].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[1].tip, INT):
                return self.error()
            self.tip = INT
            self.l_izraz = 0
        return ""
    

    # <unarni_operator>
    def unarni_operator(self):
        # nothing needs to be checked here
        ...
    

    # <cast_izraz>
    def cast_izraz(self):
        if self.right_side(UNARNI_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(L_ZAGRADA, IME_TIPA, D_ZAGRADA, CAST_IZRAZ):
            error = self.children[1].provjeri()
            if error:
                return error
            error = self.children[3].provjeri()
            if error:
                return error
            if not explicit_cast(self.children[3].tip, self.children[1].tip):
                return self.error()
        return ""
    

    # <ime_tipa>
    def ime_tipa(self):
        if self.right_side(SPECIFIKATOR_TIPA):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
        
        elif self.right_side(KR_CONST, SPECIFIKATOR_TIPA):
            error = self.children[1].provjeri()
            if error:
                return error
            if self.children[1].tip == VOID:
                return self.error()
            self.tip = make_const(self.children[1].tip)
        return ""
    

    # <specifikator_tipa>
    def specifikator_tipa(self):
        if self.right_side(KR_VOID):
            self.tip = VOID
        elif self.right_side(KR_CHAR):
            self.tip = CHAR
        elif self.right_side(KR_INT):
            self.tip = INT
        return ""
    

    # <multiplikativni_izraz>
    def multiplikativni_izraz(self):
        if self.right_side(CAST_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif (self.right_side(MULTIPLIKATIVNI_IZRAZ, OP_PUTA, CAST_IZRAZ) or
                self.right_side(MULTIPLIKATIVNI_IZRAZ, OP_DIJELI, CAST_IZRAZ) or
                self.right_side(MULTIPLIKATIVNI_IZRAZ, OP_MOD, CAST_IZRAZ)):
            error = self.children[0].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[0].tip, INT):
                return self.error()
            error = self.children[2].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[2].tip, INT):
                return self.error()
            self.tip = INT
            self.l_izraz = 0
        return ""
    

    # <aditivni_izraz>
    def aditivni_izraz(self):
        if self.right_side(MULTIPLIKATIVNI_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz

        elif self.right_side(ADITIVNI_IZRAZ, PLUS, MULTIPLIKATIVNI_IZRAZ) or self.right_side(ADITIVNI_IZRAZ, MINUS, MULTIPLIKATIVNI_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[0].tip, INT):
                return self.error()
            error = self.children[2].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[2].tip, INT):
                return self.error()
            self.tip = INT
            self.l_izraz = 0
        return ""
    

    # <odnosni_izraz>
    def odnosni_izraz(self):
        if self.right_side(ADITIVNI_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif (self.right_side(ODNOSNI_IZRAZ, OP_LT, ADITIVNI_IZRAZ) or
                self.right_side(ODNOSNI_IZRAZ, OP_GT, ADITIVNI_IZRAZ) or
                self.right_side(ODNOSNI_IZRAZ, OP_LTE, ADITIVNI_IZRAZ) or
                self.right_side(ODNOSNI_IZRAZ, OP_GTE, ADITIVNI_IZRAZ)):
            error = self.children[0].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[0].tip, INT):
                return self.error()
            error = self.children[2].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[2].tip, INT):
                return self.error()
            self.tip = INT
            self.l_izraz = 0
        return ""
    

    # <jednakosni_izraz>
    def jednakosni_izraz(self):
        if self.right_side(ODNOSNI_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif (self.right_side(JEDNAKOSNI_IZRAZ, OP_EQ, ODNOSNI_IZRAZ) or
                self.right_side(JEDNAKOSNI_IZRAZ, OP_NEQ, ODNOSNI_IZRAZ)):
            error = self.children[0].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[0].tip, INT):
                return self.error()
            error = self.children[2].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[2].tip, INT):
                return self.error()
            self.tip = INT
            self.l_izraz = 0
        return ""
    

    # <bin_i_izraz>
    def bin_i_izraz(self):
        if self.right_side(JEDNAKOSNI_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(BIN_I_IZRAZ, OP_BIN_I, JEDNAKOSNI_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[0].tip, INT):
                return self.error()
            error = self.children[2].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[2].tip, INT):
                return self.error()
            self.tip = INT
            self.l_izraz = 0
        return ""
    

    # <bin_xili_izraz>
    def bin_xili_izraz(self):
        if self.right_side(BIN_I_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(BIN_XILI_IZRAZ, OP_BIN_XILI, BIN_I_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[0].tip, INT):
                return self.error()
            error = self.children[2].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[2].tip, INT):
                return self.error()
            self.tip = INT
            self.l_izraz = 0
        return ""
