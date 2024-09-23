import unittest

from owlready2 import get_ontology

from src.ontology_tinder.ontology_tinder import OntologyTinder
#from src.ontology_tinder import ontology_tinder.OntologyTinder
from src.ontology_tinder import word_embeddings


class WordEmbeddingsTestCase(unittest.TestCase):

    def test_getSimilarity(self):
        self.assertEqual(word_embeddings.getSimilarity('alarmclock_1', 'alarmclock_1'), 1.0)


class MinimalOntologyTinderTestCase(unittest.TestCase):
    # TODO Create an ontology that has 3 concepts

    ot: OntologyTinder

    @classmethod
    def setUpClass(cls):
        # load the 3 concepts ontology
        # Test ontology in resources folder
        cls.ot = OntologyTinder(get_ontology("https://raw.githubusercontent.com/MeikeTheGollum/ontology_tinder/refs/heads/main/resources/ontology_tinder_test_1.owl"))

    def test_concept_embeddings(self):
        concept_embeddings = self.ot.concept_embeddings
        self.assertEqual(len(concept_embeddings), 3)

    def test_ontology_tinder(self):
        most_similar_concepts = self.ot.most_similar_concept_of_name(["alarmclock", "wall", "dishwasher"])
        self.assertEqual(len(most_similar_concepts), 3)
        c1, c2, c3 = most_similar_concepts

        # useful comparisons here
        self.assertEqual(c1, None)


class OntologyTinderTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ot = OntologyTinder(get_ontology("https://raw.githubusercontent.com/ease-crc/soma/refs/heads/master/owl/SOMA-HOME.owl"))

    def test_ontology_tinder(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
