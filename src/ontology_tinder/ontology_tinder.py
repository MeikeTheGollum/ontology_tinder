from functools import cached_property

import owlready2
from gensim.models import Word2Vec, KeyedVectors
import gensim.downloader
from owlready2 import Ontology
from typing_extensions import List, Dict, Tuple, Optional


def prune_name(name: str):
    return name.split("_")[0]

class OntologyTinder:
    ontology: Ontology

    _concept_embeddings: Optional[KeyedVectors] = None

    def __init__(self, ontology: Ontology):
        self.ontology = ontology
        self.ontology.load()

    def matching_concepts_by_name(self, name: str) -> List[owlready2.Thing]:
        return [concept for concept in self.ontology.classes() if concept.name.split("_")[0] == name]

    def matching_concept_by_name(self, name: str) -> owlready2.Thing:
        result = self.matching_concepts_by_name(name)
        if len(result) == 0:
            raise ValueError(f"No concept found for name {name}")
        elif len(result) > 1:
            raise ValueError(f"Multiple concepts found for name {name}. Concepts found: {result}")
        return self.matching_concepts_by_name(name)[0]

    @cached_property
    def concept_names(self) -> List[str]:
        return [concept.name for concept in self.ontology.classes()]

    @property
    def concept_embeddings(self) -> KeyedVectors:
        """
        Calculate the embeddings for all concepts in the ontology.

        :return: The embeddings for all concepts
        """
        if not self._concept_embeddings:
            data = [[name] for name in self.concept_names]
            model = Word2Vec(data, min_count=1, vector_size=100, window=5)
            self._concept_embeddings = model.wv
        return self._concept_embeddings

    @concept_embeddings.setter
    def concept_embeddings(self, value: KeyedVectors):
        self._concept_embeddings = value

    def expand_vocabulary(self, new_words: List[str]):
        """
        TODO
        """
        data = self.concept_names + new_words
        data = [[name] for name in data]
        model = Word2Vec(data, min_count=1, vector_size=100, window=5)
        return model.wv

    def most_similar_concept_of_names(self, names: List[str], top_n: int=5) -> Dict[str, Tuple[owlready2.Thing, float]]:
        """
        Find the most similar concepts for a list of names in the ontology.
        This uses a word embedding model for all concepts and the name to calculate the most similar concept.

        :param names: The names
        :param top_n: The number of most similar concepts to return
        :return: The most similar concepts
        """
        new_names = [name for name in names if name not in self.concept_embeddings.key_to_index.keys()]

        if len(new_names) > 0:
            word_vectors = self.expand_vocabulary(new_names)
        else:
            word_vectors = self.concept_embeddings

        result = dict()
        for name in names:
            current_result = [(concept, 1.) for concept in self.matching_concepts_by_name(name)]
            match_by_embedding = word_vectors.most_similar(positive=[name], topn=top_n)
            print(match_by_embedding)
            current_result.extend([(self.matching_concept_by_name(name), score) for name, score in
                                   match_by_embedding[:top_n - len(current_result)]])
            result[name] = current_result
        return result

    def closest_concept_of_name(self, name: str) -> owlready2.Thing:
        """
        Get the closest concept for a given name.

        :param name: The name
        :return: The most likely concept
        """
        result = self.most_similar_concept_of_names([name])
        return result[name][0][0]



