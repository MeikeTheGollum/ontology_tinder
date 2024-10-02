import os
import unittest

import gensim.downloader as api

from ontology_tinder.utils import model_coverage_of_words


class UtilsTestCase(unittest.TestCase):

    def test_model_containment(self):
        info = api.info()
        model = api.load(list(info["models"].keys())[0])

        with open(os.path.join("..", "resources", "pruned_names.txt"), "r") as file:
            words = file.read().split("\n")

        contained, not_contained = model_coverage_of_words(model, words)
        print(len(contained)/ len(words))

if __name__ == '__main__':
    unittest.main()
