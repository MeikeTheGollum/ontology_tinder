from cgitb import reset
from collections import Counter
from functools import cached_property
from typing import List, Dict, Literal, Tuple, Optional

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

    file : str
    ontology: Ontology
    graph = default_world.as_rdflib_graph()

    def __init__(self, file: str, ontology: Ontology):
        self.file = file
        g = Graph()
        g.parse(f"{file}")
        self.ontology = ontology
        self.ontology.load(g)


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
            concept = self.concept_names[tmp]
            if tmp is None:
                self.search_related_terms_in_onto(name, self.search_most_similar_match(name))
            else:
                print(concept)
               # self.write_into_matches("found", name, concept)
                return concept
        except ValueError:
            return None

    def write_into_matches(self, type: str, name: str, tmp: Optional = str):
        if type == "found":
            with open("../resources/found.txt", 'a') as file:
                print("I want to write")
                file.write(f"{name}, {tmp}\n")
        elif type == "not found":
            with open("../resources/not_found.txt", 'a') as file:
                file.write(f"{name}, {tmp}\n")
        elif type == "related":
            with open("../resources/found_related_term.txt", 'a') as file:
                file.write(f"{name}, {tmp}\n")
        elif type == "no_related":
            with open("../resources/no_related_terms_found.txt", 'a') as file:
                file.write(f"{name}\n")


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
        tmp_name = name.lower()
        if name in self.concept_names:
            return self.concept_names[self.concept_names.index(name)]
        else:
            most_similar = requests.get(f'http://api.conceptnet.io/query?start=/c/en/{name}&rel=/r/RelatedTo&limit=5')
            obj = most_similar.json()
            tmp = [x['end']['@id'].split("c/en/")[1] for x in obj['edges']]
            return tmp



    def search_most_similar_matches(self, names: List[str]) :
        tmp = [self.search_most_similar_match(name) for name in names]
        res = [self.search_related_terms_in_onto(name, n) for n in tmp for name in names]
        print("This is a result: " + str(res))
        return res


    def search_related_terms_in_onto(self, name: str, related: Dict[(str, float)]):
        """
        Searches for related terms in a given ontology.
        :param name: The name
        :param related: The related terms
        :return: match
        """

        print(type(related))

        related_terms = [x[0] for x in related]
        tmp = self.search_direct_matches( related_terms)
        print(tmp)
        for t in tmp:
            if t[1] is None:
                self.write_into_matches("not_found", name)
            else:
                self.write_into_matches("related", name, t[1])
        return tmp


    def get_concept_uri_of_match(self, name: str):
        search_query = """SELECT DISTINCT ?x WHERE{
           ?x rdfs:label ?s.
           }
           """
        res = self.graph.query(search_query, initBindings={"s": rdflib.term.Literal(name)})
        return res

    def get_coverage(self, names: List[str]):
        """
        Calculates the overall coverage given a list of names and the loaded ontology.

        :param names: The list of strings
        :return: Coverage in percentage as a string
        """
        direct_matches = self.search_direct_matches(names)
        for n in direct_matches:
            if n[1] is None:
                with open("../resources/not_found.txt", 'a') as file:
                    file.write(f"{n[0]}\n")
            else:
                with open("../resources/found.txt", 'a') as file:
                    file.write(f"{n[0]}, {n[1]}\n")
        tmp = Counter(elem[1] == None for elem in direct_matches)
        print(tmp)
        percentage = 100* float(tmp[False]) / float(len(direct_matches))
        return str(round(percentage, 2)) + "%"

    def check_direct_matches(self, related: List[str]):
        return None

    def get_synonyms(self, name: str) -> List[str]:
        synonyms = requests.get(f"https://api.conceptnet.io/c/en/{name.lower()}?rel=/r/Synonym&limit=10")
        obj = synonyms.json()
        print(obj)
        if len(obj['edges']) != 0:
            tmp = [x['end']['@id'].split("/")[len(x['end']['@id'].split("/"))-1] for x in obj['edges']]
            for m in tmp:
                print(self.find_related_term(m))
            return tmp
        else :
            return None

    def find_related_term(self, name: str):
        related_terms = requests.get(f"https://api.conceptnet.io/c/en/{name}?rel=/r/IsA&limit=10").json()
        print(related_terms)

    def new_related_terms(self, names: List[str], badge_size: int):
        """
        Writes into pre-specified txt files with found or not found related terms in a given ontology.
        :param names: List of strings that need related terms
        :return:
        """
        if badge_size <1:
            badge_size = len(names)

        i = 0

        while i <= badge_size:
            not_found = []
            name = names[i]
            print(name)
            related_terms = requests.get(f'http://api.conceptnet.io/query?start=/c/en/{name.lower()}&rel=/r/RelatedTo&limit=5?filter=/c/en')
            obj = related_terms.json()

            print(name + str(obj['edges']))
            if len(obj['edges']) == 0:
                #try_synonym = self.get_synonyms(name)
                #if try_synonym is None:
                self.write_into_matches("no_related", name)
                i += 1
                continue
            tmp =  [x['end']['@id'].split("/")[len(x['end']['@id'].split("/"))-1] for x in obj['edges']]
            tmp_weight = [x['weight'] for x in obj['edges']]
            upper_tmp = [x.title() for x in tmp]
            results = self.search_direct_matches(upper_tmp)
            res_tmp = Counter(elem[1] is None for elem in results)
            rel_term = []
            print(not_found)
            for m in results:
                if m[1] is None:
                    continue
                else:
                    print("m", m[1])
                    print(tmp_weight)
                    rel_term.append(m[1])

            if len(rel_term) > 0:
                tmp_rel_term = list(map(lambda  x, y : (x,y), rel_term, tmp_weight))
                self.write_into_matches("related", name,tmp_rel_term)
            elif len(rel_term) == 0:
                #syn = self.get_synonyms(name)
                #if syn is None:
                 #   self.write_into_matches("no_related", name)
                #else:
                 #   syn_res = self.search_direct_matches(syn)
                  #  res_tmp_syn = []
                   # for w in syn_res:
                    #    if w[1] is None:
                     #       continue
                      #  else:
                       #     res_tmp_syn.append(w[1])
                    #if len(res_tmp_syn) > 0:
                     #   self.write_into_matches("related", name,res_tmp_syn)
                    #else:
                self.write_into_matches("no_related", name)

            i+=1


