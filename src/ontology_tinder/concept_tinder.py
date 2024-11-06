from cgitb import reset
from collections import Counter
from functools import cached_property
from typing import List, Dict, Literal

import rdflib
from rdflib import Graph, Literal
import compose
import owlready2
import requests
import typing_extensions
from nltk.sem.chat80 import concepts
from owlready2 import Ontology, default_world
from requests import Response
from typing import Any
from operator import itemgetter

class ConceptTinder:

    ontology: Ontology
    graph = default_world.as_rdflib_graph()

    def __init__(self, ontology: Ontology):
        self.ontology = ontology
        self.ontology.load()


    @cached_property
    def concept_names(self) -> List[str]:
        return [concept.name for concept in self.ontology.classes()]

    @cached_property
    def class_names(self) -> List[str]:

        return [concept for concept in self.ontology.classes()]
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

    def search_direct_match(self, name: str) -> None | str:
        """
        Searches for direct match for a string in a given ontology. If a direct match is found
        the method returns the concept or a bool if no direct match was found.
        :param name: The name
        :return: Direct match or False if no direct match was found

        """
        try:
            tmp = self.concept_names.index(name)
            return self.concept_names[tmp]
        except ValueError:
            return None



    def search_direct_matches(self, names:List[str]):
        """
        Searches for direct matches for a list of strings in a given ontology. If a direct match is found
        for a string entry, the method appends a tuple (name, concept) to the return.
        If no direct match is found, the method returns (name, none).

        :param names: List of names
        :return: Direct match or None if no direct match was found
        """
        return [(name, self.search_direct_match(name)) for name in names]

    def search_most_similar_match(self, name: str) -> (str, (str, float) ):
        """
        Retrieves the most similar match for a given string in a given ontology.
        :param name: The name
        :return: The most similar match
        """
        results = []
        if name in self.concept_names:
            return self.concept_names[self.concept_names.index(name)]

        for entry in self.concept_names:
            relateness = requests.get(f"http://api.conceptnet.io//relatedness?node1=/c/en/{name}&node2=/c/en/{entry}").json()
            print(relateness)

            if relateness['value'] >= 0.5:
                print(relateness['value'])
                results.append((name, (entry, relateness['value'])))
        return sorted(results, key=compose.compose(itemgetter(1), itemgetter(0)))

    def search_most_similar_matches(self, names: List[str]) :
        return [[self.search_most_similar_match(name) for name in names]]

    def get_concept_uri_of_match(self, name: str):
        search_query = """SELECT DISTINCT ?x WHERE{
           ?x rdfs:label ?s.
           }
           """
        res = self.graph.query(search_query, initBindings={"s": rdflib.term.Literal(name)})
        return res

    def get_coverage(self, names: List[str]):
        """
        Caclulates the overal covergafe given a list of names and the loaded ontology.

        :param names: The list of strings
        :return: Coverage in percentage as a string
        """
        direct_matches = self.search_direct_matches(names)
        tmp = Counter(elem[1] == None for elem in direct_matches)
        percentage = 100* float(tmp[True]) / float(len(direct_matches))
        return str(round(percentage, 2)) + "%"


    def filter_concepts_by_namespace(self, namespace:str):
        filtered = []

        filtered = self.ontology.search( type =namespace)
        return filtered
