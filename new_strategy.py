from keybert import KeyBERT
from flair.embeddings import TransformerDocumentEmbeddings
from nltk.corpus import stopwords
from transformers import AutoModel, AutoTokenizer
import text_normalization
from TurkishStemmer import TurkishStemmer
roberta = TransformerDocumentEmbeddings('dbmdz/bert-base-turkish-cased')
kw_model = KeyBERT(model=roberta)
stemmer = TurkishStemmer()

doc = """
Fenerbahçe, Spor Toto Süper Lig'in 20. haftasında 1-0 öne geçtiği maçta Adana Demirspor'a 2-1 mağlup oldu.
İrfan Can'ın ortasında Valencia'nın yerde kalması sonrasında Halil Umut Meler beyaz noktayı gösterdi. Valencia 4,5 ay sonra gol atarken Fenerbahçe'yi de 1-0 öne geçirdi.
Adana Demirspor, Yunus Akgün'ün pasında Gökhan İnler'in harika şutuyla skora dengeyi getirdi ve ilk yarı 1-1 sonuçlandı.
İkinci yarının hemen başlarında Kaan Kanak'ın uzun pasında Belhanda yaptığı tek vuruşla Adana Demirspor'u 2-1'lik üstünlüğe taşıdı. Kalan dakikalarda gol olmayınca Adana Demirspor, İstanbul'da 33 yıl sonra rakibini mağlup etti.
20 hafta sonunda 9 galibiyet 5 beraberlikte kalan Fenerbahçe, lider Trabzonspor'un da 17 puan gerisine düştü. Sarı-lacivertliler ayrıca bu sezon evinde ikinci kez kaybetti.
      """
stop = stopwords.words('Turkish')
with open('turkce-stop-words.txt', encoding='utf-8') as file:  
    stw = file.read() 
stw = stw.split()
stw = [s.lower() for s in stw] 
stop += stw


tokenizer = AutoTokenizer.from_pretrained('dbmdz/bert-base-turkish-cased')
normalizer = text_normalization.TextNormalization()
normalized_text = normalizer.normalize(doc, do_lower_case=True, is_turkish=True)

tokenizer.tokenize(normalized_text)



keywords = kw_model.extract_keywords(normalized_text, keyphrase_ngram_range=(1, 1), stop_words=stop)

for i in keywords:
      print(stemmer.stem(i))


