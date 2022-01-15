from transformers import AutoModel, AutoTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import text
from sentence_transformers import SentenceTransformer
import nltk
import text_normalization
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from TurkishStemmer import TurkishStemmer
import torch
import os
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from datetime import datetime
import time
from datetime import datetime, timedelta

time.sleep(3)
stemmer = TurkishStemmer()
output_model = 'C:\\Users\\ollia\\Desktop\\bitirme\\model_for_keyword'
doc1 = """
4/a ve 4/b kapsamında sigortalı kadınlara veya eşi çalışmayan sigortalı erkek çalışanlara, doğum sonrası çocuğun yaşaması halinde emzirme ödeneği veriliyor. Emzirme ödeneği, kendi çalışmalarından dolayı SGK’dan gelir veya aylık alan kadınlar veya erkeğin sigortalı olmayan eşine de ödeniyor. 2021 yılında 232 TL olan emzirme ödeneği 2022 yılında 316 TL’ye çıkartıldı. Emzirme ödeneğinden yararlanabilmek için doğumdan önceki 120 gün sigorta primi bildirilmiş (4/b’liler için primin ödenmiş) olması gerekiyor. """
n_gram_range = (1, 1)
stop = stopwords.words('Turkish')
with open('turkce-stop-words.txt', encoding='utf-8') as file:  
    stw = file.read() 
stw = stw.split()
stw = [s.lower() for s in stw] 
stop += stw
#def modelprocess():
 #tokenizer = AutoTokenizer.from_pretrained('dbmdz/bert-base-turkish-128k-cased')
 #normalizer = text_normalization.TextNormalization()
 #normalized_text = normalizer.normalize(doc, do_lower_case=True, is_turkish=True)

#tokenizer.tokenize(normalized_text)
model = SentenceTransformer('dbmdz/bert-base-turkish-128k-cased')
#model.load_state_dict(torch.load('./model.pth'))
#model.eval()
#torch.save(model.state_dict(), 'model4.pth')
def funct(doc):
 count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop).fit([doc])
 candidates = count.get_feature_names_out()
 doc_embedding = model.encode([doc])
 candidate_embeddings = model.encode(candidates)
 top_n = 5
 distances = cosine_similarity(doc_embedding, candidate_embeddings)
 keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]
 for i in keywords:
      print(stemmer.stem(i))