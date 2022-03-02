with open('news.txt',"w+", encoding='utf-8') as text_file:
                text_file.write("abcds")
                text_file.seek(0)
                metin = text_file.read()
                print(metin)