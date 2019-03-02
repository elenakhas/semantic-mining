# from __future__ import annotations

from typing import Collection, Set, Any
import dictionary_scrapping

class Node:
    """
    A standard node in a tree, can have children nodes
    """
    # Type hints for internal variables
    name: str
    children: Set

    def __init__(self, name: str):
        self.name = name
        self.children = set()

    def __str__(self) -> str:
        len_ = self.children.__len__()
        children_text = ("no child" if len_ < 1 else
                         "1 child" if len_ == 1 else
                         "{} children".format(len_))
        return "Node \"{}\": {}".format(self.name, children_text)


class Word(Node):
    """
    A word (non-primitive) node in a tree
    """
    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self) -> str:
        len_ = self.children.__len__()
        children_text = ("no child" if len_ < 1 else
                         "1 child" if len_ == 1 else
                         "{} children".format(len_))
        return "Word \"{}\": {}".format(self.name, children_text)

    def get_definition(self) -> Set[str]:
        """Fetch and process the online definition of the current word to obtain a set of relevant lemmas defining the word

        :return: a set of relevant lemmas corresponding to the words in the definition of the current word
        """
        try:
            definitions = dictionary_scrapping.extract_definition(self.name)
            first_definition = set(definitions["definitions"]["def_1"]['relevant_words'])

            return first_definition

        except ValueError:
            return set()


class Primitive(Node):
    """
    A primitive node in a tree, should not have children
    """
    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self) -> str:
        return "Primitive \"{}\"".format(self.name)
