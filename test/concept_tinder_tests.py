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
if __name__ == '__main__':
    unittest.main()
