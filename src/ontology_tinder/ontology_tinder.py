from owlready2 import Ontology


class OntologyTinder:

    ontology: Ontology

    def __init__(self, ontology: Ontology):
        self.ontology = ontology
        self.ontology.load()