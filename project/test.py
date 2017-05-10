from tree import *

ast = Tree()

ast.add_node('Hello')
ast.add_node('something', 'Hello')
ast.add_node('hi', 'something')

ast.changeID('something', 'else', 'Hello')

ast.display('Hello')