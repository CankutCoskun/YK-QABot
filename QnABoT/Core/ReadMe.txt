Yapi Kredi Question&Answer Bot:

Project Definition:
Yk Q&A bot answers customer questions related to products or services provided by Yapı Kredi Bank. The output will be selected among a set of predefined answers(Data obtained from FAQ page of yapıkredi website: https://www.yapikredi.com.tr/memnuniyetiniz-icin-buradayiz/sikca-sorulan-sorular/ ) 

Following versions are available:
1-)Tf-idf based keyword search
2-)Word2vec based Semantic search 

Technical details:

Questions and corresponding answers represented in the same order. Text files are available at: 
 ./QnA/questions.txt
 ./QnA/answers.txt

!Warning!
There are duplicate quetions due to source of data. This problem might be avoided by checking uniqueness. Since it does not affect the robustness of this program, I simply ignored! 

Make sure TurkishNlp service is running at localhost port: 8080 for Nlp.
Methods calling service: processInput(), processDocument()


Ps:Methodologies are documented in detail under the specified directories.

Cankut Coskun
cankutcoskun@sabanciuniv.edu
19.08.2019 
Istanbul/Turkey
