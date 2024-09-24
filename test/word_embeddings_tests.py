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

    def test_ontology_tinder_single_name(self):
        most_similar_concepts = self.ot.most_similar_concept_of_name("alarmclock")
        # because we test against an ontology with three entries, only 2 of them can be
        # most similar to the one name
        self.assertEqual(len(most_similar_concepts), 2)
        c1, c2 = most_similar_concepts

        # useful comparisons here
        self.assertEqual(c1, ('dishwasher', -0.02367166429758072))
        self.assertEqual(c2, ('wall', -0.052346739917993546))
    def test_ontology_tinder_list_names(self):
        most_similar_concepts = self.ot.most_similar_concept_of_names(["alarmclock", "wall"])
        self.assertEqual(len(most_similar_concepts), 2)
        c1, c2 = most_similar_concepts
        self.assertEqual(c1[0], ('dishwasher', -0.02367166429758072) )
        self.assertEqual(c1[1], ('wall', -0.052346739917993546) )
        self.assertEqual(c2[0], ('dishwasher', -0.010839177295565605))
        self.assertEqual(c2[1], ('alarmclock', -0.05234673619270325))

    def test_ontology_tinder_single_name_closest(self):
        closest_match = self.ot.closest_concept_of_name("wall")
        self.assertEqual(len([closest_match]), 1)
        c1 = closest_match
        self.assertEqual(c1, ('dishwasher', -0.010839177295565605))

    def test_ontology_tinder_list_names_closest(self):
        closest_matches = self.ot.closest_concept_of_names(["alarmclock", "wall"])
        self.assertEqual(len(closest_matches), 2)
        c1, c2 = closest_matches
        self.assertEqual(c1, ('dishwasher', -0.02367166429758072))
        self.assertEqual(c2, ('dishwasher', -0.010839177295565605))

class OntologyTinderTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ot = OntologyTinder(get_ontology("https://raw.githubusercontent.com/ease-crc/soma/refs/heads/master/owl/SOMA-HOME.owl"))

    def test_ontology_tinder(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
