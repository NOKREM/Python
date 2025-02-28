# -*- coding:utf-8 -*-
import json
import time
from Kml2 import *
import requests
from datetime import date
from sys import argv
from os import remove

savefile = KmlGenerator.save_kml

class Afad():
    def __init__(self, byear, bmonth, bday, eyear, emonth, eday, min_lat, max_lat, min_lon, max_lon, min_depth, max_depth, min_mag, max_mag):
        self.start_date = create_date_string(byear, bmonth, bday)
        self.end_date = create_date_string(eyear, emonth, eday, is_start=False)
        self.min_lat, self.max_lat = str(min_lat), str(max_lat)
        self.min_lon, self.max_lon = str(min_lon), str(max_lon)
        self.min_mag, self.max_mag = str(min_mag), str(max_mag)
        self.min_depth, self.max_depth = str(min_depth), str(max_depth)
    def RequestPost(self):
        post_url = "https://deprem.afad.gov.tr/EventData/GetEventsByFilter"
        post_string = {
            "EventSearchFilterList": [
                {"FilterType": 1, "Value": self.min_lat},
                {"FilterType": 2, "Value": self.max_lat},
                {"FilterType": 3, "Value": self.min_lon},
                {"FilterType": 4, "Value": self.max_lon},
                {"FilterType": 6, "Value": self.min_depth},
                {"FilterType": 7, "Value": self.max_depth},
                {"FilterType": 8, "Value": self.start_date},
                {"FilterType": 9, "Value": self.end_date},
                {"FilterType": 11, "Value": self.min_mag},
                {"FilterType": 12, "Value": self.max_mag}
            ],
            "Skip": 0,
            "Take": 10000000,
            "SortDescriptor": {
                "field": "eventDate",
                "dir": "desc"
            }
        }
    
    # Add error handling and retries
        max_retries = 1
        for attempt in range(max_retries):
            try:
                post_data = requests.post(
                    url=post_url,
                    data=json.dumps(post_string),
                    headers={'Content-type': 'application/json; charset=utf-8'},
                    timeout=30  # Add timeout
                )
                post_data.raise_for_status()  # Raise exception for HTTP errors
                return post_data.json()['eventList']
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    # Exponential backoff
                    time.sleep(2 ** attempt)
                    continue
                raise Exception(f"Failed to fetch data after {max_retries} attempts: {e}")
    def parseData(self):
        keys = ["eventDate", "latitude", "longitude", "depth", "magnitude", "location"]
        records = []
        for event in self.RequestPost():
            records.append([event.get(key) for key in keys])
        return records
    def kml_extract(self):
        generator = KmlGenerator()
        kml_content = generator.create_kml(generator.process_data(self.parseData()))
        return kml_content

now = date.today()
year = now.year
month = now.month
day = now.day

def Select(args):
    byear, bmonth, bday, eyear, emonth, eday, blat, elat, blon, elon, bdepth, edepth, bmag, emag = map(str,(args[i] for i in range(0,14,1)))
    return Afad(byear,bmonth,bday,eyear,emonth,eday,blat,elat,blon,elon,bdepth,edepth,bmag,emag).kml_extract()
def MonthPrint(year,month,bmag = 0.1 ,emag = 10.0):
    lastday = last_day(year,month)
    return Afad(year,month,"01",year,month,lastday,"0.1","90.0","0.1","180.0","0.1","1000",bmag,emag).kml_extract()
def YearPrint(year ,bmag = 0.1 ,emag = 10.0):
    savefile(Select([year,"01","01",year,"12","31","0.1","90.0","0.1","180.0","0.1","1000",bmag,emag]),f"AFAD_{year}_{bmag}-{emag}.kml")
def main():
    
    if len(argv) < 2:
        print("Please provide a command argument")
        return
    cmd = argv
    if cmd[1] == "lastmonth":
        savefile(MonthPrint(year,month),f"AFAD_{year}-{str(month).zfill(2)}.kml")
    elif cmd[1] == "lastyear":
        YearPrint(year)
    elif cmd[1] == "year_print" and cmd[2] and cmd[3]:
        YearPrint(cmd[2],cmd[3])
    elif cmd[1] == "month_print" and cmd[2] and cmd[3] and cmd[4]:
        savefile(MonthPrint(cmd[2],cmd[3],cmd[4]),f"AFAD_{cmd[2]}-{str(cmd[3]).zfill(2)}_{cmd[4]}+.kml")
    elif cmd[1] == "allyear" and cmd[2]:
        for i in range(1990,year+1):
            try:
                YearPrint(i,bmag=cmd[2])
            except:
                continue
    elif cmd[1] == "allmonths" and cmd[2] and cmd[3]:
        for i in range(1,13):
            try:
                savefile(MonthPrint(cmd[2],i,cmd[3]),f"AFAD_{cmd[2]}-{str(i).zfill(2)}.kml")
            except:
                continue
if __name__ == "__main__":
    main()