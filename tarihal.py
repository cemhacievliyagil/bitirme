from datetime import datetime,timedelta
def tarihal(string):
  txt = datetime.strptime(string, "%Y-%m-%d").strftime("%d-%m-%Y")
  tarih = datetime.fromisoformat(txt).date()
  return (tarih)
#tarihal("15-02-2022")