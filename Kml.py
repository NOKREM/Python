import xml.etree.ElementTree as ET
from xml.dom import minidom
from pandas import read_csv
import calendar
from datetime import date

def outFile(file_name,data):
    file = open(file_name,"w",encoding="utf-8")
    file.write(data)
    file.close()
def last_day(year,month):
    return str(calendar.monthrange(int(year),int(month))[1])
def create_date_string(year, month, day, is_start=True):
    date_string = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}T"
    time_suffix = "00:00:00.000Z" if is_start else "23:59:59.999Z"
    return date_string + time_suffix
now = date.today()
toyear = now.year
tomonth = now.month
today = now.day
ids = [ 'ZERO_TO_ONE' , 'ZERO_TO_ONE_HL', 'TWO', 'TWO_HL', 'THREE', 'THREE_HL', 'FOUR', 'FOUR_HL', 'FIVE', 'FIVE_HL', 'SIX', 'SIX_HL', 'SEVEN', 'SEVEN_HL', 'EIGHT', 'EIGHT_HL', 'NINE', 'NINE_HL']
scales = ['0.2','0.29','0.3','0.39','0.5','0.59','0.7','0.79','0.8','0.89','0.9','0.99','1.0','1.09','2.0','2.09','3.0','3.09']
colors = ['00ffffff', '00ffffff', '00ffffff', '00ffffff', 'ff0295f0', 'ff0295f0', 'ff00ff00', 'ff00ff00' , 'ffffaa00', 'ffffaa00', 'ff7f0000', 'ff7f0000', 'ff0000ff', 'ff0000ff', 'ff4d1c31', 'ff4d1c31', 'ff000000', 'ff000000']
map_ids = ['0-1','0-1','2','2','3','3','4','4','5','5','6','6','7','7','8','8','9','9']
table_data =  "<tr><td>{}</td><td>{}</td></tr>"
cdata = """<![CDATA[<table width='300'><tr><td>Yer</td><td>{}</td></tr><tr><td>Enlem</td><td>{}</td></tr><tr><td>Boylam</td><td>{}</td></tr><tr><td>Derinlik</td><td>{}</td></tr><tr><td>M</td><td>{}</td></tr><tr><td>Tarih-Saat</td><td>{}</td></tr></table>]]>"""
def _escape_cdata(text, encoding="utf-8"):
    try:
        if "&" in text:
            text = text.replace("&", "&amp;")
        # if "<" in text:
            # text = text.replace("<", "&lt;")
        # if ">" in text:
            # text = text.replace(">", "&gt;")
        return text
    except TypeError:
        raise TypeError(
            "cannot serialize %r (type %s)" % (text, type(text).__name__)
        )
ET._escape_cdata = _escape_cdata
def KmlCreate():
     kml = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
     return kml
def DocumentCreate(element,visibility=None,name=None,open=None):
    document = ET.SubElement(element, 'Document')
    if visibility:
        visibility_element = ET.SubElement(document,'visibility')
        visibility_element.text = visibility
    if name:
        name_element = ET.SubElement(document,'name')
        name_element.text = name
    if open:
        open_element = ET.SubElement(document,'open')
        open_element.text = open
    return document
def FolderCreate(element,name=None):
    folder = ET.SubElement(element,'Folder')
    if name:
        name_element = ET.SubElement(folder,'name')
        name_element.text = name
    return folder
def create_placemark(doc_element, name, coordinates, description_text, placemark_id=None, placemark_visibility=None, placemark_styleUrl=None,point_Draworder=None):
    # Placemark elementi oluştur
    placemark = ET.SubElement(doc_element, 'Placemark')

    # Placemark elementine id özelliği ekle (varsa)
    if placemark_id:
        placemark.set('id', str(placemark_id))
    if placemark_visibility:
        visibility_element = ET.SubElement(placemark, 'visibility')
        visibility_element.text = placemark_visibility
    if placemark_styleUrl:
        styleUrl_element = ET.SubElement(placemark, 'styleUrl')
        styleUrl_element.text = placemark_styleUrl
    # Name elementi oluştur ve değeri ata
    name_element = ET.SubElement(placemark, 'name')
    name_element.text = name
    # CDATA elementi oluştur ve değeri ata
    description_element = ET.SubElement(placemark, 'description')
    description_element.text=description_text

    # Point elementi oluştur
    point = ET.SubElement(placemark, 'Point')

    # Coordinates elementi oluştur ve değeri ata
    coordinates_element = ET.SubElement(point, 'coordinates')
    coordinates_element.text = coordinates
    if point_Draworder:
        drawOrder_element = ET.SubElement(point, 'drawOrder')
        drawOrder_element.text = point_Draworder
    return placemark
