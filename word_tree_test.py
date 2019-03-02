import word_tree
import unittest

class TestWordNames(unittest.TestCase):
    known_values = (("randomapple", "randomapple"),
    ("purplechicken", "purplechicken"),
    ("waterbomb","waterbomb"))

    known_values2 = ("question", {"ask", "want", "information"})
    known_values3 = "randomapple"

    def test_Node_init(self):
        '''a Node initiated should return its own name'''

        for word_in, output in self.known_values:

            test_Node = word_tree.Node(word_in)
            test_Node_name = test_Node.name
            self.assertEqual(test_Node_name, output)

    def test_Node_add(self):
        '''a word added to a node should be within the node's children'''
        # we want to test that it adds a child []
        # we want to test that the child it adds is exactly what we asked it to add
        test_Node = word_tree.Node("test")

        for word_in, output in self.known_values:
            test_Node.add(word_in)
            self.assertTrue(output in test_Node.children)


    def test_Node_add_all(self):
        # we want to test that it adds a child []
        # we want to test that the child it adds is exactly what we asked it to add
        test_Node = word_tree.Node("test")

        words_in = [word_in for word_in, output in self.known_values]
        outputs = {output for word_in, output in self.known_values}
        test_Node.add_all(words_in)
        self.assertTrue(outputs.issubset(test_Node.children))

    def test_Word_init(self):
        '''a Word initiated should return its own name'''

        for input, output in self.known_values:

            test_Word = word_tree.Word(input)
            test_Word_name = test_Word.name
            self.assertEqual(test_Word_name, output)

    def test_Primitive_init(self):
        '''a Primitive initiated should return its own name'''

        for word_in, output in self.known_values:

            test_Primitive = word_tree.Primitive(word_in)
            test_Primitive_name = test_Primitive.name
            self.assertEqual(test_Primitive_name, output)

    def test_Word_get_definition(self):
        '''a Word's defintion's should only include the words that deemed to be relevant and should not include primitives'''

        # case #1 the word exists and the results should be correct
        word_in, output = self.known_values2
        test_Word = word_tree.Word(word_in)
        test_Word_def = test_Word.get_definition()
        self.assertEqual(test_Word_def, output)

        # case #2 the word does not exist
        test_Word = word_tree.Word(self.known_values3)
        with self.assertRaises(ValueError):
            test_Word.get_definition()



if __name__ == '__main__':
    unittest.main()
