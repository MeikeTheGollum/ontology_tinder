import os
import unittest

from nltk.sem.chat80 import concepts
from owlready2 import get_ontology

import gensim.downloader as api

from src.ontology_tinder import utils


class UtilsTestCase(unittest.TestCase):

    def test_model_containment(self):
        info = api.info()
        model = api.load(list(info["models"].keys())[0])

        with open(os.path.join("..", "resources", "pruned_names.txt"), "r") as file:
            words = file.read().split("\n")

        contained, not_contained = utils.model_coverage_of_words(model, words)
        print(len(contained)/ len(words))

    def test_direct_match_coverage(self):
        """
        Calculates the overall coverage of direct matches.

        """
        onto = get_ontology("http://www.ease-crc.org/ont/SOMA-HOME.owl").load()

        concepts = [concept.name for concept in onto.classes()]
        with open(os.path.join("..", "resources", "pruned_names.txt"), "r") as file:
            words = file.read().split("\n")
        contained, not_contained = utils.direct_match_coverage_of_words(concepts, words)
        print(100* len(contained)/ len(words))


if __name__ == '__main__':
    unittest.main()
