from scope import Scope
from consts import *


class ScopeStructure():

    current_scope = None

    def __init__(self, global_scope: Scope):
        self.current_scope = global_scope
        return
    

    def idn_name_in_scope(self, name: str):
        return self.current_scope.idn_name_in_scope(name)
    

    def add_definition(self, idn, type):
        self.current_scope.add_definition(idn, type)
        return
    
    def add_declaration(self, idn, type):
        self.current_scope.add_declaration(idn, type)
        return

    def add_child_scope(self, child: Scope):
        self.current_scope.add_child_scope(child)
        self.current_scope = child
        return
    

    def remove_scope(self):
        if self.current_scope.scope_type == GLOBAL:
            return
        self.current_scope = self.current_scope.parent_scope
        self.current_scope.remove_child_scope()
        return
    
    def global_scope(self):
        if self.current_scope.scope_type == GLOBAL:
            return self.current_scope
        return self.current_scope.parent_scope.global_scope()