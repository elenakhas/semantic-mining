from tree_builder import TreeBuilder
import sys
import pickle as pickle

word = (len(sys.argv) > 1 and sys.argv[1]) or "hello"
context = (len(sys.argv) > 2 and sys.argv[2]) or "hello this is a test"


# function to load pickle file
def pickleloader(filename):
    # # open the file for writing
    fileObject = open(filename,'rb')

    # load the object from the file into var univ_processed_train
    return pickle.load(fileObject,  encoding="latin1")  #latin1 here, to bypass
                                        # python2 to 3 pickle problem

    # here we close the fileObject
    fileObject.close()

# function to create a file and store the data in the file
def picklemaker(filename, objectname):
    # open the file for writing
    fileObject = open(filename,'wb')

    # this writes the object a to the
    # file named 'testfile'
    pickle.dump(objectname,fileObject)

    # here we close the fileObject
    fileObject.close()

if __name__ == "__main__":
    try:
        tree_builder = pickleloader("tree_builder_pickled")

    except FileNotFoundError:
        tree_builder = TreeBuilder()

    try:
        tree_builder.build_word_tree(word, context, 3)
    except (KeyboardInterrupt, Exception): pass

    filename = "tree_builder_pickled"
    picklemaker(filename, tree_builder)
