#!/usr/bin/env python
# coding: utf-8

# In[3]:


from gensim.models import Word2Vec
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
import requests
import operator


# In[2]:


def removeCharacter(list_of_sent , char):
    new_list = []
    for each in list_of_sent:
        to_be_added = each.replace(char, "")
        new_list.append(to_be_added)
    return new_list


# In[4]:


##Upload a pre-trained model 
###Corpus details:
##Retrieved from bloomberght.com 
##Processed with zemberek (nlp tool for Turkish)

model = KeyedVectors.load('/Users/cankutcoskun/Desktop/ChatBotProject/Word2VecModel/myModel')
word_vectors = model.wv


# In[ ]:


vocabulary = list(model.wv.vocab.keys())


# In[9]:


word_vectors.most_similar('kredi')


# In[10]:


model.wv.most_similar('dolar')


# In[51]:


model.wv.most_similar('fon')


# In[54]:


model.wv.most_similar('worldcard')


# In[57]:


model.wv.most_similar('mevduat')


# In[15]:


questions = []
answers = []

f_q = open("/Users/cankutcoskun/Desktop/ChatBotProject/QnA/questions.txt")
f_a = open("/Users/cankutcoskun/Desktop/ChatBotProject/QnA/answers.txt")

questions = removeCharacter(f_q.readlines(), "\n")
answers = removeCharacter(f_a.readlines(), "\n")


f_q.close()
f_a.close()


# In[16]:


print(len(questions),len(answers))


# In[60]:


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
    
        
        return all_tokens

    else:
        raise Exception(" -processDocument() WARNING REQUEST DOES NOT WORK PROPERLY \n response code: " + str(response.status_code))


# In[20]:


processed_questions = processDocument("/Users/cankutcoskun/Desktop/ChatBotProject/QnA/questions.txt")
processed_answers = processDocument("/Users/cankutcoskun/Desktop/ChatBotProject/QnA/answers.txt")
##Edge
processed_answers[145] = []
processed_qnas = [a + b for a, b in zip(processed_questions, processed_answers)]


# In[48]:


def similarity_scores(inp):
    similarity_scores = []
    for idx in range(len(processed_questions)):
        
        try:
            similarity_score = model.wv.n_similarity(processed_qnas[idx], inp)
            similarity_scores.append(similarity_score)
        except:
            print("WARNING EMPTY INPUT")
            
    return similarity_scores


# In[49]:


def checkInputWords(input_tokens):
    returnList = []
    for word in input_tokens:
        if word in vocabulary:
            returnList.append(word)
    return returnList


# In[50]:


def processInput(raw_inp):
    
    emptyList = []
    
    PARAMS = {'rawInput':raw_inp} 

    response = requests.get("http://localhost:8080/nlpPipeLine/SingleInput", params = PARAMS)
    
    print("Response Code: ", response.status_code,"\n")

    if response.status_code == requests.codes.ok:
        text = response.text
        input_tokens = text.rstrip("]").lstrip("[").replace('"','').split(",")
        
        return checkInputWords(input_tokens)
        
    else:
        raise Exception("WARNING EXCEPTION OCCURED processInput()")
        


# In[30]:


def rankingTable(scores):
    ranking_table = []

    for i in range(len(scores)):
        temp = (i,scores[i])
        ranking_table.append(temp)
        
    return ranking_table


# In[40]:


def topResponses(inp):
    processed_input = processInput(inp)
    scores = similarity_scores(processed_input)
    ranking_table = rankingTable(scores)
    ranking_table.sort(key = operator.itemgetter(1),reverse = True)
    topResp = []
    for tup in ranking_table[0:5]:
        idx = tup[0]
        topResp.append(idx)
        #print(tup[1])
    return topResp


# In[47]:


print("Sonlandırmak için lütfen 'çıkış' yazın \n")
inp = input("Ne öğrenmek istersin? \n\n") 

while inp != "çıkış":
    
    ids = topResponses(inp)
    for idx in ids:
        print(idx)
        print(questions[idx])
    #    print(answers[idx])

    inp = input("Ne öğrenmek istersin?  \n\n")
                

