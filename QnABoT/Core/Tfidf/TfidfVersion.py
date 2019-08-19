
'''
## Yapı Kredi QnA BoT version 0.1

Defintion:
This program is a Question&Answer bot which brings the top 5 best match among a predefined set of questions.

Questions and corresponding answers represented in the same order. Text files are available under the same directory with source code.
	./QnA/questions.txt
	./QnA/answers.txt
Warning!
There are duplicate quetions. This problem might be avoided by checking uniqueness.

Make sure TurkishNlp service is running at localhost port: 8080 for Nlp process.
processInput(), processDocument()

#15.08.2019
#Cankut Coskun
#cankutcoskun@sabanciuniv.edu
#Istanbul/Turkey
'''

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import requests
import os

def delEmpty(list_of_sent):
    new_list = []
    for each in list_of_sent:
        to_be_added = each.replace('\n', "")
        new_list.append(to_be_added)
    return new_list

dirpath = os.getcwd()

print("current directory is : " + dirpath)

questions_path = dirpath + "/QnA/questions.txt"
answers_path = dirpath +"/QnA/answers.txt"

questions = []
answers = []

f_q = open(questions_path)
f_a = open(answers_path)

questions = delEmpty(f_q.readlines())
answers = delEmpty(f_a.readlines())

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

        processed_doc = []
        for tks in all_tokens:
            temp = " ".join(tks)
            processed_doc.append(temp)

        return processed_doc

    else:
        raise Exception("WARNING REQUEST DOES NOT WORK PROPERLY \n response code: " + str(response.status_code))

processed_questions = processDocument(questions_path)
processed_answers = processDocument(answers_path)
##Edge
processed_answers[145] = ""

##Comibe questions and answers to retrieve semantically more relevant atomic units.
processed_qnas = []
for i in range(len(processed_questions)):
    qna = processed_questions[i] + " "+processed_answers[i]
    processed_qnas.append(qna)

## tf-idf Vectors
## bag of words structure
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=1.0, min_df = 0, use_idf = True)
bow = vectorizer.fit_transform(processed_questions)

freqs = [(word, bow.getcol(idx).sum()) for word, idx in vectorizer.vocabulary_.items()]
results = sorted (freqs, key = lambda x: -x[1])
print("Number of unique words (size of dictionary):", len(vectorizer.vocabulary_.items()))

feature_names = vectorizer.get_feature_names()
corpus_index = [n for n in processed_questions]

df = pd.DataFrame(bow.todense(), columns=feature_names)

#( num of questions , size of vocab)
print(df.shape)
print(df.head(5))

def processInput(raw_inp):

    emptyList = []
    PARAMS = {'rawInput':raw_inp}
    response = requests.get("http://localhost:8080/nlpPipeLine/singleInput", params = PARAMS)
    print("Response Code: ", response.status_code)

    if response.status_code == requests.codes.ok:
        text = response.text
        return text.rstrip("]").lstrip("[").replace('"','').split(",")
    else:
        raise Exception("Request does not respond error code: ", response.status_code)

def bestMatchIds(raw_inp):

    bestMatch_ids = []
    inp_tokens = processInput(raw_inp)
    print(inp_tokens)

    if len(inp_tokens)== 0:
        print("Üzgünüm sizi anlayamadım")

    processed_inp = " ".join(inp_tokens)
    processed_questions.append(processed_inp)

    tfidf = vectorizer.fit_transform(processed_questions)
    processed_questions.pop()
    vals = cosine_similarity(tfidf[-1], tfidf)
    vals = vals[0]


    best_match_ids = list(vals.argsort())

    return best_match_ids[-6:-1]

def main():

    print("sonlandırmak için lütfen 'çıkış' yazın\n")
    inp = input("Ne öğrenmek istersin? \n\n")

    while inp != "çıkış":
        ids = bestMatchIds(inp)
        for idx in reversed(ids):
            print("\n" + questions[idx] + "\n")
            print(answers[idx],"\n")
            print("*****************")
        inp = input("\nNe öğrenmek istersin?  \n\n")
        print()

if __name__ == "__main__":
    main()
