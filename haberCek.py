import os

import pandas as pd
from Haber.Haberturk import Haberturk
from Haber.hurriyet import Hurriyet
from Haber.milli import Milliyet
from Haber.posta import Posta
from Haber.sozcu import Sozcu
from Haber.webtekno import Webtekno
from sql_connector import dbyeYaz, deleteSameLink, keyEkle
import datetime

def deleteSame():
    df1 = pd.read_csv('Haberler.csv', header=None)
    df2 = pd.read_csv('ExHaberler.csv', header=None)
    df1[~df1[1].isin(df2[0])].to_csv('Haberler.csv', header=None, index=None)

def haberCek():
    f = open("Haberler.csv", "w+")
    f.close()
    Webtekno()
    Sozcu()    
    Milliyet()
    Hurriyet()
    Haberturk()
    Posta()
    deleteSame()
    dbyeYaz()
    keyEkle()
    deleteSameLink()

haberCek()