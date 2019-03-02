import dictionary_scrapping
import unittest
import rstr

class DictionaryScrapping(unittest.TestCase):
    known_values = (("sweet", (["sweet"], ["ADJ"])),
    ("working", (["work"], ["VERB"])),
    ("randomapple", (["randomapple"], ["NOUN"])))

    known_values_def = (
    ("tasting like sugar", (["taste", "sugar"], ["VERB", "NOUN"])),
        ("a working person has a job", (["working", "person", "have", "job"], ["NOUN", "NOUN", "VERB", "NOUN"])),
        )

    known_values_lemma = (("sweet", "sweet"),
    ("working", "work"),
    ("randomapple", "randomapple")
    )


    test_values = tuple(rstr.xeger(r'[a-z]{3,15}') for i in range(3))
    test_value_url = tuple("https://www.macmillandictionary.com/dictionary/{}/{}".format("british", i2) for i2 in test_values)
    # known_values_url = zip([test_values, test_value_url])

    def test_udpipe_checker(self):
        POS_OF_INTEREST = ["NOUN", "VERB", "ADJ", "ADV", "PART"]

        for word_in, output in self.known_values:
            result = dictionary_scrapping.udpipe_checker(word_in)
            self.assertEqual(result, output)

        for word_in, output in self.known_values_def:
            result = dictionary_scrapping.udpipe_checker(word_in)
            self.assertEqual(result, output)

    def udpipe_checker_treebuild(self):
        word_in, context, output = ["tasting", "i love tasting things", "taste"]
        result = dictionary_scrapping.udpipe_checker_treebuild(context, word_in)
        self.assertEqual(result, output)


    def test_get_lemma_word(self):
        for word_in, output in self.known_values_lemma:
            result = dictionary_scrapping.get_lemma_word(word_in)
            self.assertEqual(result, output)

    def test_get_url(self):
        for i in range(len(self.test_values)):
            result = dictionary_scrapping.get_url(self.test_values[i])
            self.assertEqual(result, self.test_value_url[i])


    def test_get_data(self):
        test_data = dictionary_scrapping.get_data("sweet")
        self.assertIn("sweet_1", test_data.find("meta", property="og:url")['content'])
        self.assertEqual("tasting like sugar", test_data.find("span", {"DEFINITION"}).text.strip())

    def test_extract_definition(self):
        test_data = dictionary_scrapping.extract_definition("sweet")
        self.assertEqual("sweet", test_data["word"])
        self.assertEqual("tasting like sugar", test_data["definitions"]["def_1"]["dictionary_entry"])
        self.assertEqual(['taste', 'sugar'], test_data["definitions"]["def_1"]["relevant_words"])


        test_data = dictionary_scrapping.extract_definition("apple")
        self.assertEqual("apple", test_data["word"])
        self.assertEqual("a hard round fruit that is white inside and has a smooth green, yellow, or red skin, which is called peel when it has been removed. The middle part of the apple containing the seeds is called the core. Apples grow on apple trees.", test_data["definitions"]["def_1"]["dictionary_entry"])
        self.assertEqual(['hard',
 'round',
 'fruit',
 'white',
 'inside',
 'have',
 'smooth',
 'green',
 'yellow',
 'red',
 'skin',
 'call',
 'peel',
 'when',
 'remove',
 'middle',
 'part',
 'apple',
 'contain',
 'seed',
 'call',
 'core',
 'Apple',
 'grow',
 'apple',
 'tree'], test_data["definitions"]["def_1"]["relevant_words"])



    # def extract_definition(self):
    #     self.assertEqual()






if __name__ == '__main__':
    unittest.main()
