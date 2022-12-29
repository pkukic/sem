from FunctionType import FunctionType
from consts import GLOBAL

class Scope():

    parent_scope = None
    child_scope = None
    idn_values = []
    function_values = []
    scope_type = None

    def __init__(self, parent_scope, scope_type):
        self.parent_scope = parent_scope
        self.child_scope = None
        self.declarations = {}
        self.definitions = {}
        self.idn_values = []
        self.scope_type = scope_type
        return
    

    def add_parent_scope(self, parent):
        self.parent_scope = parent
        return
    

    def add_child_scope(self, child):
        child.add_parent_scope(self)
        self.child_scope = child
        return
    

    def remove_child_scope(self):
        self.child_scope = None
        return
    

    def add_definition(self, idn, type):
        self.definitions[idn] = type
        self.idn_values.append(idn)
        return
    
    def add_declaration(self, idn, type):
        self.declarations[idn] = type
        self.idn_values.append(idn)
        return
    

    def idn_name_in_scope(self, name: str):
        for value in self.idn_values:
            if value == name:
                return True
        if self.parent_scope:
            return self.parent_scope.idn_name_in_scope(name)
        return False
    
    def idn_name_in_local_scope(self, name: str):
        for value in self.idn_values:
            if value == name:
                return True
        return False

    def type_of_idn_in_scope(self, name):
        if name in self.declarations:
            return self.declarations[name]
        elif name in self.definitions:
            return self.definitions[name]
        return self.parent_scope.type_of_idn_in_scope(name)

    def function_definitions(self):
        local_function_definitions = {k: v for (k, v) in self.definitions.items() if isinstance(self.definitions[k], FunctionType)}
        if not self.parent_scope:
            return local_function_definitions
        return local_function_definitions | self.parent_scope.function_definitions()

    def function_declarations(self):
        local_function_declarations = {k: v for (k, v) in self.definitions.items() if isinstance(self.declarations[k], FunctionType)}
        if not self.parent_scope:
            return local_function_declarations
        return local_function_declarations | self.parent_scope.function_definitions()

    def global_scope(self):
        if self.scope_type == GLOBAL:
            return self
        return self.parent_scope.global_scope()
