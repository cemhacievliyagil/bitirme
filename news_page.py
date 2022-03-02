from gensim.models import KeyedVectors
from gensim.test.utils import common_texts
from gensim.models import Word2Vec
import gensim.downloader as api
word_vectors = KeyedVectors.load_word2vec_format('trmodel', binary=True)


def calculate_it(numInt):
    v = word_vectors.word_vec(numInt)
    kategoriler = ['Gündem', 'Siyaset','Ekonomi','Dünya','Magazin','Otomobil','Teknoloji','Eğitim','Spor','Futbol','Basketbol', 'Kültür-Sanat', 'Yaşam', 'Sağlık', 'Bilim']
    results = []
    v = word_vectors.most_similar(v)
    for x in v :
       results.append(x[0])
    for y in results:
       if(numInt == y):
          results.remove(y)
    return  (results)
    
        
        