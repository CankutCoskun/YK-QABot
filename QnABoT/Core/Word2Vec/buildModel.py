'''
#Reads processed tokens from a file called "docs_processed.txt"
#corpus type list of lists of strings [[Str]]

#Built gensim word2vec model, gensim reference: https://radimrehurek.com/gensim/models/word2vec.html
#Gensim is an open source library which is
#Using highly optimized C routines,
#Originally ported from  the C package https://code.google.com/p/word2vec/ and extended with additional functionality and optimizations
#70x speedup compared to plain NumPy implementation (https://rare-technologies.com/parallelizing-word2vec-in-python/).

#Save the model ('/Word2VecModel/myModel')
#Load the model KeyedVectors.load('/Word2VecModel/myModel')

#Visualize the embeddings
#Write the weights (vecs.tsv and meta.tsv )to disk. To use the [Embedding Projector](http://projector.tensorflow.org)

15.08.2019
Cankut Coskun
cankutcoskun@sabanciuniv.edu
'''

import numpy as np
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
import os

#Input: docs (List of list of Strings)
cdir = os.getcwd()
print(cdir)
f = open(cdir + "/docs_processed.txt")
content = f.read()
data = content.split("\n")

#Empty line at the end string.split behaviour
data.pop()

docs = []

for d in data:
    doc = d.split(" ")
    doc.pop()
    docs.append(doc)

##Parameters
# min_count: Ignore words that appear less than this
# size: Dimensionality of word embeddings
# workers: Number of processors (parallelisation)
# window: Context window for words during training
# iter: Number of epochs training over corpus

path = get_tmpfile( cdir + "/word2vec.model")

model = Word2Vec(docs, min_count=1, size=200, workers=4, window=5, iter=100)
word_vectors = model.wv

model.save("word2vec.model")

#Word embedding dimesions
print(model.vector_size)

##Vocabulary
##Vocab size Total number of unique words in model
vocabulary = model.wv.vocab.keys()
vocabulary = list(vocabulary)
size_vocab = len(vocabulary)

#*********Test bench*********
print(model.wv.most_similar('kredi'))
print(model.wv.most_similar_cosmul('dolar', topn = 5))
print(model.wv.most_similar_cosmul('worldcard', topn = 5))

##Get the probability distribution of the center word given context words.
##Returns: topn length list of tuples of (word, probability).
##Return type: list of (str, float)
#model.predict_output_word(["hesap", "kredi", "kart"], topn=10)

##Compute cosine similarity between two sets of words.
model.wv.n_similarity(["ankara","istanbul"], [ "izmir","türkiye"])
model.wv.similarity("ankara","istanbul")

##Embeddings
#print(type(model.wv["ankara"]))
#print(model.wv["ankara"].size)
#print(model.wv["ankara"])

## Next, let's retrieve the word embeddings learned during training. This will be a matrix with shape `(vocab_size,embedding-dimension)`.
embed_list = []
for word in vocabulary:
    embed_list.append(model.wv[word].tolist())

print("Size vocabulary",len(embed_list))
print("Embedding dimensions",len(embed_list[0]))
embeddings = np.array(embed_list)
print(embeddings.shape)
print(embeddings[0])

## Visualize Embeddings
import io

out_v = io.open( cdir + '/tsvFiles/vecs.tsv', 'w', encoding='utf-8')
out_m = io.open(cdir + '/tsvFiles/meta.tsv', 'w', encoding='utf-8')

for idx in range(len(vocabulary)):
    word = vocabulary[idx]
    #print(word)
    weights = embeddings[idx]
    #print(weights)
    #print(len(weights))
    out_m.write(word + "\n")
    out_v.write('\t'.join([str(w) for w in weights]) + "\n")

out_v.close()
out_m.close()

'''

## Visualize the embeddings
#
## We will now write the weights to disk. To use the [Embedding Projector](http://projector.tensorflow.org), we will upload two files in tab separated format: a file of vectors (containing the embedding), and a file of meta data (containing the words).
#
# To visualize our embeddings we will upload them to the embedding projector.
#
# Open the [Embedding Projector](http://projector.tensorflow.org/).
#
# * Click on "Load data".
#
# * Upload the two files we created above: ```vecs.tsv``` and ```meta.tsv```. T

'''
