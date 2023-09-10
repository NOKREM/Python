from urllib.request import urlopen
import pandas as pd
import re
from Kml import KmlCreate
import xml.etree.ElementTree as ET
import sys
from bs4 import BeautifulSoup

class KOERI:
    def __init__(self):
        self.lastquake_url = "http://www.koeri.boun.edu.tr/scripts/lst9.asp"
        self.monthprint_url = "http://udim.koeri.boun.edu.tr/zeqmap/xmlt/{}{}.xml"
        self.zeqdb_url = "http://www.koeri.boun.edu.tr/sismo/zeqdb/submitRecSearchT.asp?"
        self.zeqdb_params = "bYear={}&bMont={}&bDay={}&eYear={}&eMont={}&eDay={}&EnMin={}&EnMax={}&BoyMin={}&BoyMax={}&MAGMin={}&MAGMax={}&DerMin={}&DerMax={}&Tip=DepremDeprem&ofName={}{}{}_{}{}{}_{}_{}.txt"
        self.xml_tree = "earhquake"
        self.codepage = "cp1254"
    def lasteq():
        url =KOERI().lastquake_url
        body = urlopen(url).read().decode(KOERI().codepage)
        match = re.findall('(\n[0-9]{3}.*İlksel\r|\n[0-9]{3}.*REVIZE.*\r)', body)
        data = []
        for i in match: data.append(i.split())
        for i in range(len(data)):
            data[i][0] += "T" + data[i][1]
            del data[i][7]
            del data[i][5]
            del data[i][1]
            for j in range(5,len(data[i])):
                data[i][5] += data[i][j]
            for j in range(6,len(data[i])):
                try:
                    del data[i][j]
                except:
                    del data[i][6]
        return KmlCreate.Create(KmlCreate.Convert(pd.DataFrame(data)))
    def month_print(year,month):
        url = KOERI().monthprint_url.format(year,month)
        body = urlopen(url).read().decode(KOERI().codepage)
        tree = ET.fromstring(body)
        data = []
        myorder = [0, 1, 3, 4, 6, 5, 2]
        for items in tree.findall(KOERI().xml_tree):
            arr = list(items.attrib.values())
            arr[0] = re.sub(' ','\t',arr[0])
            data.append('\t'.join(arr))
        for i in range(len(data)):
            data[i]=re.sub(' ','',data[i]).split('\t')
            data[i] = [data[i][j] for j in myorder]
        for i in range(len(data)):
            data[i][0] += "T"+data[i][1]
            if data[i][5] == "-.-":
                data[i][5] = 0.0
            del data[i][1]
        return KmlCreate.Create(KmlCreate.Convert(pd.DataFrame(data)))
    def zeqdb(params):
        parse_params = params.split(" ")
        begin_date = parse_params[0].split("-")
        end_date = parse_params[1].split("-")
        latitude = parse_params[2].split("-")
        longitude = parse_params[3].split("-")
        magnitude = parse_params[4].split("-")
        depth = parse_params[5].split("-")
        begin_year = begin_date[0] ; begin_month = begin_date[1] ; begin_day = begin_date[2]
        end_year = end_date[0] ; end_month = end_date[1] ; end_day = end_date[2]
        begin_lat = latitude[0] ; end_lat = latitude[1]
        begin_lon = longitude[0] ; end_lon = longitude[1]
        begin_mag = magnitude[0] ; end_mag = magnitude[1]
        begin_depth = depth[0] ; end_depth = depth[1]
        url = KOERI().zeqdb_url
        params = KOERI().zeqdb_params.format(
            begin_year,begin_month,begin_day,
            end_year, end_month, end_day,
            begin_lat, end_lat, begin_lon, end_lon,
            begin_mag, end_mag, begin_depth, end_depth,
            begin_year, begin_month, begin_day,
            end_year, end_month, end_day,
            begin_mag, end_mag
        )
        data = urlopen(url+params).read().decode(KOERI().codepage)
        html = BeautifulSoup(data, "lxml").decode(KOERI().codepage)
        match = re.findall("[0-9]{6}\t.*",html)
        for i in range(len(match)):
            match[i] = match[i].split("\t")
        for i in range(len(match)):
            for j in range(13,7,-1):
                del match[i][j]
            del match[i][1]
            del match[i][0]
            match[i][0]+="T"+match[i][1]
            del match[i][1]
        return KmlCreate.Create(KmlCreate.Convert(pd.DataFrame(match)))

    def all_month_print():
        for i in range(2003, 2024):
            for j in range(1, 13):
                file = open(str(i) + "_"+str(j) + ".kml", "w")
                if j < 10:
                    file.write(KOERI.month_print(i, "0"+str(j)))
                    file.close()
                else:
                    file.write(KOERI.month_print(i, j))
                    file.close()
    def allzeqdb():
        for i in range(1900, 2013):
            file = open(str(i)+"_ZEQDB.kml","w")
            file.write(KOERI.zeqdb(str(i)+"-01-01 "+str(i) + "-12-31 "+"28-50 "+"18-50 "+"0-9 "+"0-500"))
            file.close()
if sys.argv[1] == "month_print":
    print(KOERI.month_print(sys.argv[2],sys.argv[3]))
elif sys.argv[1] == "lasteq":
    print(KOERI.lasteq())
elif sys.argv[1] == "zeqdb":
    print(KOERI.zeqdb(sys.argv[2]))
elif sys.argv[1] == "allyear":
    KOERI.all_month_print()
elif sys.argv[1] == "allzeqdb":
    KOERI.allzeqdb()
"""
    ZEQDB
    For Example
    koeri.py zeqdb "2023-01-01 2023-01-31 28.50-50.00 18.00-50.00 0-9 0-500"
"""
