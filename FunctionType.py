class FunctionType:
    def __init__(self, arguments_types=[], return_type=None):
        self.arguments_types = arguments_types
        self.return_type = return_type

    def __eq__(self, other):
        return isinstance(other, FunctionType) and self.arguments_types == other.arguments_types and \
            self.return_type == other.return_type
    

    # def __str__(self):
    #     return self.arguments_types + "->" + self.return_type
    

    # def __repr__(self):
    #     return self.arguments_types + "->" + self.return_type