class Scope():

    parent_scope = None
    child_scope = None
    idn_values = []
    function_values = []
    scope_type = None

    def __init__(self, parent_scope, scope_type):
        self.parent_scope = parent_scope
        self.child_scope = None
        self.idn_values = []
        self.function_values = []
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
    

    def add_idn(self, idn):
        self.idn_values.append(idn)
        return
    

    def add_function(self, func):
        self.function_values.append(func)
        return
    

    def idn_name_in_scope(self, name: str):
        for value in self.idn_values:
            if value.name == name:
                return True
        if self.parent_scope:
            return self.parent_scope.idn_name_in_scope(name)
        return False