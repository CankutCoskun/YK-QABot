
Yapı Kredi QnA BoT version 0.1

Defintion:
This program is a Question&Answer bot which brings the top 5 best match among a predefined set of questions using a search engine based on Tf-idf Approach. 

Methodology:

1-)Build an inverted index structure. This provides the basis for efficient query processing.

ex:

term1 occurs in {d1, d5, d6, d11, . . .},
term2 occurs in {d11, d23, d59, d84, . . .}, and
term3 occurs in {d1, d4, d11, d19, . . .}.


2-)To allow ranked retrieval create a term document matrix with TF-IDF weight:

Term frequency - inverse document frequency" (Tf-idf):

TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document).

IDF(t) = log_e(Total number of documents / Number of documents with term t in it)

Tf-idf weights = tf(t) * idf(t):

Matrix shape: (num of questions , size of vocab):
 
ex:	
corpus includes 2 documents: "love programming", "programming also love" 
 

			also		love		programming

love programming	0.000000	0.707107	0.707107
programming also love	0.704909	0.501549	0.501549


All questions and user input converted to n dimensional vectors <vocab size>.

3-)Ranking:
Cosine similarity is a metric used to determine how similar the documents are irrespective of their size.
Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space.


