
# coding: utf-8

import re
import time

from bs4 import BeautifulSoup
import urllib.request, json, urllib.error
from unidecode import unidecode


# set the UDPipe API IRI structure
UDPIPE_URL_STRUCTURE = "http://lindat.mff.cuni.cz/services/udpipe/api/process?tokenizer&tagger&parser&model=english-ewt-ud-2.3-181115&data={}"

# set the list of POS we are interested in
POS_OF_INTEREST = ["NOUN", "VERB", "ADJ", "ADV", "PART"]

def udpipe_checker(string: str, pos_of_interest=POS_OF_INTEREST):
    """
    takes a string, puts it in a UDPipe API-usable format, calls UDPipe with tokeniser and tagger,
    extracts the information returned in JSON format and returns a list of words and a list of their
    corresponding parts of speech.

    input: string, pos_of_interest: list
    output: two lists
    """
    string_udpipe = "%20".join(string.split(" "))
    string_udpipe_url = UDPIPE_URL_STRUCTURE.format(string_udpipe)
    # McM's definitions has possesive contractions ('s) and it is in unicode format that is throwing an error downstream
    # we replace the utf for ' (i.e. \u2019) with a single quote here to avoid the problem downstream
    string_udpipe_url = unidecode(string_udpipe_url)

    try:
        with urllib.request.urlopen(string_udpipe_url) as url:
            udpipe_apiresponse = json.loads(url.read().decode('utf-8'))


        # we only want the result part of the JSON
        udpipe_result = udpipe_apiresponse["result"]
        # the results are in a single string and demarcated with newline. so we split them out here
        udpipe_result_ = udpipe_result.split("\n")

        word_list = []
        pos_list = []

        for i in udpipe_result_:
            # we are only interested in the lines of the result part of the UDPipe JSON with words and their POS.
            # these all start with a / and a digit. we use regex to pick these out.
            if re.match(r'^\d', i):
                __ = i.split("\t")

                # index position 1 and 3 of every line in the results part of UDPipe JSON is the word and its corresponding POS
                if __[3] in pos_of_interest:
                    try:
                        get_data(__[2])
                        word_list.append(__[2])
                        pos_list.append(__[3])
                    except ValueError:
                        try:
                            __get_data = get_data(__[1], MCM_URL_STRUCTURE="https://www.macmillandictionary.com/search/{}/?q={}")
                            try:
                                lemma_word = __get_data.find("span", {"class":"INFLX redword "}).text
                            except Exception:
                                try:
                                    lemma_word = __get_data.find("span", {"class":"redword"}).text
                                except Exception:
                                    lemma_word = re.sub(r"\W+", "-",__get_data.find("span", {"class":"BASE"}).text)

                            word_list.append(lemma_word)
                            pos_list.append(__[3])
                            print("Replaced '{}' with '{}' for word '{}'".format(__[2], lemma_word, __[1]))

                        except ValueError:
                            # if the word is not recognised either way, we do not use it
                            #word_list.append(__[1])
                            #pos_list.append(__[3])
                            print("Ignored unknown lemma '{}' for word '{}'".format(__[2],  __[1]))
                            pass

                        except Exception:
                            pass

        return word_list, pos_list

    except (urllib.error.HTTPError, urllib.error.URLError, urllib.error.ContentTooShortError) as e:
        print(e)
        return [], []


def udpipe_checker_treebuild(context: str, root_word):
    """
    takes a string, puts it in a UDPipe API-usable format, calls UDPipe with tokeniser and tagger,
    extracts the information returned in JSON format and returns a list of words and a list of their
    corresponding parts of speech.

    input: context:string, root_word:string
    output: two lists
    """
    string_udpipe = "%20".join(context.split(" "))
    string_udpipe_url = UDPIPE_URL_STRUCTURE.format(string_udpipe)
    # McM's definitions has possesive contractions ('s) and it is in unicode format that is throwing an error downstream
    # we replace the utf for ' (i.e. \u2019) with a single quote here to avoid the problem downstream
    string_udpipe_url = unidecode(string_udpipe_url)

    try:
        with urllib.request.urlopen(string_udpipe_url) as url:
            udpipe_apiresponse = json.loads(url.read().decode('utf-8'))

        # we only want the result part of the JSON
        udpipe_result = udpipe_apiresponse["result"]
        # the results are in a single string and demarcated with newline. so we split them out here
        udpipe_result_ = udpipe_result.split("\n")

        for i in udpipe_result_:
            # we are only interested in the lines of the result part of the UDPipe JSON with words and their POS.
            # these all start with a / and a digit. we use regex to pick these out.
            if re.match(r'^\d', i):
                __ = i.split("\t")

                # index position 1 and 3 of every line in the results part of UDPipe JSON is the word and its corresponding POS
                if __[1] == root_word:

                    return __[2]
        return root_word

    except (urllib.error.HTTPError, urllib.error.URLError, urllib.error.ContentTooShortError) as e:
        print(e.info())
        return root_word


