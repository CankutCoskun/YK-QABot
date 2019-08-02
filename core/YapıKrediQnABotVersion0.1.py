### Yapı Kredi QnA BoT version 0.1

#!!!!There are duplicate Quetions and Answers 
#It does not effect te result. It reponses the best match


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import requests

def removeCharacter(list_of_sent , char):
    new_list = []
    for each in list_of_sent:
        to_be_added = each.replace(char, "")
        new_list.append(to_be_added)
    return new_list

def processDocument(path):
    
    PARAMS = {'rawDocPathName': path}
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

        
        
def processInput(raw_inp):
    
    emptyList = []
    
    PARAMS = {'rawInput':raw_inp} 

    response = requests.get("http://localhost:8080/nlpPipeLine/SingleInput", params = PARAMS)
    
    print("Response Code: ", response.status_code)

    if response.status_code == requests.codes.ok:
        text = response.text
        return True, text.rstrip("]").lstrip("[").replace('"','').split(",")
    else:
        return False, emptyList

    
def rankingTable(scores):
    ranking_table = []

    for i in range(len(scores)):
        temp = (i,scores[i])
        ranking_table.append(temp)
        
    return ranking_table

def bestMatchIdx(raw_inp):

    bestMatch_idx = -1
    
    check , inp_tokens = processInput(raw_inp) 
    
    print(inp_tokens)
    
    emptyList = []
    
    if inp_tokens == emptyList:
        return -1
    
    processed_inp = ""
    
    if check:
        processed_inp = " ".join(inp_tokens)
    else:
        return False
    
    processed_questions.append(processed_inp)
    tfidf = vectorizer.fit_transform(processed_questions)
    vals = cosine_similarity(tfidf[-1], tfidf)
    
    processed_questions.pop()
    
    best_match_idx = vals.argsort()[0][-2]
    
    score_list = vals.tolist()[0]
    
    ranking_table = rankingTable(score_list[0:-1])
    
    return best_match_idx

def userInputBestMatch(inp):
    bestIdx = bestMatchIdx(inp)
    print(bestIdx)
    
    if bestIdx == -1:
        print ("Üzgünüm sizi anlayamadım\n")
    else:
        print(questions[bestIdx])
        print(answers[bestIdx])

questions = []
answers = []

f_q = open("questions.txt")
f_a = open("answers.txt")

questions = removeCharacter(f_q.readlines(), "\n")
answers = removeCharacter(f_a.readlines(), "\n")

f_q.close()
f_a.close()

processed_questions = processDocument("./questions.txt")
processed_answers = processDocument("./answers.txt")

##Edge
processed_answers[145] = ""
processed_qnas = []

for i in range(len(processed_questions)):
    qna = processed_questions[i] + " "+processed_answers[i]
    processed_qnas.append(qna)

vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=1.0, min_df = 0, use_idf = True)
bow = vectorizer.fit_transform(processed_qnas)

freqs = [(word, bow.getcol(idx).sum()) for word, idx in vectorizer.vocabulary_.items()]
results = sorted (freqs, key = lambda x: -x[1])
print("Number of unique words (size of dictionary):", len(vectorizer.vocabulary_.items()))

feature_names = vectorizer.get_feature_names()
corpus_index = [n for n in processed_questions]

df = pd.DataFrame(bow.todense(), columns=feature_names)

#( num of questions , size of vocab)
print(df.shape)

df.head(5)


################################################
print("sonlandırmak için lütfen 'çıkış' yazın\n")

inp = input("Ne öğrenmek istersin? \n\n") 

while inp != "çıkış":
    
    userInputBestMatch(inp)
    inp = input("Ne öğrenmek istersin?  \n\n")
                
                

