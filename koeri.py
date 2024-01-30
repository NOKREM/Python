import requests
from lxml import html
import pandas as pd
import re
from kml import *
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
        # Veri girişi
        veri = requests.get("http://www.koeri.boun.edu.tr/scripts/lst0.asp") ; veri.encoding = "cp1254"
        # Satırları böl
        satirlar = str(veri.text).strip().split('\n')
        pmag = []
        main_data = []
        # Her bir satırı işle
        for satir in satirlar:
            # Düzenli ifade kullanarak ayrıştırma
            eslesme = re.match(r'(\d{4}.\d{2}.\d{2} \d{2}:\d{2}:\d{2})\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(-\.-|\d+\.\d+)\s*(-\.-|\d+\.\d+)\s*(-\.-|\d+\.\d+)\s*(.*)', satir)    
            if eslesme:
                date = eslesme.group(1)
                lat = eslesme.group(2)
                long = eslesme.group(3)
                depth = eslesme.group(4)
                md = eslesme.group(5)
                ml = eslesme.group(6)
                mw = eslesme.group(7)
                if mw == "-.-":
                    pmag = ml
                else:
                    pmag = mw
                loc = eslesme.group(8).split()
                if loc[-1] == "İlksel":
                    del loc[-1]
                else:
                    del loc[-1]
                    del loc[-1]
                    del loc[-1]
                loc = " ".join(loc)
                main_data += [[date,lat,long,depth,pmag,loc]]
        df = pd.DataFrame(main_data) 
        return Create(Convert(pd.DataFrame(df)))
    def month_print(year,month):
        url = KOERI().monthprint_url.format(year,month)
        body = requests.get(url)
        body.encoding = "cp1254"
        tree = ET.fromstring(body.text)
        data = []
        myorder = [0, 1, 3, 4, 6, 5, 2]
        for items in tree.findall(KOERI().xml_tree):
            arr = list(items.attrib.values())
            arr[0] = re.sub(' ','\t',arr[0])
            data.append('\t'.join(arr))
        for i in range(len(data)):
            data[i]=data[i].split('\t')
            data[i] = [data[i][j] for j in myorder]
        for i in range(len(data)):
            data[i][0] += " "+data[i][1]
            if data[i][5] == "-.-":
                data[i][5] = 0.0
            del data[i][1]
        return Create(Convert(pd.DataFrame(data)))
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
        data = requests.get(url+params)
        data.encoding = "cp1254"
        html = BeautifulSoup(data.text, "lxml").decode(KOERI().codepage)
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
        return Create(Convert(pd.DataFrame(match)))
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
    outFile(str(sys.argv[2])+"-"+sys.argv[3]+".kml",KOERI.month_print(sys.argv[2],sys.argv[3]))
elif sys.argv[1] == "lasteq":
    outFile("lasteq.kml",KOERI.lasteq())
elif sys.argv[1] == "zeqdb":
    outFile("zeqdb.kml",KOERI.zeqdb(sys.argv[2]))
elif sys.argv[1] == "zeqdb_monthprint":
    year = sys.argv[2]
    month = sys.argv[3]
    outFile(str(year)+"-"+str(month)+"_ZEQDB.kml",KOERI.zeqdb(str(year)+"-"+str(month)+"-01 "+str(year)+"-"+str(month)+"-"+str(last_day(year,month))+" 28.50-50.00 18.00-50.00 0-9 0-500"))
elif sys.argv[1] == "allyear":
    KOERI.all_month_print()
elif sys.argv[1] == "allzeqdb":
    KOERI.allzeqdb()
"""
    ZEQDB
    For Example
    koeri.py zeqdb "2023-01-01 2023-01-31 28.50-50.00 18.00-50.00 0-9 0-500"
"""
