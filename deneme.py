# coding=utf-8
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
#from TurkishStemmer import TurkishStemmer
import torch
import time
from datetime import datetime
from zeyrek import MorphAnalyzer
import lemmatizer
#-*- coding: utf-8 -*-
time.sleep(3)
#stemmer = TurkishStemmer()
with open('news.txt', encoding='utf-8') as text_file:
        doc1 = text_file.read()
n_gram_range = (2, 2)
stop = []
"""with open('turkce-stop-words.txt', encoding='utf-8') as file:  
    stw = file.read() 
stw = stw.split()
stw = [s.lower() for s in stw] 
stop += stw
def modelprocess(doc):
 tokenizer = AutoTokenizer.from_pretrained('distiluse-base-multilingual-cased-v1')
 normalizer = text_normalization.TextNormalization()
 normalized_text = normalizer.normalize(doc, do_lower_case=True, is_turkish=True)
 tokenizer.tokenize(normalized_text)
 print(normalized_text)
 return normalized_text"""


model = SentenceTransformer('distiluse-base-multilingual-cased-v1')
#model.load_state_dict(torch.load('./model.pth'))
#model.eval()
torch.save(model.state_dict(), 'model4.pth')
def funct(doc1):
 #count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop).fit([doc])
 #candidates = count.get_feature_names_out()
 #analyzer = MorphAnalyzer()
#print(candidates)
 candidates = lemmatizer.run_examples(doc1) 
 #print(candidates)
 for i in lemmatizer.extract_specials(doc1):
  candidates.append(i)
 candidates = list(dict.fromkeys(candidates))
 wordset = set(candidates)
 candidates = [item for item in wordset if item.istitle() or item.title() not in wordset]
 print("ADAYLAR: ")
 print(candidates)

 doc_embedding = model.encode([doc1])
 candidate_embeddings = model.encode(candidates)
 top_n = 10
 distances = cosine_similarity(doc_embedding, candidate_embeddings)
#print(distances)
 keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]
 keywords = list(dict.fromkeys(keywords))
 #print(keywords)
 keywordsx = keywords[-8:]
 for i in keywordsx:
    print((i))
 return keywordsx
#doc2 = modelprocess(doc1)
funct(doc1)