Description
Method for NLP project

## Files
* `toy_corpus/`: **[Obsolete]** folder where the toy corpus data is located
  * `xml/`: folder where the XML version of the definitions are located
    * `carrot.xml`: XML of the definition of the noun "carrot", source is 
    [the article "carrot" of the McMillan Dictionary](https://www.macmillandictionary.com/dictionary/british/carrot)
    * `sweet_1.xml`: XML of the definition of the adjective "sweet", source is 
    [the article "sweet_1" of the McMillan Dictionary](https://www.macmillandictionary.com/dictionary/british/sweet_1)
* `dictionary_scrapping.py`: file containing the functions needed to interact with UD Pipe and the McMillan dictionary; 
among the interactions, there is: the extraction a definition given its dictionary key (basically the lemma) and the 
extraction of the correct key/lemma for a given word and a given context; the support for word search should is 
included, and is used as a backup for unrecognised lemma or words
* `word_tree.py`: file containing the classes necessary to build a semantic tree: Node, and its children Word and 
Primitives
* `primitives.py`: file containing a single function to create a dictionary of all the primitives, as described in 
https://intranet.secure.griffith.edu.au/schools-departments/natural-semantic-metalanguage/in-brief
* `tree_builder.py`: file containing the class TreeBuilder, which contains the tools to create a semantic tree for a 
word (linking words to their children)
* `tree_counter.py`: file containing the functions needed to process some kind of distance between trees based on the
words present in that tree
* `draw_heatmap.py`: file containing the functions needed to process the similarity/distance matrices for the different 
words and adjectives; it also operates as a script to compute those matrices and draw a heatmap (a collored martix) for
each matrix
* `run.py`: file containing the functions needed to run a basic tree building process for an explicitly defined word and
context
* `large_run.py`: script similar to `run.py` put processing all the words from `noun_contexts.csv` and
`adj_contexts.csv`

* `dictionary_scrapping_test.py`: unit tests for `dictionary_scrapping_test.py`
* `word_tree_test.py`: unit tests for `word_tree_test.py`
* `tree_builder_test.py`: unit tests for `tree_builder_test.py`
* `tree_counter_test.py`: unit tests for `tree_counter_test.py`

* `noun_contexts.csv`: file contains all the nouns of the toy corpus, and a context for each of them
* `adj_contexts.csv`: file contains all the adjectives of the toy corpus, and a context for each of them

## Setup & Dependencies
This project is built using Python 3.7

The following packages are needed:
* `lxml`
* `bs4`
* `unidecode`
* `pickle`

## Usage
To use the file contained in this repository, you can either use each file individually or use only the intended 
process. I you wish to use each file individually, there is for most of them a ``if __name__ == '__main__':`` statement
giving an example of how to use the different processes of the file and what kind of result they give.

### Intended use
The intended use is composed of two main steps:
1. creating and populating a word database, which means creating an oriented semantic graph of as set of 
interesting words according to their definition in the McMillan dictionary;
2. using the created graph to explore the semantic trees of specific words and comparing them.

#### Fist step: creating and populating a word database
This step is currently really long (more than 4 hours for 1 word and a maximal distance to the word of 10), so we 
provide a sample database in the pickled TreeBuilder `tree_builder_pickled` and a larger one in 
`tree_builder_pickled_large`.

If you still want to create another word database, modify `large_run.py` by replacing the word list file
(`..._contexts.csv`) by your own using a similar structure. Then, choose the maximal distance to the word for 
construction of the graph (last argument `10` in `tree_builder.build_word_tree(word, context, 10)`).
You can now run the script and wait for your database to be populated.

The last option is to use a given database, and to add now words to it.
Do do so, you will need to unpickle a database, run `build_tree(new_word, context_for_the_new_word)` on it, then 
pickling it once again (you can see that process in the ``if __name__ == '__main__':`` statement in `run.py`)

#### Second step: exploring the graph
The second step is to use the graph to compare words. To do so, you can either draw a similarity matrix heatmap (refer 
to the ``if __name__ == '__main__':`` statement in `draw_heatmap.py`) or just get the similarity ratio between two words
(refer to the ``if __name__ == '__main__':`` statement in `tree_counter.py`).

To directly obtain results from a word database, just run `draw_heatmap.py`.

## Theoretical basis
### Distance between ordered trees
* https://www.ifi.uzh.ch/dbtg/teaching/thesesarch/Vertiefung_LeaBay_v2.pdf
* https://arxiv.org/abs/1508.03381
* [https://doi.org/10.1007/978-3-642-22194-1_71](https://sci-hub.tw/https://doi.org/10.1007/978-3-642-22194-1_71)

### Distance between unordered trees
* [https://ieeexplore.ieee.org/document/6630333](https://sci-hub.tw/https://ieeexplore.ieee.org/document/6630333)
* [https://ieeexplore.ieee.org/document/1260818](https://sci-hub.tw/https://ieeexplore.ieee.org/document/1260818)

## References
