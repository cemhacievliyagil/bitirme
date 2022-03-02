def kisaltmalar():
    liste = []
    file = open("kısaltmalar.txt",encoding="utf-8")
    temp = file.read().splitlines()
    for line in temp:
            fields = line.split("\t")
            liste.append(fields)
    return liste