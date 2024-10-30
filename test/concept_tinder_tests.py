import os
import unittest
import sys
import requests
from owlready2 import get_ontology

from src.ontology_tinder import concept_tinder, collector

import gensim.downloader as api

from src.ontology_tinder import concept_tinder
from src.ontology_tinder.concept_tinder import ConceptTinder


class MinimalConceptNetTestCase(unittest.TestCase):
    ct = ConceptTinder

    @classmethod
    def setUpClass(cls):
        # load the 3 concepts ontology
        # Test ontology in resources folder
        ct = cls.ct
        cls.ct = ConceptTinder(get_ontology("https://raw.githubusercontent.com/MeikeTheGollum/ontology_tinder/refs/heads/main/resources/ontology_tinder_test_1.owl"))

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
        tmp_objs = self.ct.get_concept_matches(self,["apple", "wall", "alarmclock"])
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
        self.assertEqual(len(s3), 6)#

    def test_relatedness_of_pair(self):
        val1 = self.ct.get_relatedness_between_concepts(self, "wall", "floor")
        val2 = self.ct.get_relatedness_between_concepts(self, "shelf", "bookcase")

        self.assertEqual(val1, 0.172)
        self.assertEqual(val2, 0.671)

    def test_related_terms(self):
        related_terms = self.ct.get_related_concepts(self, "alarmclock")
        self.assertEqual(len(related_terms), 50)

    def test_no_direct_match(self):
        no_direct_match= self.ct.search_direct_match('Apple')
        self.assertEqual(no_direct_match, None)

    def test_direct_match(self):
        direct_match= self.ct.search_direct_match('wall')
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
if __name__ == '__main__':
    unittest.main()
