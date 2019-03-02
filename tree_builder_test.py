from tree_builder import *
from primitives import get_primitives_dict
import unittest


class TreeBuilderTest(unittest.TestCase):
    """ there are 3 things to check:
        - return value:
            when we ask for a primitive, it gives the primitive (ex: time)
            when we ask for a known word, it gives the correct word object
            when we ask for an unknown word, build the tree and add the word to known words
        - depth limiter:

        - word-base modification:
        """
    def setUp(self):
        # fictive words

        pass

    def test_init(self) -> None:
        tree_builder = TreeBuilder()

        self.assertEqual(tree_builder.primitives.keys(), get_primitives_dict().keys())
        self.assertIsInstance(tree_builder.processed_words, dict)

    def test_build_word_tree_return_primitive(self) -> None:
        tree_builder = TreeBuilder()

        # when we ask for a primitive, it gives the primitive (ex: time)
        for primitive in get_primitives_dict().keys():
            self.assertIn(primitive, tree_builder.primitives.keys())

            result = tree_builder.build_word_tree(primitive)
            self.assertIsInstance(result, Primitive)
            self.assertIs(result, tree_builder.primitives[primitive])

    def test_build_word_tree_return_known_word(self) -> None:
        tree_builder = TreeBuilder()

        # when we ask for a known word, it gives the correct word object
        test_word = Word('test_word')
        tree_builder.processed_words['test_word'] = test_word

        result = tree_builder.build_word_tree('test_word')

        self.assertIn('test_word', tree_builder.processed_words.keys())
        self.assertIsInstance(result, Word)
        self.assertIs(result, test_word)

    def test_build_word_tree_return_unknown_word_no_def(self) -> None:
        # when we ask for an unknown word, build the tree and add the word to known words
        tree_builder = TreeBuilder()
        # replace get_definition: empty definition
        Word.get_definition = lambda self: {}

        result = tree_builder.build_word_tree('test_word')

        self.assertIn('test_word', tree_builder.processed_words.keys())
        self.assertEqual(result.name, 'test_word')
        self.assertSetEqual(result.children, set())

    def test_build_word_tree_return_unknown_word_primitive_def(self) -> None:
        # when we ask for an unknown word, build the tree and add the word to known words
        from random import choice

        tree_builder = TreeBuilder()
        # replace get_definition: primitives only definition
        Word.get_definition = lambda self: {choice(list(tree_builder.primitives.keys())),
                                            choice(list(tree_builder.primitives.keys())),
                                            choice(list(tree_builder.primitives.keys()))}

        result = tree_builder.build_word_tree('test_word')

        self.assertIn('test_word', tree_builder.processed_words.keys())
        self.assertEqual(result.name, 'test_word')
        self.assertIsInstance(result.children, set)
        self.assertLessEqual(len(result.children), 3)
        for child in result.children:
            self.assertIsInstance(child, Primitive)

    def test_build_word_tree_return_unknown_word_known_words_def(self) -> None:
        tree_builder = TreeBuilder()
        tree_builder.processed_words = {'known_word_1': Word('known_word_1'), 'known_word_2': Word('known_word_2')}
        # replace get_definition: known words definition
        Word.get_definition = lambda self: {'known_word_1', 'known_word_2'}

        result = tree_builder.build_word_tree('test_word')
        self.assertIn('test_word', tree_builder.processed_words.keys())
        self.assertEqual(result.name, 'test_word')
        self.assertSetEqual(result.children, {tree_builder.processed_words['known_word_1'],
                                              tree_builder.processed_words['known_word_2']})

    def test_build_word_tree_return_unknown_word_self_def(self) -> None:
        tree_builder = TreeBuilder()
        # replace get_definition: identical words definition
        Word.get_definition = lambda self: {'test_word'}

        result = tree_builder.build_word_tree('test_word')
        self.assertIn('test_word', tree_builder.processed_words.keys())
        self.assertEqual(result.name, 'test_word')
        self.assertSetEqual(result.children, set())

    def test_build_word_tree_return_unknown_word_complex_def(self) -> None:

        class PhantomWord(Word):
            """
            Phantom word class with specific function
            """

            def get_definition(self):
                if self.name == 'test_word':
                    return {'test_word_1', 'test_word_2'}

                elif self.name == 'test_word_1':
                    return {'test_word_2'}

                elif self.name == 'test_word_2':
                    return {'test_word_3', 'time'}

                else:
                    return {'i'}

        tree_builder = TreeBuilder()
        # replace get_definition: unknown words definition
        Word.get_definition = PhantomWord.get_definition

        result = tree_builder.build_word_tree('test_word')
        self.assertIn('test_word', tree_builder.processed_words.keys())
        self.assertIn('test_word_1', tree_builder.processed_words.keys())
        self.assertIn('test_word_2', tree_builder.processed_words.keys())
        self.assertIn('test_word_3', tree_builder.processed_words.keys())

        self.assertEqual(result.name, 'test_word')
        result_children_dict = {child.name: child for child in result.children}
        self.assertIn('test_word_1', result_children_dict.keys())
        self.assertIn('test_word_2', result_children_dict.keys())

        result_1_children_dict = {child.name: child for child in result_children_dict['test_word_1'].children}
        self.assertIn('test_word_2', result_1_children_dict.keys())

        result_2_children_dict = {child.name: child for child in result_children_dict['test_word_2'].children}
        self.assertIn('test_word_3', result_2_children_dict.keys())
        self.assertIn('time', result_2_children_dict.keys())
        self.assertIsInstance(result_2_children_dict['time'], Primitive)

        result_3_children_dict = {child.name: child for child in result_2_children_dict['test_word_3'].children}
        self.assertIn('i', result_3_children_dict.keys())
        self.assertIsInstance(result_3_children_dict['i'], Primitive)



if __name__ == "__main__":
    unittest.main()
