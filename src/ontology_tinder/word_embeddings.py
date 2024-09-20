#importing necessary models
from gensim.models import Word2Vec
import gensim
from nltk.tokenize import sent_tokenize, word_tokenize
import  warnings
import collector


warnings.filterwarnings(action='ignore')

# Reads current test files
sample1 = open("C:/Users/meike/ontology_tinder/src/files/names.txt")
sample2 = open("C:/Users/meike/ontology_tinder/src/files/names2.txt")

s1 = sample1.read()
s2 = sample2.read()

# Replace escape character with space
f1 = s1.replace("\n", " ")
f2 = s2.replace("\n", " ")

data = []

#iterate through each sentence in the file
for i in sent_tokenize(f1):
    for x in sent_tokenize(f2):
        temp = []
        for j in word_tokenize(i):
            for w in word_tokenize(x):
                temp.append(j.lower())
                temp.append(w.lower())
    data.append(temp)
#print(data)


# Create CBOW model
model1 = gensim.models.Word2Vec(data, min_count = 1, vector_size=100, window=5)
#print(model1)

print(model1.wv.similarity('alarmclock_1', 'agentbody_1'))
print(model1.wv.similarity('alarmclock_1', 'alarmclock_2'))

def get_data():
    return data
def getSimilarity(word1, word2):
    return model1.wv.similarity(word1, word2)