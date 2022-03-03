# coding=utf-8
import re
from numpy import digitize
from zeyrek import MorphAnalyzer
from collections import OrderedDict
import nltk
from transformers import AutoTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity
import os
from datetime import datetime
from zeyrek import MorphAnalyzer
from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer
import os
os.environ["JAVA_HOME"] = "D:\Java\jdk-15.0.1"
#nltk.download('punkt')
stop = []
analyzer = MorphAnalyzer()
def run_examples(text):
 words = []
 with open('turkce-stop-words.txt','r', encoding='utf-8') as file:  
    stop = [line.strip() for line in file]
 dizix = []

    # Analyze text from the file and print out formatted parses of each word.
 result = analyzer.analyze(text)
 for word_result in result:
        for parse in word_result:
            if((parse.morphemes[0] == 'Noun') and (parse.word not in stop)and (parse.word not in words)):
                 words.append(analyzer.lemmatize(parse.word)[0][1])
                 dizix.append(parse.word)
 
 dizi = []
 dizi1 = []
 dizi = OrderedDict((tuple(x), x) for x in words).values()
 for eleman in dizi:
     for kucukeleman in eleman:
         #print(kucukeleman)
         dizi1.append(kucukeleman)
         resultx= (analyzer.analyze(kucukeleman))
         for a in resultx:
          for b in a:
           if(b.morphemes[0] == "Verb" and kucukeleman in dizi1):
              dizi1.remove(kucukeleman)
           else:
               continue
 return (dizi1)
 #print(dizix)
with open('news.txt', encoding='utf-8') as text_file:
        text = text_file.read()
#run_examples(text)
"""resultx= (analyzer.analyze("Ali Yerlikaya"))
for a in resultx:
    for b in a:
        print(b)
        if(b.morphemes[0] == "Verb"):
         print(False)"""
punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

def extract_specials(stringx):
 model = AutoModelForTokenClassification.from_pretrained("savasy/bert-base-turkish-ner-cased")
 tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-ner-cased")
 ner=pipeline('ner', model=model, tokenizer=tokenizer)
 #stringx = ("""İstanbul Valisi Ali Yerlikaya, kentteki yoğun kar yağışı ve buzlanma nedeniyle bir sonraki duyuruya kadar motokuryelik yapılmayacağını, motosiklet ve elektrikli scooterların kullanılmayacağını bildirdi.İstanbul Valisi Ali Yerlikaya, kentteki yoğun kar yağışı ve buzlanma nedeniyle bir sonraki duyuruya kadar motokuryelik yapılmayacağını, motosiklet ve elektrikli scooterların kullanılmayacağını bildirdi.Vali Yerlikaya, sosyal medya hesabından yaptığı açıklamada, "İstanbul’daki yoğun kar yağışı ve buzlanma nedeniyle trafik seyir ve can güvenliğini sağlamak için bir sonraki duyuruya kadar motokuryelik yapılmayacak, motosiklet ve elektrikli scooterlar kullanılmayacaktır." ifadelerini kullandı.İstanbul'da Kasım ayındaki fırtınada 15 Temmuz Şehitler Köprüsü'nde ilerlemeye çalışan moto kuryelerin görüntüsü hafızalara kazınmıştı. Görüntülerdeki kuryelere metrobüsler refakat etmişti ancak pek çok noktada hem kuryeler hem de diğer iki tekerli araç kullananlar büyük güçlük çekmişti. """)
 ner_list = ner(stringx)
 this_name = []
 all_names_list_tmp = []
 
 final_list = []
 ner_list2 = []
 ner_list3 = []
 for i in ner_list:
     if(i['word'] in ner_list2):
         continue
     else:
         ner_list2.append(i['word'])
         ner_list3.append(i)
 
 for ner_dict in ner_list3:
    if ner_dict['entity'] == 'B-ORG':
        if len(this_name) == 0:
            this_name.append(ner_dict['word'])
        else:
            all_names_list_tmp.append([this_name])
            this_name = []
            this_name.append(ner_dict['word'])
    elif ner_dict['entity'] == 'I-ORG':
        this_name.append(ner_dict['word'])

#all_names_list_tmp1.append([this_name])
 print(ner_list3)
 for ner_dict in ner_list3:
    if ner_dict['entity'] == 'B-PER':
        if len(this_name) == 0:
            this_name.append(ner_dict['word'])
        else:
            all_names_list_tmp.append([this_name])
            this_name = []
            this_name.append(ner_dict['word'])
    elif ner_dict['entity'] == 'I-PER':
        this_name.append(ner_dict['word'])
    elif ner_dict['entity'] == 'B-LOC':
        final_list.append([ner_dict['word']])

 all_names_list_tmp.append([this_name])
 final_list3 = []
 final_list4=[]
 for name_list in all_names_list_tmp:
    full_name = ' '.join(name_list[0]).replace(' ##', '').replace(' .', '.')
    final_list.append([full_name])
    final_list1 = OrderedDict((tuple(x), x) for x in final_list).values()
    final_list2 = []
    for i in final_list1:
      final_list2.append(i)
 for j in final_list2:
     final_list3.append(j[0])
 for k in final_list3:
        k=re.sub(r'[^\w\s]', '', k)
        final_list4.append(k)
 if ("Covid-19" in text )or ("covid-19 " in text) or ("COVİD-19" in text):
    final_list4.append("covid-19")
 print(final_list4)
 
 return(final_list4)
#extract_specials(text)

