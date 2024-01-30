# -*- coding:utf-8 -*-
import json
import  pandas as pd
from kml import *
import requests
from datetime import date
from sys import argv
from os import remove


class Afad():
    def __init__(self, byear,bmonth,bday,eyear,emonth,eday,min_lat,max_lat,min_lon,max_lon,min_depth,max_depth,min_mag,max_mag):
        self.start_date = create_date_string(byear,bmonth,bday)
        self.end_date = create_date_string(eyear,emonth,eday,is_start=False)
        self.min_lat, self.max_lat, self.min_lon, self.max_lon = map(str, [min_lat, max_lat, min_lon, max_lon])
        self.min_mag, self.max_mag, self.min_depth, self.max_depth = map(str, [min_mag, max_mag, min_depth ,max_depth])
    def RequestPost(self):
        post_url = "https://deprem.afad.gov.tr/EventData/GetEventsByFilter"
        #queries = [ self.min_lat, self.max_lat, self.min_lon, self.max_lon, self.min_depth, self.max_depth, self.start_date, self.end_date, self.min_mag, self.max_mag ]
        post_string = {
            "EventSearchFilterList": [
                {
                    "FilterType": 1, "Value": self.min_lat,
                },
                {
                    "FilterType": 2, "Value": self.max_lat,
                },
                {
                    "FilterType": 3, "Value": self.min_lon,
                },
                {
                    "FilterType": 4, "Value": self.max_lon,
                },
                {
                    "FilterType": 6, "Value": self.min_depth,
                },
                {
                    "FilterType": 7, "Value": self.max_depth,
                },
                {
                    "FilterType": 8, "Value": self.start_date,
                },
                {
                    "FilterType": 9, "Value": self.end_date,
                },
                {
                    "FilterType": 11, "Value": self.min_mag,
                },
                {
                    "FilterType": 12, "Value": self.max_mag,
                }
            ],
            "Skip":0,
            "Take":10000000,
            "SortDescriptor":{
                "field":"eventDate",
                "dir":"desc"
            }
        }
        post_data = requests.post(url = post_url,data=json.dumps(post_string),headers={'Content-type': 'application/json; charset=utf-8'})
        return post_data.json()
    def Dataframe(self):
        df =[]
        keys = ["eventDate", "latitude", "longitude", "depth", "magnitude", "location"]
        for i in Afad.RequestPost(self)['eventList']:
            df.append(list(map(i.get,keys)))
        return pd.DataFrame(df)
    def KmlExtract(self):
        return Create(Convert(Afad.Dataframe(self)))
def Select(args):
    byear, bmonth, bday, eyear, emonth, eday, blat, elat, blon, elon, bmag, emag, bdepth, edepth = map(str,(args[i] for i in range(0,14,1)))
    return Afad(byear,bmonth,bday,eyear,emonth,eday,blat,elat,blon,elon,bdepth,edepth,bmag,emag).KmlExtract()
def MonthPrint(year,month):
    lastday = last_day(year,month)
    return Afad(year,month,"01",year,month,lastday,"0.1","90.0","0.1","180.0","0.1","1000","0.1","10.0").KmlExtract()
def YearPrint(year,month):
    for i in range(1,int(month)+1):
        try:
            print(f"{year}-{str(i).zfill(2)}.kml Creating...",end=" ")
            outFile(f"{year}-{str(i).zfill(2)}.kml",MonthPrint(year,i))
            print("Done.")
        except:
            print("Fail!")
            file.close()
            remove(file.name)
            continue
def LastMonth():
    today = date.today()
    return MonthPrint(today.year,today.month)
today = date.today()
year = str(today.year)
month =str(today.month)
day = str(today.day)
lastday = last_day(year,month)
if argv[1] == "lastmonth":
    outFile(f"{year}-{month.zfill(2)}.kml",LastMonth())
elif argv[1] == "lastyear":
    YearPrint(year,month)
elif argv[1] == "lastday":
    cmd = year,month,today.day,year,month,today.day,"0.1","90.0","0.1","180.0","0.1","10.0","0.1","1000"
    outFile(f"{year}-{month.zfill(2)}-{day.zfill(2)}.kml",Select(cmd))
elif argv[1] == "month":
    outFile(f"{str(argv[2])}-{str(argv[3]).zfill(2)}.kml",MonthPrint(argv[2],argv[3]))
elif argv[1] == "year_allmonths":
    YearPrint(argv[2],12)
elif argv[1] == "allyear_allmonths":
    byear = argv[2]
    eyear = argv[3]
    for i in range(int(byear),int(eyear)+1):
        YearPrint(i,12) 
elif argv[1] == "year":
    cmd = argv[2],"01","01",argv[2],12,31,"0.1","90.0","0.1","180.0","0.1","10.0","0.1","1000"
    outFile(argv[2]+".kml",Select(list(cmd)))
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
    cmd = "1990","01","01",year,month,lastday,"0.1","90.0","0.1","180.0","0.1","10.0","0.1","1000"
    outFile("AllEQAFAD.kml",Select(list(cmd)))
elif argv[1] == "mag5":
    cmd = "1990","01","01",year,month,lastday,"0.1","90.0","0.1","180.0","5.0","10.0","0.1","1000"
    outFile("mag5.kml",Select(list(cmd)))
elif argv[1] == "mag4":
    cmd = "1990","01","01",year,month,lastday,"0.1","90.0","0.1","180.0","4.0","10.0","0.1","1000"
    outFile("mag4.kml",Select(list(cmd)))
else:
    print(Select(argv[1:]))