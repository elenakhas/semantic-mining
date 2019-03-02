import unittest
from run import pickleloader
import tree_counter, tree_builder, primitives, word_tree

class TreeCounterTest(unittest.TestCase):

    def setUp(self):
        # create a first instance of a tree for testing.
        test_string = "the test will end when it ends"
        test_string_split = test_string.split(" ")
        test = {}
        primitive = primitives.get_primitives_dict()

        for i in range(len(test_string_split)):
            if test_string_split[i] in primitive.keys():
                test[test_string_split[i]] = word_tree.Primitive(test_string_split[i])
            else:
                test[test_string_split[i]]=  word_tree.Word(test_string_split[i])

        test["the"].children.add(test["test"])
        test["the"].children.add(test["will"])
        test["the"].children.add(test["when"])
        test["test"].children.add(test["will"])
        test["test"].children.add(test["end"])
        test["will"].children.add(test["ends"])

        #create a 2nd instance of a tree for testing.
        test_instance_tree = tree_builder.TreeBuilder()
        test_instance_tree.processed_words = test

        test_string1 = "a moon was sent over the sea"
        test_string_split1 = test_string1.split(" ")
        test1 = {}

        for i in range(len(test_string_split1)):
            if test_string_split1[i] in primitive.keys():
                test1[test_string_split1[i]] = word_tree.Primitive(test_string_split1[i])
            else:
                test1[test_string_split1[i]]=  word_tree.Word(test_string_split1[i])

        test1["a"].children.add(test1["moon"])
        test1["a"].children.add(test1["was"])
        test1["a"].children.add(test1["sent"])
        test1["moon"].children.add(test1["over"])
        test1["moon"].children.add(test1["sea"])
        test1["over"].children.add(test1["sea"])

        test_instance_tree1 = tree_builder.TreeBuilder()
        test_instance_tree1.processed_words = test1

        # generate known values for test_tree_counter_launcher
        known_values1 = ("the", [str(i) for i in tree_counter.tree_counter_launcher(test_instance_tree, "the").keys()])

        # generate known values for test_tree_counter
        known_values2 = (test_instance_tree.processed_words["the"], tree_counter.tree_counter(test_instance_tree.processed_words["the"], max_depth=1))

        # generate known values for test_similarity_score
        tree_counter_1, tree_counter_2 = tree_counter.tree_counter(test_instance_tree.processed_words["the"], max_depth=1), tree_counter.tree_counter(test_instance_tree1.processed_words["a"], max_depth=1)
        known_values3 = ([tree_counter_1, tree_counter_2], (tree_counter.similarity_score(tree_counter_1, tree_counter_2)))

        return test_instance_tree, known_values1, known_values2, known_values3

    def test_tree_counter_launcher(self):
        '''
        given a word in string form, tree_counter_launcher should return a counter with a count of all the words in the word's semantic tree
        '''
        # use 2nd variable returned from self.setUp()
        word_in, output = self.setUp()[1]
        result_prelim = tree_counter.tree_counter_launcher(self.setUp()[0], word_in).keys()
        # extract the name of each Word in the counter, in order to compare with known results
        result = [str(i) for i in result_prelim]
        self.assertEqual(result, output)


    def test_tree_counter(self):
        '''
        given a Word, produces a counter that counts the different words in the tree starting from root_word and with a maximal depth
        '''
        # use 3rd variable returned from self.setUp()

        word_in, output = self.setUp()[2]
        result = tree_counter.tree_counter(word_in, max_depth=1)
        self.assertEqual(result, output)


    def test_similarity_score(self):
        '''
        given two different counters, provide the similarity score for them
        '''
        # use 4th variable returned from self.setUp()

        word_in, output = self.setUp()[3]
        result = tree_counter.similarity_score(word_in[0],word_in[1])
        self.assertEqual(result, output)



if __name__ == '__main__':
    unittest.main()
