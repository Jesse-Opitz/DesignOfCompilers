# Brett Kromkamp (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014
#
# Altered by: Jesse Opitz

from node import Node

(_ROOT, _DEPTH, _BREADTH) = range(3)


class Tree:

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, identifier, parent=None):
        node = Node(identifier)
        self[identifier] = node

        if parent is not None:
            self[parent].add_child(identifier)

        return node

    # Added by: Jesse Opitz
    def changeID(self, identifier, newID, parent=None):
        node = Node(newID)

        if parent is not None:
            #print('Parent: ' + str(self.__nodes[parent].identifier()))
            #print('Parent children: ' + str(self.__nodes[parent].children()))

            self.__nodes[parent].add_child(node.identifier())
            self.__nodes[parent].del_child(identifier)

            #print('Parent Children now: ' + str(self.__nodes[parent].children()))
        for i in self.__getitem__(identifier).children():
            node.add_child(i)
        #print('Old node children: ' + str(self.__nodes[identifier].children()))
        #print('New node children: ' + str(node.children()))
        #print(self.__nodes)
        newDict = {}
        for key, value in self.__nodes.items():
            if key == identifier:
                newDict[newID] = node
                #print('Key: ' + key)
                #print('Node: ' + str(node))
            else:
                newDict[key] = value
                #print('Key: ' + key)
                #print('Value: ' + str(value))
        #print('New dict: ' + str(newDict))
        self.__nodes = newDict


        #ident =
        #print(ident.identifier())
        #print(ident)

        #return ident

    def display(self, identifier, depth=_ROOT):
        children = self[identifier].children
        if depth == _ROOT:
            print("{0}".format(identifier))
        else:
            #Altered print statement from:
            # print("\t"*depth, "{0}".format(identifier))
            # to current print statement
            print("--|"*depth, "{0}".format(identifier))

        depth += 1
        for child in children():
            self.display(child, depth)  # recursive call

    def traverse(self, identifier, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from 
        # 'Essential LISP' by John R. Anderson, Albert T. Corbett, 
        # and Brian J. Reiser, page 239-241
        yield identifier
        queue = self[identifier].children()
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children()
            if mode == _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode == _BREADTH:
                queue = queue[1:] + expansion  # width-first

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item
