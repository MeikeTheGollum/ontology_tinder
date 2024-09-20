import gensim
from owlready2 import *
import rdflib
from rdflib import Literal
import inspect
from gensim import *
from gensim.models import Word2Vec
import word_embeddings



onto = get_ontology("file://C:/Users/meike/ontology_tinder/src/resources/SOMA_home.owl").load()
graph = default_world.as_rdflib_graph()
# DUL = Namespace("http://www.ease-crc.org/ont/")
# graph.bind("DUL", DUL)

names = []
def search_instances_in_loaded_ontology():
    search_query = """SELECT DISTINCT ?s WHERE{
    ?s ?o ?p.
    }
    """
    res = graph.query(search_query)
    for row in res:
        print(row.s)

def get_names():
    print("Hello")
    search_query = """
prefix dul:<http://www.ontologydesignpatterns.org/ont/dul/DUL.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX soma: <http://www.ontologydesignpatterns.org/ont/SOMA.owl#>

select ?entity where {
?entity rdfs:subClassOf* dul:DesignedArtifact.
 

}


    """
    print("Im finished")
    res = graph.query(search_query)
    for r in res:
        print(r[0])
        names.append(r[0])
    return res

def prepare_result_for_vector():
    clipped_names = []
    for name in names:
        tmp = name.split("#")
        clipped_names.append(tmp[1])
    vector = word2Vec(clipped_names)

    print(vector)
    return vector

#Word2Vec.train(sentences, total_words=None, word_count=0, total_examples=None, queue_factor=2, report_delay=1.0)[

def ProcessedSetting():
    processed_sentences = [i for i in word_embeddings.get_data()]
    words_model = Word2Vec(
        sentences=processed_sentences,
        min_count=10,  # Purning the internal dictionary
        vector_size=200,  # the number of dimensions (N) gensim maps the word onto
        window=2,  # Define when two words are together, 2 means, 2 words left and 2 words right
        compute_loss=True,
        sg=1
    )

    training_loss = words_model.get_latest_training_loss()
    print(f"Training Loss: {training_loss}")
    for w, sim in words_model.wv.most_similar('alarmclock_1'):
        print((w,sim))
# Suche nach einzelnen Strings und Liste
def word2Vec(data):
    tmp = gensim.models.Word2Vec(data, min_count=1, vector_size=100, window=5)
    tmp2 = word_embeddings.get_data()
    test = gensim.models.Word2Vec(tmp2, min_count=1, vector_size=100, window=5)
    haha = test.wv.most_similar(positive=['alarmclock_2'], topn=10 )
    for w, sim in test.wv.most_similar('clock'):
        print((w,sim))
    #print(haha)
    #test = tmp.wv.most_similar(positive=['alarmclock_1'], topn=5)
   # print(test)
    return tmp