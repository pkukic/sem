from node import Node
from scope_structure import ScopeStructure


def get_num_spaces_and_plain_str(string: str):
    stripped_str = string.lstrip()
    num_of_leading_spaces = len(string) - len(stripped_str)
    return num_of_leading_spaces, stripped_str


class GenerativeTree():

    root_node = None
    scope_structure = None

    def __init__(self, input: list, scope_structure: ScopeStructure):
        depth = 0
        previous_node = None
        self.scope_structure = scope_structure

        for node_str_raw in input:
            num_of_leading_spaces, node_str = get_num_spaces_and_plain_str(node_str_raw)
            # cases based on the previous node
            # root node case
            if (num_of_leading_spaces == 0):
                self.root_node = Node(node_str, parent_node=None, scope_structure=self.scope_structure)
                previous_node = self.root_node
            # siblings
            elif (num_of_leading_spaces == depth):
                new_node = Node(node_str, parent_node=previous_node.parent_node, scope_structure=self.scope_structure)
                previous_node.parent_node.add_child(new_node)
                previous_node = new_node
            # child
            elif (num_of_leading_spaces == depth + 1):
                new_node = Node(node_str, parent_node=previous_node, scope_structure=self.scope_structure)
                previous_node.add_child(new_node)
                previous_node = new_node
            # uncle
            elif (num_of_leading_spaces < depth):
                difference = depth - num_of_leading_spaces
                temp_node = previous_node
                for i in range(difference + 1):
                    temp_node = temp_node.parent_node
                new_node = Node(node_str, parent_node=temp_node, scope_structure=self.scope_structure)
                temp_node.add_child(new_node)
                previous_node = new_node
            
            # set new depth
            depth = num_of_leading_spaces
        
        return
    

    def print(self):
        self.root_node.print(0)
        return
    
