import json
import  pandas as pd
from Kml import KmlCreate
import requests
from datetime import date
import calendar
from sys import argv
from os import remove

def last_day(year,month):
    return calendar.monthrange(int(year),int(month))[1]
class Afad():
    def __init__(self, byear,bmonth,bday,eyear,emonth,eday,min_lat,max_lat,min_lon,max_lon,min_depth,max_depth,min_mag,max_mag):
        self.byear = str(byear)
        self.bmonth = str(bmonth)
        self.bday = str(bday)
        self.eyear = str(eyear)
        self.emonth = str(emonth)
        self.eday = str(eday)
        self.lastday = str(calendar.monthrange(int(self.eyear),int(self.emonth))[1])
        self.min_lat = min_lat
        self.max_lat = max_lat
        self.min_lon = min_lon
        self.max_lon = max_lon
        self.min_depth = min_depth
        self.max_depth = max_depth
        self.min_mag = min_mag
        self.max_mag = max_mag
    def RequestPost(self):
        post_url = "https://deprem.afad.gov.tr/EventData/GetEventsByFilter"
        post_string =  {
            "EventSearchFilterList":[
                {
                    "FilterType": 1, "Value": str(self.min_lat),
                },
                {
                    "FilterType": 2, "Value": str(self.max_lat),
                },
                {
                    "FilterType": 3, "Value": str(self.min_lon),
                },
                {
                    "FilterType": 4, "Value": str(self.max_lon),
                },
                {
                    "FilterType": 6, "Value": str(self.min_depth),
                },
                {
                    "FilterType": 7, "Value": str(self.max_depth),
                },
                {
                    "FilterType": 8, "Value": str(self.byear+"-"+self.bmonth+"-"+self.bday+"T00:00:00.000Z"),
                },
                {
                    "FilterType": 9, "Value": str(self.eyear+"-"+self.emonth+"-"+self.eday+"T23:59:59.999Z"),
                },
                {
                    "FilterType": 11, "Value": str(self.min_mag),
                },
                {
                    "FilterType": 12, "Value": str(self.max_mag),
                }
            ],
            "Skip":0,
            "Take":10000000,
            "SortDescriptor":{
                "field":"eventDate",
                "dir":"desc"
            }
        }   
        post_data = requests.post(url = post_url,data=json.dumps(post_string),headers={'Content-type': 'application/json'})
        return post_data.json()
    def Dataframe(self):
        df =[]
        keys = ["eventDate", "latitude", "longitude", "depth", "magnitude", "location"]
        for i in Afad.RequestPost(self)['eventList']:
            df.append(list(map(i.get,keys)))
        return pd.DataFrame(df)
    def KmlExtract(self):
        return KmlCreate.Create(KmlCreate.Convert(Afad.Dataframe(self)))
def Select(args):
    byear = args[0]
    bmonth = args[1]
    bday = args[2]
    eyear = args[3]
    emonth = args[4]
    eday = args[5]
    blat = args[6]
    elat = args[7]
    blon = args[8]
    elon = args[9]
    bmag = args[10]
    emag = args[11]
    bdepth = args[12]
    edepth = args[13]
    return Afad(str(byear),str(bmonth),str(bday),str(eyear),str(emonth),str(eday),str(blat),str(elat),str(blon),str(elon),str(bdepth),str(edepth),str(bmag),str(emag)).KmlExtract()
def MonthPrint(year,month):
    month = str(month)
    year = str(year)
    lastday = str(last_day(year,month))
    month_length= len(month)
    if month_length != 2:
        month = "0"+month
    return Afad(year,month,"01",year,month,lastday,"0.1","90.0","0.1","180.0","0.1","1000","0.1","10.0").KmlExtract()
def YearPrint(year,month):
    for i in range(1,month+1):
        try:
            print(str(year)+"-"+str(i)+".kml Creating...",end=" ")
            file = open(str(year)+"-"+str(i)+".kml","w",encoding="utf8")
            file.write(MonthPrint(year,i))
            file.close()
            print("Done.")
        except:
            print("Fail!")
            file.close()
            remove(file.name)
            continue
def LastMonth():
    today = date.today()
    year = today.year
    month = today.month
    lastday = str(last_day(year,month))
    return Afad(year,month,"01",year,month,lastday,"0.1","90.0","0.1","180.0","0.1","1000","0.1","10.0").KmlExtract()
if argv[1] == "lastmonth":
    print(LastMonth())
elif argv[1] == "month":
    print(MonthPrint(argv[2],argv[3]))
elif argv[1] == "lastyear":
    year = date.today().year
    month = date.today().month
    YearPrint(year,month)
elif argv[1] == "year_withmonts":
    year = argv[2]
    YearPrint(year,12)
elif argv[1] == "allyear_withmonths":
    byear = argv[2]
    eyear = argv[3]
    year = date.today().year
    for i in range(int(byear),int(eyear)+1):
        YearPrint(i,12)
elif argv[1] == "year":
    cmd = argv[2],"01","01",argv[2],12,31,"0.1","90.0","0.1","180.0","0.1","10.0","0.1","1000"
    file = open(argv[2]+".kml","w",encoding="utf-8")
    file.write(Select(list(cmd)))
    file.close()
elif argv[1] == "allyear":
    byear = argv[2]
    eyear = argv[3]
    for i in range(int(byear),int(eyear)+1):
        cmd = str(i),"01","01",str(i),"12","31","0.1","90.0","0.1","180.0","0.1","10.0","0.1","1000"
        file = open(str(i)+".kml","w",encoding="utf-8")
        try:
            file.write(Select(list(cmd)))
            file.close()
        except:
            file.close()
            remove(file.name)
            continue
elif argv[1] == "alleq":
    today = date.today()
    year = today.year
    month = today.month
    lastday = str(last_day(year,month))
    cmd = "1990","01","01",year,month,lastday,"0.1","90.0","0.1","180.0","0.1","10.0","0.1","1000"
    file = open("AllEQAFAD.kml","w",encoding="utf-8")
    file.write(Select(list(cmd)))
    file.close()
elif argv[1] == "mag5":
    year = date.today().year
    month = date.today().month
    lastday = str(last_day(year,month))
    cmd = "1990","01","01",year,month,lastday,"0.1","90.0","0.1","180.0","5.0","10.0","0.1","1000"
    print(Select(list(cmd)))
else:
    print(Select(argv[1:]))