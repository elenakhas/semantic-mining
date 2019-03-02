from email.policy import default
from typing import Tuple

from tree_builder import TreeBuilder, Node
import sys
import _pickle as pickle
import pprint
from collections import Counter
from run import pickleloader


def tree_counter_launcher(tree_builder: TreeBuilder, root_word: str, max_depth: int = 5) -> Counter:
    """Produce a counter that counts the different words in the tree starting from root_word and with a maximal depth
    of max_depth, according to the semantic graph stored in tree_builder

    This launcher's main is to find the word object in the word database

    :param tree_builder: TreeBuilder containing the word database to explore
    :param root_word: key/lemma corresponding to the word at the root of the tree
    :param max_depth: maximal depth of the tree to explore
    :return: Counter object counting all the word in the tree
    """

    try:
        # Find the word in the wordbase
        root_word_node = tree_builder.primitives.get(root_word,  # we search the word among the primitives
                                                     # if we do net find it we search among the processed words
                                                     tree_builder.processed_words.get(root_word))

        return tree_counter(root_word_node, max_depth)

    except KeyError:
        print("Word {} is not present in the wordbase".format(root_word))
        return Counter()


def tree_counter(root_word: Node, max_depth: int) -> Counter:
    """Recurrent algorithm producing a counter that counts the different words in the tree starting from root_word and with a maximal depth
    of max_depth, see tree_counter_launcher() for the starting procedure

    :param root_word: node corresponding to the word at the root of the tree
    :param max_depth: maximal depth of the tree to explore
    :return: Counter object counting all the word in the tree"""
    counter = Counter()
    counter[root_word] += 1

    # if we have not reached the maximal depth, we look at the children
    # word counter
    if max_depth > 0:
        # Add the counters of all the children of the node
        for child in root_word.children:
            counter += tree_counter(child, max_depth - 1)

    return counter


def similarity_score(tree_counter_1: Counter, tree_counter_2: Counter) -> Tuple[int, int]:
    """Compute a kind of distance between two trees, by using counters of the words composing those trees

    the first distance value is what we call "similarity":

        similarity = number of words shared by both trees / total umber of words in the two trees

    the second distance value is what we call "difference":

        difference = (number of words of the first tree not in the second one +
        number of words of the second tree not in the first one) / total umber of words in the two trees

    :param tree_counter_1: counter of the words in the first tree to compare
    :param tree_counter_2: counter of the words in the second tree to compare
    :return: tuple of two integers: the similarity ratio, and the difference ratio
    """
    # similarity - elements that are in both trees
    similarity = tree_counter_1 & tree_counter_2

    # dissimilarity - elements in 1 but not the other
    # create a copy of the counter and subtract the second counter to it
    difference = Counter(tree_counter_1)
    difference.subtract(tree_counter_2)
    # get the absolute value
    for key in difference: difference[key] = abs(difference[key])

    # total
    total = tree_counter_1 + tree_counter_2

    # produce the ratios
    similarity_ratio = sum(similarity.values()) / sum(total.values())
    difference_ratio = sum(difference.values()) / sum(total.values())

    return similarity_ratio, difference_ratio


if __name__ == "__main__":
    tree_builder = pickleloader("tree_builder_pickled")
    # pprint.pprint([i for i in tree_builder.processed_words])
    print(tree_counter_launcher(tree_builder, "taste"))

    print(tree_builder.processed_words.keys())
    print(similarity_score(tree_counter_launcher(tree_builder, "taste"), tree_counter_launcher(tree_builder, "food")))
