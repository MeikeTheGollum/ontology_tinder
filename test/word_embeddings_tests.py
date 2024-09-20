import unittest

from owlready2 import get_ontology

from ontology_tinder.ontology_tinder import OntologyTinder
from src.ontology_tinder import word_embeddings


class WordEmbeddingsTestCase(unittest.TestCase):

    def test_getSimilarity(self):
        self.assertEqual(word_embeddings.getSimilarity('alarmclock_1', 'alarmclock_1'), 1.0)


class OntologyTinderTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ot = OntologyTinder(get_ontology("https://raw.githubusercontent.com/ease-crc/soma/refs/heads/master/owl/SOMA-HOME.owl"))

    def test_ontology_tinder(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
