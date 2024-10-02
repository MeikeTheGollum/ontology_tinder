import unittest

from owlready2 import get_ontology

from ontology_tinder.ontology_tinder import OntologyTinder


#
# class WordEmbeddingsTestCase(unittest.TestCase):
#
#     def test_getSimilarity(self):
#         self.assertEqual(word_embeddings.getSimilarity('alarmclock_1', 'alarmclock_1'), 1.0)


class MinimalOntologyTinderTestCase(unittest.TestCase):

    ot: OntologyTinder

    @classmethod
    def setUpClass(cls):
        # load the 3 concepts ontology
        # Test ontology in resources folder
        cls.ot = OntologyTinder(get_ontology("https://raw.githubusercontent.com/MeikeTheGollum/ontology_tinder/refs/heads/main/resources/ontology_tinder_test_1.owl"))

    def test_concept_embeddings(self):
        concept_embeddings = self.ot.concept_embeddings
        self.assertEqual(len(concept_embeddings), 3)

    def test_ontology_tinder_single_names(self):
        most_similar_concepts = self.ot.most_similar_concept_of_names(["alarmclock"], 3)
        self.assertEqual(len(most_similar_concepts), 1)

        alarm_clock_similarity = most_similar_concepts["alarmclock"]

        self.assertEqual(len(alarm_clock_similarity), 3)
        concepts = [c for c,_ in alarm_clock_similarity]
        self.assertEqual(set(concepts), set(self.ot.ontology.classes()))

    def test_get_closest_concept_of_name(self):
        similar_concept = self.ot.closest_concept_of_name("clock")
        self.assertEqual(similar_concept.name, "alarmclock")


class OntologyTinderTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ot = OntologyTinder(get_ontology("https://raw.githubusercontent.com/ease-crc/soma/refs/heads/master/owl/SOMA-HOME.owl"))

    def test_ontology_tinder(self):
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