def get_lemma_word(word: str) -> str:
    """
    Get the stem of the word being searched

    :param word: word input by the user, which we will obtain the stem for
    :return: the stem of the word we are searching for
    """
    # we use the udpipe_checker to access UDPipe to obtain the stem of the word

    return udpipe_checker(word)[0][0]


def get_url(word: str, dictionary: str = 'british', MCM_URL_STRUCTURE: str = "https://www.macmillandictionary.com/dictionary/{}/{}") -> str:
    """
    Produce the URL of the definition of a word

    :param word: word to search in the dictionary, which we will obtain the stem for
    :param dictionary: possible values are: 'british' and 'american'
    :return: the URL of the word in the dictionary
    """

    return MCM_URL_STRUCTURE.format(dictionary, word)


def get_data(word: str, dictionary: str = 'british',MCM_URL_STRUCTURE: str = "https://www.macmillandictionary.com/dictionary/{}/{}") -> BeautifulSoup:
    """
    Produce the HTML content of the definition of a word

    :param word: word to search in the dictionary
    :param dictionary: possible values are: 'british' and 'american'
    :return: the HTML content of the definition in the dictionary
    """
    # set the url of the MacMillan dictionary entry for the word
    dict_url = get_url(word, dictionary, MCM_URL_STRUCTURE)

    # open a connexion to the dictionary page
    try:
        request = urllib.request.urlopen(dict_url)
    except urllib.error.URLError:
        try:
            request = urllib.request.urlopen(dict_url)
            time.sleep(1)
        except urllib.error.URLError:
            request = urllib.request.urlopen(dict_url)
            time.sleep(10)

    # grab the page source content
    dict_fulldata = BeautifulSoup(request, "lxml")

    if "Sorry, no search result for" in dict_fulldata.find_all({"h1"})[0].text:
        raise ValueError('The word {} is not in the dictionary'.format(word))
    else:
        return dict_fulldata



def extract_definition(word_input: str, dictionary: str = 'british'):
    """
    Extract the information from the definition of a word in the MacMillan dictionary

    :param word_input: word to search in the dictionary
    :param dictionary: possible values are: 'british' and 'american'
    :return: a dictionary containing various information about the definition of the word in the dictionary
    """

    # Get the HTML data of the word definition
    dict_fulldata = get_data(word_input, dictionary)

    # extract the definitions and store in a dictionary
    dict_processed = {
        # the first layer key for the dictionary is the word we are building the semantic tree for.
        "word": word_input,

        # we nest an empty dictionary with the key "definitions" to store the various definitions of the word.
        "definitions": {}
    }

    # using find_all in BS4, we extract only the dictionary definitions
    # be aware that the structure of the McM website is such that they embed url links to definitions of words
    # in a dictionary entry.

    # let's pick out all the URLs that McM has embedded into each definition of the word
    definitions = dict_fulldata.find_all("span", {"DEFINITION"})

    for i in range(len(definitions)):
        # a simple way to get only the definitions text (e.g. without all the URLs etc..,) is to use the BS4 .text method
        definition = definitions[i].text
        # let's get rid of spaces at the start of the definition
        definition = definition.lstrip(" ")
        # for each definition, we create an empty dictionary
        dict_processed["definitions"]["def_"+str(i+1)] = {}
        # we here the dictionary entry
        dict_processed["definitions"]["def_"+str(i+1)]["dictionary_entry"] = definition

        # we run the udpipechecker function here to obtain the POS for the dictionary entry. we only extract the
        # words that have POS we are interested in
        relevant_words = udpipe_checker(definition)[0]
        dict_processed["definitions"]["def_"+str(i+1)]['relevant_words'] = relevant_words
        urls = definitions[i].find_all("a", {"QUERY"})
        # this extracts all the words that the URLs are for and puts them in a list. we are going to use this
        # list for checking in the next step.
        url_words = [i2.text for i2 in urls]

        # we create an empty set that we will store all the URLs for the relevant words in a dictionary entry
        dict_processed["definitions"]["def_"+str(i+1)]["urls"] = set()

        for word in relevant_words:
            for url in urls:
                if word.lower() == url.text:
                    dict_processed["definitions"]["def_"+str(i+1)]["urls"].add(url['href'])
            if word.lower() not in url_words:
                mcm_urlstructure = "https://www.macmillandictionary.com/dictionary/{}/{}"
                dict_processed["definitions"]["def_"+str(i+1)]["urls"].add(get_url(word.lower(), dictionary))

    return dict_processed

if __name__ == "__main__":
    # ##### 1. Ask for word, ask for British or American English.
    word = 'apple'  # input("What is the word you want to build the semantic tree for?")
    dictionary = 'british'  # input("Do you want the British or the American English definition?")

    dict_processed = extract_definition(word, dictionary)


    import pprint

    pprint.pprint(dict_processed)
