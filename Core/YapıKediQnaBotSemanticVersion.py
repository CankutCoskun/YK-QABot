
'''
15.08.2019
Cankut Coskun
cankutcoskun@sabanciuniv.edu

## Yapı Kredi QnA BoT version 0.2
# Semantic search using a word2vec embeddings
# Each wordvector is represented as a point in a 200 dimensional hyperspace

###Corpus details:
##Financial news retrieved from bloomberght.com
##Processed with zemberek (nlp tool for Turkish) ( https://github.com/ahmetaa/zemberek-nlp )
##Make sure TurkishNlp service is running at localhost port: 8080

#Cosine similarity is a metric used to determine how similar the documents are irrespective of their size.
#Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space.
#The cosine similarity is advantageous because even if the two similar documents are far apart by the Euclidean distance because of the size
#they could still have a smaller angle between them. Smaller the angle, higher the similarity.

'''
from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
import requests
import operator

questions_path = "/Users/cankutcoskun/Desktop/SummerInternshipProject/Core/QnA/questions.txt"
answers_path = "/Users/cankutcoskun/Desktop/SummerInternshipProject/Core/QnA/answers.txt"

##Load a pre-trained model
model = KeyedVectors.load('/Users/cankutcoskun/Desktop/SummerInternshipProject/Core/Word2VecModel/myModel')
word_vectors = model.wv
##Initiliaze vocabulary
vocabulary = list(model.wv.vocab.keys())


def removeCharacter(list_of_sent , char):
    new_list = []
    for each in list_of_sent:
        to_be_added = each.replace(char, "")
        new_list.append(to_be_added)
    return new_list

questions = []
answers = []
f_q = open(questions_path)
f_a = open(answers_path)
questions = removeCharacter(f_q.readlines(), "\n")
answers = removeCharacter(f_a.readlines(), "\n")

f_q.close()
f_a.close()

def processDocument(path):

    PARAMS = {'docPathName': path}
    response = requests.get("http://localhost:8080/nlpPipeLine/document", params = PARAMS)

    if response.status_code == requests.codes.ok:
        resp_text = response.text
        resp_list = resp_text.rstrip("]").lstrip("[").replace('"','').split("],[")

        all_tokens = []

        for r in resp_list:
            tokens = r.split(",")
            all_tokens.append(tokens)


        return all_tokens

    else:
        raise Exception("WARNING REQUEST DOES NOT WORK PROPERLY \n response code: " + str(response.status_code))

#Compute cosine similarity between two sets of words.
def similarity_scores(inp):
    similarity_scores = []
    for idx in range(len(processed_questions)):

        try:
            similarity_score = model.wv.n_similarity(processed_qnas[idx], inp)
            similarity_scores.append(similarity_score)
        except:
            print("WARNING EMPTY INPUT")

    return similarity_scores

def checkInputWords(input_tokens):
    returnList = []
    for word in input_tokens:
        if word in vocabulary:
            returnList.append(word)
    return returnList

def processInput(raw_inp):

    emptyList = []

    PARAMS = {'rawInput':raw_inp}

    response = requests.get("http://localhost:8080/nlpPipeLine/singleInput", params = PARAMS)

    print("Response Code: ", response.status_code,"\n")

    if response.status_code == requests.codes.ok:
        text = response.text
        input_tokens = text.rstrip("]").lstrip("[").replace('"','').split(",")
        return checkInputWords(input_tokens)

    else:
        raise Exception("WARNING REQUEST ERROR ")

def rankingTable(scores):
    ranking_table = []

    for i in range(len(scores)):
        temp = (i,scores[i])
        ranking_table.append(temp)

    return ranking_table

def topResponses(inp):
    processed_input = processInput(inp)
    scores = similarity_scores(processed_input)
    ranking_table = rankingTable(scores)
    ranking_table.sort(key = operator.itemgetter(1),reverse = True)
    topResp = []
    for tup in ranking_table[0:5]:
        idx = tup[0]
        topResp.append(idx)

    return topResp

processed_questions = processDocument(questions_path)
processed_answers = processDocument(answers_path)
##Edge ??
processed_answers[145] =[]

##Comibe questions and answers to retrieve semantically more relevant atomic units.
processed_qnas = [a + b for a, b in zip(processed_questions, processed_answers)]

def main():
    print("Sonlandırmak için lütfen 'çıkış' yazın \n")
    inp = input("Ne öğrenmek istersin? \n\n")
    while inp != "çıkış":
        ids = topResponses(inp)
        for idx in ids:
            print(idx)
            print(questions[idx])
            print(answers[idx])

        inp = input("Ne öğrenmek istersin?  \n\n")

if __name__ == "__main__":
    main()