def create_style(doc_element, style_id, scale, color=None):
    # Style elementi oluştur
    style = ET.SubElement(doc_element, 'Style')
    style.set('id', style_id)

    # IconStyle elementi oluştur
    icon_style = ET.SubElement(style, 'IconStyle')
    # Icon elementi oluştur
    icon = ET.SubElement(icon_style, 'Icon')
    if color:
        icon_color = ET.SubElement(icon_style, 'color')
        icon_color.text = color
    # Hata ayıklama amaçlı olarak icon elementine bir link ekleyelim
    href = ET.SubElement(icon, 'href')
    href.text = 'http://maps.google.com/mapfiles/kml/pal2/icon18.png'
    # Scale elementi oluştur
    scale_element = ET.SubElement(icon_style, 'scale')
    scale_element.text = str(scale)

    # LABELSTYLE elementi oluştur
    labelstyle_element = ET.SubElement(style, 'LabelStyle')
    labelstyle_color = ET.SubElement(labelstyle_element, 'color')
    labelstyle_color.text = "00ffffff"

    return style
def create_style_map(doc_element, style_map_id, normal_style_url, highlight_style_url=None):
    # StyleMap elementi oluştur
    style_map = ET.SubElement(doc_element, 'StyleMap')
    style_map.set('id', style_map_id)

    # Pair elementi oluştur (normal durum)
    pair_normal = ET.SubElement(style_map, 'Pair')
    key_normal = ET.SubElement(pair_normal, 'key')
    key_normal.text = 'normal'
    style_url_normal = ET.SubElement(pair_normal, 'styleUrl')
    style_url_normal.text = normal_style_url

    # Pair elementi oluştur (highlight durum, varsa)
    if highlight_style_url:
        pair_highlight = ET.SubElement(style_map, 'Pair')
        key_highlight = ET.SubElement(pair_highlight, 'key')
        key_highlight.text = 'highlight'
        style_url_highlight = ET.SubElement(pair_highlight, 'styleUrl')
        style_url_highlight.text = highlight_style_url

    return style_map

def Style(sty):
        styles = [
            "#0-1",
            "#0-1",
            "#2",
            "#3",
            "#4",
            "#5",
            "#6",
            "#7",
            "#8",
            "#9"
        ]
        for i in range(10):
            if i >= sty and sty < i+1:
                return styles[i]

def ColumnCreator(data):
    with open(data, 'r') as temp_f:
        #get No of columns in each line
        col_count = [len(l.split("\t")) for l in temp_f.readlines()]
    ### Generate column names  (names will be 0, 1, 2, ..., maximum columns - 1)
    column_names = [i for i in range(max(col_count))]
    return column_names

def DataFrameExtract(data, columns):
    return read_csv(data, delimiter="\t", header=None, names=columns)
def Convert(data):
    data[4] = data[4].astype(float) #Mag
    data[3] = data[3].astype(float) #Depth
    mag = data[4]
    mags = []
    for i in range(10): # Magnitude Sorter
        tmp = mag.between(i, i + 0.9)
        mags.append(data[tmp].reset_index())
    return mags
def Create(data):
    kml = KmlCreate()
    document = DocumentCreate(kml,visibility="0",open="0")
    for i in range(0,len(ids)):
        if i<4:
            create_style(document,str(ids[i]),scales[i]) #büyüklük 3 den küçükse color ekleme
        else:
            create_style(document,str(ids[i]),scales[i],colors[i])
    for i in range(0,len(ids),2):
        create_style_map(document,str(map_ids[i]),f"#{str(ids[i])}",f"#{str(ids[i+1])}")
    for i in range(10):
        count = data[i].shape[0] # İndex Count control
        if count == 0:
            continue
        folder_element = FolderCreate(document,name=f"{str(i)} Magnitudes")
        STYLE = Style(i)
        for j in range(count):
            datehour = data[i][0][j]
            latitude = data[i][1][j]
            longitude = data[i][2][j]
            depth = data[i][3][j]
            magnitude = data[i][4][j]
            location = data[i][5][j]
            create_placemark(folder_element,
                             str(f"{location} - {magnitude}"),
                             str(f"{longitude},{latitude},0"),
                             str(f"{cdata.format(location,latitude,longitude,depth,magnitude,datehour)}"),
                             placemark_visibility="0",
                             placemark_styleUrl=str(STYLE),
                             point_Draworder="1"
                             )

    tree_str = minidom.parseString(ET.tostring(kml)).toprettyxml(indent="    ")

    return tree_str
        