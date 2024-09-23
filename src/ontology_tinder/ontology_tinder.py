from functools import cached_property

import owlready2
from owlready2 import Ontology
from gensim.models import Word2Vec
import nltk
#from typing_extensions import List, Any, Dict
import typing_extensions

class OntologyTinder:

    ontology: Ontology

    def __init__(self, ontology: Ontology):
        self.ontology = ontology
        self.ontology.load()

    @cached_property
    def concept_embeddings(self) -> typing_extensions.Dict[owlready2.Thing, typing_extensions.Any]:
        """
        Calculate the embeddings for all concepts in the ontology.

        TODO Check that this generates the desired dictionary

        :return: The embeddings for all concepts
        """
        data = []

        for concept in self.ontology.classes():
            data.append(concept.name.split("_"))
        print(data)
        model = Word2Vec(data, min_count=1, vector_size=100, window=5)
        print(model)
        word_vectors = model.wv
        # tmp = {concept: model.wv[concept.name.split("_")[0]] for concept in self.ontology.classes
        #         if concept.name.split("_")[0] in model}
        return word_vectors

    def most_similar_concept_of_name(self, name: str) -> typing_extensions.List[owlready2.Thing]:
        """
        Find the most similar concepts for a given string in the ontology.
        This uses a word embedding model for all concepts and the name to calculate the most similar concept.
        :param name: The name
        :return: The most similar concepts
        """
        # convert the name to a token
        #model = Word2Vec[name]
        vector = self.concept_embeddings[name]

        # compare with tokens from self.concept_embeddings
        result = self.concept_embeddings.most_similar(positive=name)
        print(result)
        return result

    def most_similar_concept_of_names(self, names: typing_extensions.List[str]) -> typing_extensions.List[owlready2.Thing]:
        """
        Find the most similar concepts for a list of names in the ontology.
        This uses a word embedding model for all concepts and the name to calculate the most similar concept.

        :param names: The names
        :return: The most similar concepts
        """

        # convert the names to tokens
        model1 = Word2Vec(names, min_count=1, vector_size=100, window=5)

        # compare with tokens from self.concept_embeddings
        result = [self.concept_embeddings.most_similar(positive=name) for name in names ]
        # return the most similar concepts
        print(result)
        return result
