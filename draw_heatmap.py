from typing import List, Optional

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

import dictionary_scrapping
from tree_counter import *
from pprint import pprint

label_noun = ["noun_{}".format(i) for i in range(8)]
label_adjective = ["adjective_{}".format(i) for i in range(12)]

data = np.array([[.5458,.8673,.9434],
                 [.1954,.2344,.4354]])
data = np.random.randn(8, 12)

# code is from https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html

# sentences = np.array([["".format(label_noun, data[i,j]*100) for j in range(len(data[i]))] for i in range(len(data))])
# labels = np.array([["".format(label_noun, data[i,j]*100) for j in range(len(data[i]))] for i in range(len(data))])

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Arguments:
        data       : A 2D numpy array of shape (N,M)
        row_labels : A list or array of length N with the labels
                     for the rows
        col_labels : A list or array of length M with the labels
                     for the columns
    Optional arguments:
        ax         : A matplotlib.axes.Axes instance to which the heatmap
                     is plotted. If not provided, use current axes or
                     create a new one.
        cbar_kw    : A dictionary with arguments to
                     :meth:`matplotlib.Figure.colorbar`.
        cbarlabel  : The label for the colorbar
    All other arguments are directly passed on to the imshow call.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=["black", "white"],
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Arguments:
        im         : The AxesImage to be labeled.
    Optional arguments:
        data       : Data used to annotate. If None, the image's data is used.
        valfmt     : The format of the annotations inside the heatmap.
                     This should either use the string format method, e.g.
                     "$ {x:.2f}", or be a :class:`matplotlib.ticker.Formatter`.
        textcolors : A list or array of two color specifications. The first is
                     used for values below a threshold, the second for those
                     above.
        threshold  : Value in data units according to which the colors from
                     textcolors are applied. If None (the default) uses the
                     middle of the colormap as separation.

    Further arguments are passed on to the created text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[im.norm(data[i, j]) > threshold])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts


def plot(data_similarity: List[List[float]],
         data_difference: List[List[float]],
         label_noun: List[str],
         label_adjective: List[str],
         two_plots: Optional[bool]=True) -> None:
    """Draws the heatmap for two sets of data: a similarity matrix and a difference matrix

    :param data_similarity: two dimensional array of similarity ratios, of size (N * A)
    :param data_difference: two dimensional array of difference ratios, of size (N * A)
    :param label_noun: list of labels for the nouns (or the first dimension of the data)
    :param label_adjective: list of labels for the adjectives (or the second dimension of the data)
    :param two_plots: optional argument, default value is True; if true, draws similarity and difference on two plots,
    otherwise draws them on a single plot side by side
    """

    data_percentile_similarity = np.array([[cell * 100 for cell in line] for line in data_similarity])
    data_percentile_difference = np.array([[cell * 100 for cell in line] for line in data_difference])

    if two_plots:
        # Two plots
        # draw similarity
        fig, ax = plt.subplots()

        im, _ = heatmap(data_percentile_similarity, label_noun, label_adjective, ax=ax,
                           cmap="YlGn", cbarlabel="Similarity %\n(# shared words / # words in the two trees)")
        annotate_heatmap(im, valfmt="{x:.1f} %")

        fig.tight_layout()
        plt.show()

        # draw difference
        fig, ax = plt.subplots()

        im, _ = heatmap(data_percentile_difference, label_noun, label_adjective, ax=ax,
                           cmap="YlOrRd", cbarlabel="Difference %\n(# non-shared words / # words in the two trees)")
        annotate_heatmap(im, valfmt="{x:.1f} %")

        fig.tight_layout()
        plt.show()

    else:
        # One plot
        # draw similarity
        fig, (ax1, ax2) = plt.subplots(1, 2)

        im, _ = heatmap(data_percentile_similarity, label_noun, label_adjective, ax=ax1,
                           cmap="YlGn", cbarlabel="Similarity %\n(# shared words / # words in the two trees)")
        annotate_heatmap(im, valfmt="{x:.1f} %")

        im, _ = heatmap(data_percentile_difference, label_noun, label_adjective, ax=ax2,
                           cmap="YlOrRd", cbarlabel="Difference %\n(# non-shared words / # words in the two trees)")
        annotate_heatmap(im, valfmt="{x:.1f} %")

        fig.tight_layout()
        plt.show()


if __name__ == "__main__":
    tree_builder = pickleloader("tree_builder_pickled")

    # get the words and their contexts
    # with open('noun_contexts.csv') as f:
    #     contexts_noun = [line.split(';') for line in f.read().split('\n')]
    # with open('adj_contexts.csv') as f:
    #     contexts_adj = [line.split(';') for line in f.read().split('\n')]
    contexts_noun = [['taste', 'taste'], ['mouth', 'mouth'], ['eat', 'eat']]
    contexts_adj = [['drink', 'drink'], ['create', 'create'], ['flavour', 'I love that flavour']]

    # get the key (lemma) corresponding to the word
    lemmas_noun = [dictionary_scrapping.udpipe_checker_treebuild(context, word) for word, context in contexts_noun]
    lemmas_adj = [dictionary_scrapping.udpipe_checker_treebuild(context, word) for word, context in contexts_adj]

    # get the counters for all the words
    counters_noun = [tree_counter_launcher(tree_builder, root_word) for root_word in lemmas_noun]
    counters_adj = [tree_counter_launcher(tree_builder, root_word) for root_word in lemmas_adj]

    # build the distance matrix
    data_similarity_difference = [
        [similarity_score(noun, adj) for adj in counters_adj]
        for noun in counters_noun
    ]

    data_similarity = [[cell[0] for cell in line] for line in data_similarity_difference]
    data_difference = [[cell[1] for cell in line] for line in data_similarity_difference]

    # draw the similarity matrices

    plot(data_similarity, data_difference, lemmas_noun, lemmas_adj, False)

    # pprint(tree_builder.processed_words.keys())
    # pprint(similarity_score(tree_counter_launcher(tree_builder, "taste"), tree_counter_launcher(tree_builder, "food")))
