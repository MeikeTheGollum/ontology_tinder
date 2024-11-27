import unittest

import requests
from owlready2 import get_ontology

import src.ontology_tinder.utils
from src.ontology_tinder.concept_tinder import ConceptTinder


class MinimalConceptNetTestCase(unittest.TestCase):
    ct = ConceptTinder

    @classmethod
    def setUpClass(cls):
        # load the 3 concepts ontology
        # Test ontology in resources folder
        ct = cls.ct
        cls.ct = ConceptTinder(get_ontology(
            "https://raw.githubusercontent.com/MeikeTheGollum/ontology_tinder/refs/heads/main/resources/ontology_tinder_test_1.owl"))

    def test_read_minimal_ontology(self):
        concepts = self.ct.concept_names
        print(concepts)

        self.assertEqual(len(concepts), 3)

    def test_concept_not_found(self):
        obj = self.ct.get_concept_match(self, "appleA")
        self.assertEqual(obj, 404)

    def test_concept_match(self):
        name = "alarmclock"
        obj = self.ct.get_concept_match(self, name)
        self.assertEqual(4, len(obj))
        self.assertEqual('/c/en/alarmclock', obj['@id'])

    def test_concept_matches(self):
        tmp_objs = self.ct.get_concept_matches(self, ["apple", "wall", "alarmclock"])
        id1, id2, id3 = tmp_objs[0]['@id'], tmp_objs[1]['@id'], tmp_objs[2]['@id']
        self.assertEqual('/c/en/apple', id1)
        self.assertEqual('/c/en/wall', id2)
        self.assertEqual('/c/en/alarmclock', id3)
        self.assertEqual(len(tmp_objs), 3)

    def test_get_sources_for_concept(self):
        tmp_objs = self.ct.get_concept_resource(self, "alarmclock")
        self.assertEqual(len(tmp_objs), 6)

    def test_get_sources_for_concepts(self):
        tmp_objs = self.ct.get_concepts_resources(self, ["apple", "wall", "alarmclock"])
        self.assertEqual(len(tmp_objs), 3)
        s1, s2, s3 = tmp_objs[0], tmp_objs[1], tmp_objs[2]
        self.assertEqual(len(s1), 20)
        self.assertEqual(len(s2), 20)
        self.assertEqual(len(s3), 6)  #

    def test_relatedness_of_pair(self):
        val1 = self.ct.get_relatedness_between_concepts(self, "wall", "floor")
        val2 = self.ct.get_relatedness_between_concepts(self, "shelf", "bookcase")

        self.assertEqual(val1, 0.172)
        self.assertEqual(val2, 0.671)

    def test_related_terms(self):
        related_terms = self.ct.get_related_concepts(self, "alarmclock")
        self.assertEqual(len(related_terms), 50)

    def test_no_direct_match(self):
        no_direct_match = self.ct.search_direct_match('Apple')
        self.assertEqual(no_direct_match, None)

    def test_direct_match(self):
        direct_match = self.ct.search_direct_match('wall')
        self.assertEqual(direct_match, 'wall')

    def test_direct_matches(self):
        direct_matches = self.ct.search_direct_matches(["apple", "wall", "alarmclock"])
        c1, c2, c3 = direct_matches[0][1], direct_matches[1][1], direct_matches[2][1]
        self.assertEqual(c1, None)
        self.assertEqual(c2, 'wall')
        self.assertEqual(c3, 'alarmclock')

    def test_coverage_of_direct_matches(self):
        coverage = self.ct.get_coverage(["apple", "beer", "alarmclock"])
        self.assertEqual(coverage, "66.67%")

    def test_most_similar_matches(self):
        related_matches = self.ct.search_most_similar_match("floor")
        c1, c2, c3 = related_matches[0], related_matches[1], related_matches[2]
        self.assertEqual(len(related_matches), 3)
        self.assertEqual(c1[1], ('wall', 0.172))
        self.assertEqual(c2[1], ('dishwasher', 0.07))
        self.assertEqual(c3[1], ('alarmclock', -0.007))

    def test_most_similar_matches_for_list(self):
        related_matches = self.ct.search_most_similar_matches(["wall", "floor", "apple"])
        print(related_matches)

    def test_get_concept_iri_of_direct_match(self):
        test = self.ct.get_concept_uri_of_match("wall")
        print(list(test))
    def test_search_related_terms_in_onto(self):
        related = self.ct.search_most_similar_matches(["floor" , "wall" , "alarmclock"])
        print(related)




class RealLifeTests(unittest.TestCase):
    ct = ConceptTinder
    prunedNames = src.ontology_tinder.utils.read_object_names("pruned_names.txt", "resources")
    notFound = src.ontology_tinder.utils.read_object_names("not_found.txt", "resources")
    @classmethod
    def setUpClass(cls):
        ct = cls.ct
        cls.ct = ConceptTinder("../resources/SOMA_DFL_Module.rdf", get_ontology("file://../resources/SOMA_DFL_Module.rdf"))

    def test_coverage_of_direct_match(self):
        coverage = self.ct.get_coverage(self.prunedNames)
        self.assertEqual(coverage, "5.65%")

    def test_direct_match(self):
        direct_match = self.ct.search_direct_match("Fork")
        self.assertEqual(direct_match, "Fork")

    def test_most_similar_match_direct_match(self):
        direct_match = self.ct.search_most_similar_match("Fork")
        self.assertEqual(direct_match, "Fork")

    def test_most_similar_match(self):
        most_similar = self.ct.search_most_similar_match("designer")
        self.assertEqual(len(most_similar), 5)

    def test_direct_match_no_direct_match(self):
        not_found =  self.ct.search_direct_match("Meike")

    def test_search_related_terms(self):
        lst = self.ct.search_most_similar_match("apple")
        related = self.ct.search_related_terms_in_onto("apple", lst)
        print(related)


    def test_most_similar_matches(self):
        not_found = src.ontology_tinder.utils.read_object_names("not_found.txt", "resources")
        most_similar_matches = self.ct.search_most_similar_matches(self.prunedNames)
        print(most_similar_matches)


    def test_most_similar_matches_for_list(self):
        lst = self.ct.search_most_similar_matches(["mug", "frameshelf", "apple"])

    def test_direct_matches(self):
        direct_matches = self.ct.search_direct_matches(self.prunedNames)
        c1 = [item for item in direct_matches if item[0] == "A-Frameshelf"]
        c2 = [item for item in direct_matches if item[0] == "Fork"]
        self.assertEqual(c1[0][1], None)
        self.assertEqual(c2[0][1], "Fork")
    def test_test(self):
        most_similar = requests.get("http://api.conceptnet.io/query?start=/c/en/mug&rel=/r/RelatedTo&limit=5")

        obj = most_similar.json()
        tmp = [edge['end']['@id'] for edge in obj['edges']]
        test = tmp[0]
        lol=  test.split("c/en/")
        print(lol[1])
        print(most_similar)
        print(obj)
        print(tmp)

    def test_new_related_terms(self):
        res = self.ct.new_related_terms(self.notFound, len(self.notFound))
        


    def test_get_synonym(self):
        syn = self.ct.find_related_term("alarm_clock")


if __name__ == '__main__':
    unittest.main()
