# Copyright (C) by Brett Kromkamp 2011-2014 (brett@perfectlearn.com)
# You Programming (http://www.youprogramming.com)
# May 03, 2014
# Altered by: Jesse Opitz
# No longer has @property anywhere
# Added del_child

class Node:
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__children = []

    def identifier(self):
        return self.__identifier

    def children(self):
        return self.__children

    def add_child(self, identifier):
        self.__children.append(identifier)

    # Added by: Jesse Opitz
    def del_child(self, identifier):
        self.__children.remove(identifier)
