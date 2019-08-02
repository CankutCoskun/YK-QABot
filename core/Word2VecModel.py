#!/usr/bin/env python
# coding: utf-8

# In[1]:


#gensim reference: https://radimrehurek.com/gensim/models/word2vec.html
#https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/soft_cosine_tutorial.ipynb


# In[28]:


import numpy as np
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors


# In[22]:


#Input: docs (List of list)  

f = open("/Users/cankutcoskun/Desktop/ChatBotProject/docs_processed.txt")
content = f.read()
data = content.split("\n")

#Empty line at the end string.split behaviour
data.pop()

docs = []

for d in data:
    doc = d.split(" ")
    doc.pop()
    docs.append(doc)
    


# In[26]:


# min_count: Ignore words that appear less than this
# size: Dimensionality of word embeddings
# workers: Number of processors (parallelisation)
# window: Context window for words during training
# iter: Number of epochs training over corpus

model = Word2Vec(docs, min_count=1, size=200, workers=4, window=5, iter=100)
word_vectors = model.wv
fname = get_tmpfile('/Users/cankutcoskun/Desktop/ChatBotProject/Word2VecModel/myModel')
model.save(fname)

#Word embedding dimesions
model.vector_size


# In[32]:


##Vocabulary
##Vocab size Total number of unique words in model 

vocabulary = model.wv.vocab.keys()
vocabulary = list(vocabulary)
size_vocab = len(vocabulary)


# In[64]:


print(model.wv.most_similar('kredi'))


# In[63]:


print(model.wv.most_similar_cosmul('dolar', topn =15))


# In[62]:


print(model.wv.most_similar_cosmul('worldcard', topn =15))


# In[39]:


##Get the probability distribution of the center word given context words.
##
##Parameters:
##context_words_list (list of str) – List of context words.
##topn (int, optional) – Return topn words and their probabilities.
##
##Returns: topn length list of tuples of (word, probability).
##
##Return type: list of (str, float)
#    
#model.predict_output_word(["hesap", "kredi", "kart"], topn=10)


# In[40]:


##Compute cosine similarity between two sets of words.
#model.wv.n_similarity(["ankara","istanbul"], [ "izmir","türkiye"])
#model.wv.similarity("ankara","istanbul")


# In[66]:


print(model.wv["ankara"])
print(type(model.wv["ankara"]))
print(model.wv["ankara"].size)


# ## Retrieve the learned embeddings
# 
# Next, let's retrieve the word embeddings learned during training. This will be a matrix of shape `(vocab_size,embedding-dimension)`.

# In[67]:


embed_list = []
for word in vocabulary:
    embed_list.append(model.wv[word].tolist())
print("Size vocabulary",len(embed_list))
print("Embedding dimensions",len(embed_list[0]))
embeddings = np.array(embed_list)
print(embeddings.shape)


# In[54]:


embeddings[0]


# ## Visualize Embeddings

# We will now write the weights to disk. To use the [Embedding Projector](http://projector.tensorflow.org), we will upload two files in tab separated format: a file of vectors (containing the embedding), and a file of meta data (containing the words).

# In[56]:


import io

out_v = io.open('/Users/cankutcoskun/Desktop/ChatBotProject/tsvFiles/vecs.tsv', 'w', encoding='utf-8')
out_m = io.open('/Users/cankutcoskun/Desktop/ChatBotProject/tsvFiles/meta.tsv', 'w', encoding='utf-8')

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


# ## Visualize the embeddings
# 
# To visualize our embeddings we will upload them to the embedding projector.
# 
# Open the [Embedding Projector](http://projector.tensorflow.org/).
# 
# * Click on "Load data".
# 
# * Upload the two files we created above: ```vecs.tsv``` and ```meta.tsv```. T
# 
# The embeddings you have trained will now be displayed. You can search for words to find their closest neighbors. For example, try searching for "beautiful". You may see neighbors like "wonderful". Note: your results may be a bit different, depending on how weights were randomly initialized before training the embedding layer.
# 
# Note: experimentally, you may be able to produce more interpretable embeddings by using a simpler model. Try deleting the `Dense(16)` layer, retraining the model, and visualizing the embeddings again.
# 
# <img src="https://github.com/tensorflow/docs/blob/master/site/en/r2/tutorials/text/images/embedding.jpg?raw=1" alt="Screenshot of the embedding projector" width="400"/>
# 
