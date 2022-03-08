from datetime import datetime,timedelta
def tarihal(string):
  txt = datetime.strptime(string, "%Y-%m-%d").strftime("%d-%m-%Y")
  #tarih = datetime.fromisoformat(txt).date()
  print(txt)
  return (txt)
tarihal("2022-02-24")