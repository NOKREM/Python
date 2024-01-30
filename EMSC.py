from kml import *
import json
import pandas as pd
import requests

emsc_url = "https://seismicportal.eu/fdsnws/event/1/query"
ahead_url = "https://www.emidius.eu/fdsnws/event/1/query"
query_params = {"start":{},"end":{},
    "minlat":{},"maxlat":{},"minlon":{},"maxlon":{},
    "mindepth":{},"maxdepth":{},"minmag":{},"maxmag":{},
    "lat":{},"lon":{},"minradius":{},"maxradius":{},
    "magtype":{},"limit":"1000000",
    "format":"json","nodata":"404"}
def parseJson(jdata,depth=True,region=False):
    features = jdata["features"]
    main_data = []
    for feature in features:
        time = feature["properties"]["time"]
        lat = feature["properties"]["lat"]
        lon = feature["properties"]["lon"]
        if depth:
            depth = feature["properties"]["depth"]
        mag = feature["properties"]["mag"]
        if region:
            flynn_region = feature["properties"]["flynn_region"] + " " + feature["properties"]["region"]
        else:
            flynn_region = feature["properties"]["flynn_region"]
        main_data += [[time, lat, lon, depth, mag, flynn_region]]
    return main_data
def postEMSC(url_adress,query):
    json_data = requests.get(url_adress,params=query)
    return parseJson(json.loads(json_data.text))
def postAHEAD(url_adress,query):
    json_data = requests.get(url_adress)
    return parseJson(json.loads(json_data.text),depth=False,region=True)
def query_param_emsc(
        start,end,minlat=-90,maxlat=90,minlon=-180,maxlon=180,mindepth="0",maxdepth=1000,minmag="0.0",maxmag=10.0,
        circle=False,lat=None,lon=None,minradius=None,maxradius=None,
        magnitudetype=None,
        params=None):
    if start: params["start"] = f"{start}T00:00:00.000Z"
    if end: params["end"] = f"{end}T23:59:59.999Z"
    if minlat: params["minlat"] = minlat
    if maxlat: params["maxlat"] = maxlat
    if minlon: params["minlon"] = minlon
    if maxlon: params["maxlon"] = maxlon
    if mindepth: params["mindepth"] = mindepth
    if maxdepth: params["maxdepth"] = maxdepth
    if minmag: params["minmag"] = minmag
    if maxmag: params["maxmag"] = maxmag
    if circle:
        params["lat"] = lat ; params["lon"] = lon ; params["minradius"] = minradius ; params["maxradius"] = maxradius
    #Ml,Ms,mb,Mw
    if magnitudetype:
        params["magtype"] = magnitudetype.lower()
    return params
def query_param_ahead(
        start,end,minlat=-90,maxlat=90,minlon=-180,maxlon=180,minmag="0.0",maxmag=10.0,
        magnitudetype=None,
        params=None):
    if start: params["starttime"] = f"{start}T00:00:00.000Z"
    if end: params["endtime"] = f"{end}T23:59:59.999Z"
    if minlat: params["minlat"] = minlat
    if maxlat: params["maxlat"] = maxlat
    if minlon: params["minlong"] = minlon
    if maxlon: params["maxlong"] = maxlon
    if minmag: params["minmag"] = minmag
    if maxmag: params["maxmag"] = maxmag
    #Ml,Ms,mb,Mw
    if magnitudetype:
        params["magnitudetype"] = magnitudetype.lower()
    return params
def kml_out(data):
    return Create(Convert(pd.DataFrame(data)))
def monthPrint(year,month):
    lastday = last_day(year,month)
    d_params = query_param_emsc(f"{year}-{str(month).zfill(2)}-01",f"{year}-{str(month).zfill(2)}-{lastday}",params=query_params)
    return kml_out(postEMSC(emsc_url,d_params))
def yearPrint(year):
    for i in range(1,13,1):
        print(f"{year}-{str(i).zfill(2)}.kml Writing...",end=" ")
        try:
            outFile(f"{year}-{str(i).zfill(2)}.kml",monthPrint(year,i))
            print("Done.")
        except:
            print("Fail.")
def all_m7():
    lasday = last_day(toyear,tomonth)
    d_params = query_param_emsc("1900-01-01",f"{toyear}-{str(tomonth).zfill(2)}-{lasday}",minmag="7.0",params=query_params)
    return kml_out(postEMSC(emsc_url, d_params))
def ahead_all():
    d_params = query_param_ahead("1000-01-01","1899-12-31",params=query_params)
    return postAHEAD(ahead_url,d_params)
print(ahead_all())