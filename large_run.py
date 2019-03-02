from run import *


if __name__ == "__main__":
    tree_builder = TreeBuilder()

    filename = "tree_builder_pickled_large"

    with open('noun_contexts.csv') as f:
        word_data = [line.split(';') for line in f.read().split('\n')]
        from pprint import pprint
        pprint(word_data)

    for word, context in word_data:
        print("Starting word '{}', with context {}".format(word, context))
        tree_builder.build_word_tree(word, context, 10)
        print("Ending word '{}', with context {}".format(word, context))

        picklemaker(filename, tree_builder)
        print("Database pickled in '{}',".format(filename))
