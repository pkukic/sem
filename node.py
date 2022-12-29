from consts import *
from utils import *
from scope_structure import ScopeStructure
from scope import Scope
from FunctionType import FunctionType


class Node():

    name = ""
    parent_node = None
    children = []
    leaf_node = False
    scope_structure = None

    # params for semantic analysis
    tip = None
    ntip = None
    l_izraz = None
    tipovi = []
    identifikatori = []
    vrijednost = None
    br_elem = None


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
        self.ntip = None
        self.l_izraz = None
        self.tipovi = []
        self.identifikatori = []
        self.vrijednost = None
        self.br_elem = None
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


    def in_loop(self):
        p = self.parent_node
        allowed_parents = [
            NAREDBA, 
            LISTA_NAREDBI, 
            SLOZENA_NAREDBA, 
            NAREDBA_GRANANJA
        ]
        if p.name != NAREDBA_PETLJE:
            if p.name not in allowed_parents:
                return False
            return p.in_loop()
        return True

    
    def nesting_function_type(self):
        p = self.parent_node
        allowed_parents = [
            NAREDBA,
            LISTA_NAREDBI,
            SLOZENA_NAREDBA,
            NAREDBA_GRANANJA,
            NAREDBA_PETLJE
        ]
        if p.name != DEFINICIJA_FUNKCIJE:
            if p.name not in allowed_parents:
                return None
            return p.nesting_function_type()
        return p.children[0].tip.return_type


    def goes_to_niz_znakova(self):
        if self.name == NIZ_ZNAKOVA:
            return (True, self.br_elem)
        if self.leaf_node:
            return (False, None)
        if len(self.children) > 1:
            return (False, None)
        return self.children[0].goes_to_niz_znakova()
            

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
    

    def provjeri(self, lista_identifikatora=None, lista_tipova=None, ntip=None):
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
        elif (self.name == BIN_ILI_IZRAZ):
            output = self.bin_ili_izrazi()
        elif (self.name == LOG_I_IZRAZ):
            output = self.log_i_izraz()
        elif (self.name == LOG_ILI_IZRAZ):
            output = self.log_ili_izraz()
        elif (self.name == IZRAZ_PRIDRUZIVANJA):
            output = self.izraz_pridruzivanja()
        elif (self.name == IZRAZ):
            output = self.izraz()

        elif (self.name == SLOZENA_NAREDBA):
            output = self.slozena_naredba(lista_identifikatora, lista_tipova)
        elif (self.name == LISTA_NAREDBI):
            output = self.lista_naredbi()
        elif (self.name == NAREDBA):
            output = self.naredba()
        elif (self.name == IZRAZ_NAREDBA):
            output = self.izraz_naredba()
        elif (self.name == NAREDBA_GRANANJA):
            output = self.naredba_grananja()
        elif (self.name == NAREDBA_PETLJE):
            output = self.naredba_petlje()
        elif (self.name == NAREDBA_SKOKA):
            output = self.naredba_skoka()

        elif (self.name == PRIJEVODNA_JEDINICA):
            output = self.prijevodna_jedinica()
        elif (self.name == VANJSKA_DEKLARACIJA):
            output = self.vanjska_deklaracija()
        elif (self.name == DEFINICIJA_FUNKCIJE):
            output = self.definicija_funkcije()
        elif (self.name == LISTA_PARAMETARA):
            output = self.lista_parametara()
        elif (self.name == DEKLARACIJA_PARAMETRA):
            output = self.deklaracija_parametra()
        elif (self.name == LISTA_DEKLARACIJA):
            output = self.lista_deklaracija()

        elif (self.name == DEKLARACIJA):
            output = self.deklaracija()
        elif (self.name == LISTA_INIT_DEKLARATORA):
            output = self.lista_init_deklaratora(ntip)
        elif (self.name == INIT_DEKLARATOR):
            output = self.init_deklarator(ntip)
        elif (self.name == IZRAVNI_DEKLARATOR):
            output = self.izravni_deklarator(ntip)
        elif (self.name == INICIJALIZATOR):
            output = self.inicijalizator()        
        elif (self.name == LISTA_IZRAZA_PRIDRUZIVANJA):
            output = self.lista_izraza_pridruzivanja()

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
            if is_const_x(self.tip):
                self.l_izraz = 0
            else:
                self.l_izraz = 1

        elif self.right_side(POSTFIKS_IZRAZ, L_ZAGRADA, D_ZAGRADA):
            error = self.children[0].provjeri()
            if error:
                return error
            ft = self.children[0].tip
            if not ft.arguments_types == [VOID]:
                self.error()
            self.tip = ft.return_type
            self.l_izraz = 0
            return ""

        elif self.right_side(POSTFIKS_IZRAZ, L_ZAGRADA, LISTA_ARGUMENATA, D_ZAGRADA):
            error = self.children[0].provjeri()
            if error:
                return error
            error = self.children[2].provjeri()
            if error:
                return error
            required_types_list = self.children[0].arguments_types
            current_types_list = self.children[2].tipovi
            n = len(required_types_list)
            m = len(current_types_list)
            if n != m:
                return self.error()
            for i in range(n):
                if not implicit_cast(self.current_types_list[i], self.required_types_list[i]):
                    self.error()
            return ""


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
        return ""
    

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

        elif (self.right_side(ADITIVNI_IZRAZ, PLUS, MULTIPLIKATIVNI_IZRAZ) or 
                self.right_side(ADITIVNI_IZRAZ, MINUS, MULTIPLIKATIVNI_IZRAZ)):
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
    

    # <bin_ili_izrazi>
    def bin_ili_izrazi(self):
        if self.right_side(BIN_XILI_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(BIN_ILI_IZRAZ, OP_BIN_ILI, BIN_XILI_IZRAZ):
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
    

    # <log_i_izraz>
    def log_i_izraz(self):
        if self.right_side(BIN_ILI_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(LOG_I_IZRAZ, OP_I, BIN_ILI_IZRAZ):
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
    

    # <log_ili_izraz>
    def log_ili_izraz(self):
        if self.right_side(LOG_I_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(LOG_ILI_IZRAZ, OP_ILI, LOG_I_IZRAZ):
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
    

    # <izraz_pridruzivanja>
    def izraz_pridruzivanja(self):
        if self.right_side(LOG_ILI_IZRAZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(POSTFIKS_IZRAZ, OP_PRIDUZI, IZRAZ_PRIDRUZIVANJA):
            error = self.children[0].provjeri()
            if error:
                return error
            if self.children[0].l_izraz != 1:
                return self.error()
            error = self.children[2].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[2].tip, self.children[0].tip):
                return self.error()
            self.tip = self.children[0].tip
            self.l_izraz = 0
        return ""
    

    # <izraz>
    def izraz(self):
        if self.right_side(IZRAZ_PRIDRUZIVANJA):
            error = self.children[0].provjeri()
            if error:
                return error
    def in_loop(self):
        p = self.parent_node
        allowed_parents = [
            NAREDBA, 
            LISTA_NAREDBI, 
            SLOZENA_NAREDBA, 
            NAREDBA_GRANANJA
        ]
        if p.name != NAREDBA_PETLJE:
            if p.name not in allowed_parents:
                return False
            self.tip = self.children[0].tip
            self.l_izraz = self.children[0].l_izraz
        
        elif self.right_side(IZRAZ, ZAREZ, IZRAZ_PRIDRUZIVANJA):
            error = self.children[0].provjeri()
            if error:
                return error
            error = self.children[2].provjeri()
            if error:
                return error
            self.tip = self.children[2].tip
            self.l_izraz = 0
        return ""


    # <slozena_naredba>
    def slozena_naredba(self, lista_identifikatora=None, lista_tipova=None):
        # u oba slucaja ce se tu stvarati prazan scope
        # s tim da ce se puniti sa deklaracijama kad dodje do LISTA_DEKLARACIJA
        # ako se provjerava tijelo funkcije, onda se parametri funkcije
        # moraju spremiti u scope tijela prvo.
        if lista_identifikatora is not None and lista_tipova is not None:
            child_scope = Scope(self.scope_structure.current_scope, LOCAL)
            self.scope_structure.add_child_scope(child_scope)
            for (idn, tip) in zip(lista_identifikatora, lista_tipova):
                self.scope_structure.add_declaration(idn, tip)
        
        if self.right_side(L_VIT_ZAGRADA, LISTA_NAREDBI, D_VIT_ZAGRADA):
            error = self.children[1].provjeri()
            if error:
                return error
            child_scope = Scope(self.scope_structure.current_scope, LOCAL)
            self.scope_structure.add_child_scope(child_scope)
        elif self.right_side(L_VIT_ZAGRADA, LISTA_DEKLARACIJA, LISTA_NAREDBI, D_VIT_ZAGRADA):
            error = self.children[1].provjeri()
            if error:
                return error
            error = self.children[2].provjeri()
            if error:
                return error
            child_scope = Scope(self.scope_structure.current_scope, LOCAL)
            self.scope_structure.add_child_scope(child_scope)
        return ""
        
    # <lista_naredbi>
    def lista_naredbi(self):
        if self.right_side(NAREDBA):
            error = self.children[0].provjeri()
            if error:
                return error
        elif self.right_side(LISTA_NAREDBI, NAREDBA):
            error = self.children[0].provjeri()
            if error:
                return error
            error = self.children[1].provjeri()
            if error:
                return error
        return ""

    # <naredba>
    def naredba(self):
        # sve produkcije su jedinicne
        error = self.children[0].provjeri()
        if error:
            return error
        return ""
    
    # <izraz_naredba>
    def izraz_naredba(self):
        if self.right_side(TOCKAZAREZ):
            self.tip = INT
        if self.right_side(IZRAZ, TOCKAZAREZ):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tip = self.children[0].tip

    # <naredba_grananja>
    def naredba_grananja(self):
        if self.right_side(KR_IF, L_ZAGRADA, IZRAZ, D_ZAGRADA, NAREDBA):
            error = self.children[2].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[2].tip, INT):
                return self.error()
            error = self.children[4].provjeri()
            if error:
                return error
        elif self.right_side(KR_IF, L_ZAGRADA, IZRAZ, D_ZAGRADA, NAREDBA, KR_ELSE, NAREDBA):
            error = self.children[2].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[2].tip, INT):
                return self.error()
            error = self.children[4].provjeri()
            if error:
                return error
            error = self.children[6].provjeri()
            if error:
                return error
        return ""

    # <naredba_petlje>
    def naredba_petlje(self):
        if self.right_side(KR_WHILE, L_ZAGRADA, IZRAZ, D_ZAGRADA, NAREDBA):
            error = self.children[2].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[2].tip, INT):
                return self.error()
            error = self.children[4].provjeri()
            if error:
                return error
        elif self.right_side(KR_FOR, L_ZAGRADA, IZRAZ_NAREDBA, IZRAZ_NAREDBA, D_ZAGRADA, NAREDBA):
            error = self.children[2].provjeri()
            if error:
                return error
            error = self.children[3].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[3].tip, INT):
                return self.error()
            error = self.children[5].provjeri()
            if error:
                return error
        elif self.right_side(KR_FOR, L_ZAGRADA, IZRAZ_NAREDBA, IZRAZ_NAREDBA, IZRAZ, D_ZAGRADA, NAREDBA):
            error = self.children[2].provjeri()
            if error:
                return error
            error = self.children[3].provjeri()
            if error:
                return error
            if not implicit_cast(self.children[3].tip, INT):
                return self.error()
            error = self.children[4].provjeri()
            if error:
                return error
            error = self.children[5].provjeri()
            if error:
                return error
        return ""

    # <naredba_skoka>
    def naredba_skoka(self):
        if self.right_side(KR_CONTINUE, TOCKAZAREZ) or self.right_side(KR_BREAK, TOCKAZAREZ):
            if not self.in_loop():
                return self.error()
        if self.right_side(KR_RETURN, TOCKAZAREZ):
            if self.nesting_function_type() != VOID:
                return self.error()
        if self.right_side(KR_RETURN, IZRAZ, TOCKAZAREZ):
            error = self.children[1].provjeri()
            if error:
                return error
            t = self.nesting_function_type()
            if (t is None) or (not implicit_cast(self.children[1], t)):
                return self.error()
        return ""

    
    # <prijevodna_jedinica>
    def prijevodna_jedinica(self):
        if self.right_side(VANJSKA_DEKLARACIJA):
            error = self.children[0].provjeri()
            if error:
                return error
        if self.right_side(PRIJEVODNA_JEDINICA, VANJSKA_DEKLARACIJA):
            error = self.children[0].provjeri()
            if error:
                return error
            error = self.children[1].provjeri()
            if error:
                return error
        return ""

    # <vanjska_deklaracija>    
    def vanjska_deklaracija(self):
        error = self.children[0].provjeri()
        if error:
            return error
        return ""
    

    # <definicija_funkcije>
    def definicija_funkcije(self):
        if self.right_side(IME_TIPA, IDN, L_ZAGRADA, KR_VOID, D_ZAGRADA, SLOZENA_NAREDBA):
            # provjeri ime tipa
            error = self.children[0].provjeri()
            if error:
                return error
            ime_tipa = self.children[0]
            idn = self.children[1]
            # ime_tipa.tip != const(T)
            if is_const_x(ime_tipa.tip):
                return self.error()
            # ne postoji prije definirana funcija IDN.ime
            if self.scope_structure.idn_name_in_scope(idn.lex):
                return self.error()
            # ako postoji deklaracija imena IDN.ime u globalnom djelokrugu
            # onda je pripadni tip de deklaracije funkcija(void -> <ime_tipa>.tip)
            current_return_type = ime_tipa.tip
            global_scope = self.scope_structure.global_scope()
            if idn.lex in global_scope.declarations:
                required_type = global_scope.declarations[idn.lex]
                if required_type != FunctionType([VOID], current_return_type):
                    self.error()
            # zabiljezi definiciju i deklaraciju funkcije
            self.scope_structure.add_definition(idn.lex, FunctionType([VOID], current_return_type))
            self.scope_structure.add_declaration(idn.lex, FunctionType([VOID], current_return_type))
            # provjeri(<slozena_naredba>)
            error = self.children[5].provjeri()
            if error:
                return error

        elif self.right_side(IME_TIPA, IDN, L_ZAGRADA, LISTA_PARAMETARA, D_ZAGRADA, SLOZENA_NAREDBA):
            error = self.children[0].provjeri()
            # provjeri ime tipa
            if error:
                return error
            ime_tipa = self.children[0]
            idn = self.children[1]
            lista_parametara = self.children[3]
            # ime_tipa.tip != CONST(T)
            if is_const_x(ime_tipa.tip):
                return self.error()
            # ne postoji prije definirana funkcija IDN.ime
            if self.scope_structure.idn_name_in_scope(idn.lex):
                return self.error()
            # provjeri(lista_parametara)
            error = lista_parametara.provjeri()
            if error:
                return error
            # ako postoji deklaracija IDN.ime u globalnom djelokrugu,
            # onda je pripadni tip funkcija(lista_param.tipovi -> ime_tipa.tip)
            current_return_type = ime_tipa.tip
            current_argument_types = lista_parametara.tipovi
            if idn.lex in global_scope.declarations:
                required_type = global_scope.declarations[idn.lex]
                if required_type != FunctionType(current_argument_types, current_return_type):
                    return self.error()
            # zabiljezi definiciju i deklaraciju funkcije
            self.scope_structure.add_definition(idn.lex, FunctionType(current_argument_types, current_return_type))
            self.scope_structure.add_declaration(idn.lex, FunctionType(current_argument_types, current_return_type))
            # provjeri(slozena_naredba) uz parametre funkcije
            # koristeci <lista_param>.tipovi i <lista_param>.imena
            error = self.children[5].provjeri(lista_identifikatora=lista_parametara.identifikatori, 
                lista_tipova=lista_parametara.tipovi)
            if error:
                return error
        
        return ""

    def lista_parametara(self):
        if self.right_side(DEKLARACIJA_PARAMETRA):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tipovi = [self.children[0].tip]
            self.identifikatori = [self.children[0].lex]
        elif self.right_side(LISTA_PARAMETARA, ZAREZ, DEKLARACIJA_PARAMETRA):
            error = self.children[0].provjeri()
            if error:
                return error
            error = self.children[2].provjeri()
            if error:
                return error
            if self.children[2].lex in self.children[0].identifikatori:
                return self.error()
            self.tipovi = self.children[0].tipovi + [self.children[2].tip]
            self.identifikatori = self.children[0].identifikatori + [self.children[2].lex]
        return ""

    def deklaracija_parametra(self):
        if self.right_side(IME_TIPA, IDN):
            error = self.children[0].provjeri()
            if error:
                return error
            if self.children[0].tip == VOID:
                return self.error()
            self.tip = self.children[0].tip
            self.lex = self.children[1].lex
        elif self.right_side(IME_TIPA, IDN, L_UGL_ZAGRADA, D_UGL_ZAGRADA):
            error = self.children[0].provjeri()
            if error:
                return error
            if self.children[0].tip == VOID:
                return self.error()
            self.tip = make_niz(self.children[0].tip)
            self.lex = self.children[1].lex
        return ""

    def lista_deklaracija(self):
        if self.right_side(DEKLARACIJA):
            error = self.children[0].provjeri()
            if error:
                return error
        elif self.right_side(LISTA_DEKLARACIJA, DEKLARACIJA):
            error = self.children[0].provjeri()
            if error:
                return error
            error = self.children[1].provjeri()
            if error:
                return error
        return ""

    def deklaracija(self):
        if self.right_side(IME_TIPA, LISTA_INIT_DEKLARATORA, TOCKAZAREZ):
            error = self.children[0].provjeri()
            if error:
                return error
            current_ntip = self.children[0].tip
            error = self.children[1].provjeri(ntip=current_ntip)
            if error:
                return error
        return ""
    
    def lista_init_deklaratora(self, ntip):
        if ntip is None:
            return self.error()
        self.ntip = ntip
        current_ntip = self.ntip
        if self.right_side(INIT_DEKLARATOR):
            error = self.children[0].provjeri(ntip=current_ntip)
            if error:
                return error
        elif self.right_side(LISTA_INIT_DEKLARATORA, ZAREZ, INIT_DEKLARATOR):
            error = self.children[0].provjeri(ntip=current_ntip)
            if error:
                return error
            error = self.children[2].provjeri(ntip=current_ntip)
            if error:
                return error
        return ""
    
    def init_deklarator(self, ntip):
        if ntip is None:
            return self.error()
        self.ntip = ntip
        current_ntip = self.ntip
        if self.right_side(IZRAVNI_DEKLARATOR):
            error = self.children[0].provjeri(ntip=current_ntip)
            if error:
                return error
            if is_const_x(self.children[0].tip):
                return self.error()
            if is_niz_x(self.children[0].tip):
                return self.error()
        elif self.right_side(IZRAVNI_DEKLARATOR, OP_PRIDUZI, INICIJALIZATOR):
            error = self.children[0].provjeri(ntip=current_ntip)
            if error:
                return error
            error = self.children[2].provjeri()
            if error:
                return error
            izravni_deklarator_type = self.children[0].tip
            if not is_niz_x(izravni_deklarator_type):
                stripped_type = izravni_deklarator_type
                if is_const_x(stripped_type):
                    stripped_type = remove_const_from_const_x(stripped_type)
                if not implicit_cast(self.children[2].tip, stripped_type):
                    return self.error()
            elif is_niz_x(izravni_deklarator_type):
                stripped_type = remove_niz_from_niz_x(izravni_deklarator_type)
                if is_const_x(stripped_type):
                    stripped_type = remove_const_from_const_x(stripped_type)
                if not (self.children[2].br_elem <= self.children[0].br_elem):
                    return self.error()
                for u in self.children[2].tipovi:
                    if not implicit_cast(u, stripped_type):
                        return self.error()
        return ""
    
    def izravni_deklarator(self, ntip):
        if ntip is None:
            return self.error()
        self.ntip = ntip
        if self.right_side(IDN):
            if self.ntip == VOID:
                return self.error()
            if self.scope_structure.idn_name_in_scope(self.children[0].lex):
                return self.error()
            self.scope_structure.add_declaration(self.children[0].lex, self.ntip)
            self.tip = self.ntip
        elif self.right_side(IDN, L_UGL_ZAGRADA, BROJ, D_UGL_ZAGRADA):
            if self.ntip == VOID:
                return self.error()
            if self.scope_structure.idn_name_in_scope(self.children[0].lex):
                return self.error()
            if self.children[2].vrijednost is None:
                return self.error()
            if self.children[2].vrijednost <= 0:
                return self.error()
            elif self.children[2].vrijednost > 1024:
                return self.error()
            array_type = make_niz(self.ntip)
            self.scope_structure.add_declaration(self.children[0].lex, array_type)
            self.tip = array_type
            self.br_elem = self.children[2].vrijednost
        elif self.right_side(IDN, L_ZAGRADA, KR_VOID, D_ZAGRADA):
            if self.scope_structure.idn_name_in_scope(self.children[0].lex):
                required_type = self.scope_structure.type_of_idn_in_scope(self.children[0].lex)
                if required_type != FunctionType([VOID], self.ntip):
                    return self.error()
            else:
                self.scope_structure.add_declaration(self.children[0].lex, 
                    FunctionType([VOID], self.ntip))
        elif self.right_side(IDN, L_ZAGRADA, LISTA_PARAMETARA, D_ZAGRADA):
            error = self.children[2].provjeri()
            if error:
                return error
            if self.scope_structure.idn_name_in_scope(self.children[0].lex):
                required_type = self.scope_structure.type_of_idn_in_scope(self.children[0].lex)
                if required_type != FunctionType(self.children[2].tipovi, self.ntip):
                    return self.error()
            else:
                self.scope_structure.add_declaration(self.children[0].lex, 
                    FunctionType(self.children[2].tipovi, self.ntip))
        return ""

    def inicijalizator(self):
        if self.right_side(IZRAZ_PRIDRUZIVANJA):
            error = self.children[0].provjeri()
            if error:
                return error
            flag, array_length = self.children[0].goes_to_niz_znakova()
            if flag:
                self.br_elem = array_length + 1
                self.tipovi = [CHAR] * self.br_elem
            else:
                self.tip = self.children[0].tip
        elif self.right_side(L_VIT_ZAGRADA, LISTA_IZRAZA_PRIDRUZIVANJA, D_VIT_ZAGRADA):
            error = self.children[1].provjeri()
            if error: 
                return error
            self.br_elem = self.children[1].br_elem
            self.tipovi = self.children[1].tipovi
        return ""
    
    
    def lista_izraza_pridruzivanja(self):
        if self.right_side(IZRAZ_PRIDRUZIVANJA):
            error = self.children[0].provjeri()
            if error:
                return error
            self.tipovi = [self.children[0].tip]
            self.br_elem = 1
        elif self.right_side(LISTA_IZRAZA_PRIDRUZIVANJA, ZAREZ, IZRAZ_PRIDRUZIVANJA):
            error = self.children[0].provjeri()
            if error:
                return error
            error = self.children[1].provjeri()
            if error:
                return error
            self.tipovi = self.children[0].tipovi + [self.children[2].tip]
            self.br_elem = self.children[0].br_elem + 1

    
            
