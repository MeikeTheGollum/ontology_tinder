from functools import cached_property
from typing import List, Dict

import owlready2
import requests
import typing_extensions
from owlready2 import Ontology
from requests import Response
from typing import Any


class ConceptTinder:

    def hello(self):
        print("Hello")

    def get_concept_matches(self, names: List[str]) -> List[Dict]:
        """
        Collects the API responses from conceptnet for a given list of strings
        :param names: list of names
        :return: List of API responses
        """
        tmp_objs = [requests.get(f"http://api.conceptnet.io/c/en/{x}").json() for x in names]

        return tmp_objs

    def get_concept_match(self, name: str) -> Dict | int:
        """
        Returns the API response of a given name.
        :param name: name
        :return: API response
        """
        obj = requests.get(f"http://api.conceptnet.io/c/en/{name}").json()
        if len(obj['edges']) == 0:
            return obj['error']['status']
        return obj

    def get_concept_resource(self, name:str) -> Dict:
        """
        Returns the resources from a concept given a name.
        :param name: name
        :return: The resources associated with the name in ConceptNet
        """
        tmp = requests.get(f"http://api.conceptnet.io/c/en/{name}").json()
        obj = [x.get('sources') for x in tmp['edges']]
        return obj

    def get_concepts_resources(self, names: List[str]) -> List[Any]:
        """
        Returns the resources from concepts given a list of names.
        :param names: List of names
        :return: The resources associated with the list
        """
        result =[]
        tmps = [requests.get(f"http://api.conceptnet.io/c/en/{name}").json() for name in names]
        for objs in tmps:
            result.append([entry.get('sources') for entry in objs['edges']])
        return result


    def get_relatedness_between_concepts(self, name1: str, name2:str) -> float:
        """
        Returns the relatedness value for a given pair of names.
        :param name1: First name
        :param name2: Second name
        :return: Value of relatedness
        """
        obj = requests.get(f"http://api.conceptnet.io//relatedness?node1=/c/en/{name1}&node2=/c/en/{name2}").json()
        return obj['value']
    def get_related_concepts(self, name:str) -> Dict:
        """
        Returns all related concepts of a name.
        :param name: The name
        :return: The related terms
        """
        tmp = requests.get(f"http://api.conceptnet.io/related/c/en/{name}").json()
        return tmp['related']
