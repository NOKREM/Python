import pandas as pd
from pandas import read_csv
from sys import argv

class KmlCreate:
    def __init__(self):
        self.begin_kml = """
<kml>
    <Document>
        <name></name>
        <visibility>0</visibility>
        <open>0</open>
        <Style id="ZERO_TO_ONE">
            <IconStyle>
                <scale>0.2</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="ZERO_TO_ONE_HL">
            <IconStyle>
                <scale>0.29</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="TWO">
            <IconStyle>
                <scale>0.3</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="TWO_HL">
            <IconStyle>
                <scale>0.39</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="THREE">
            <IconStyle>
                <color>ff0295f0</color>
                <scale>0.5</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="THREE_HL">
            <IconStyle>
                <color>ff0295f0</color>
                <scale>0.59</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
         <Style id="FOUR">
            <IconStyle><color>ff00ff00</color>
                <scale>0.7</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="FOUR_HL">
            <IconStyle>
                <color>ff00ff00</color>
                <scale>0.79</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="FIVE">
            <IconStyle>
                <color>ffffaa00</color>
                <scale>0.8</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="FIVE_HL">
            <IconStyle>
                <color>ffffaa00</color>
                <scale>0.89</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="SIX">
            <IconStyle>
                <color>ff7f0000</color>
                <scale>0.9</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="SIX_HL">
            <IconStyle>
                <color>ff7f0000</color>
                <scale>0.99</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="SEVEN">
            <IconStyle>
                <color>ff0000ff</color>
                <scale>1.0</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="SEVEN_HL">
            <IconStyle>
                <color>ff0000ff</color>
                <scale>1.09</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="EIGHT">
            <IconStyle>
                <color>ff0000ff</color>
                <scale>1.2</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="EIGHT_HL">
            <IconStyle>
                <color>ff0000ff</color>
                <scale>1.29</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="NINE">
            <IconStyle>
                <color>ff0000ff</color>
                <scale>1.4</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <Style id="NINE_HL">
            <IconStyle>
                <color>ff0000ff</color>
                <scale>1.49</scale>
                <Icon><href>http://maps.google.com/mapfiles/kml/pal2/icon18.png</href></Icon>
            </IconStyle>
            <LabelStyle><color>00ffffff</color></LabelStyle>
        </Style>
        <StyleMap id="0-1">
            <Pair>
                <key>normal</key>
                <styleUrl>#ZERO_TO_ONE</styleUrl>
            </Pair>
            <Pair>
                <key>highlight</key>
                <styleUrl>#ZERO_TO_ONE_HL</styleUrl>
            </Pair>
        </StyleMap>
        <StyleMap id="2">
            <Pair>
                <key>normal</key>
                <styleUrl>#TWO</styleUrl>
            </Pair>
            <Pair>
                <key>highlight</key>
                <styleUrl>#TWO_HL</styleUrl>
            </Pair>
        </StyleMap>
        <StyleMap id="3">
            <Pair>
                <key>normal</key>
                <styleUrl>#THREE</styleUrl>
            </Pair>
            <Pair>
                <key>highlight</key>
                <styleUrl>#THREE_HL</styleUrl>
            </Pair>
        </StyleMap>
        <StyleMap id="4">
            <Pair>
                <key>normal</key>
                <styleUrl>#FOUR</styleUrl>
            </Pair><Pair>
                <key>highlight</key>
                <styleUrl>#FOUR_HL</styleUrl>
            </Pair>
        </StyleMap>
        <StyleMap id="5">
            <Pair>
                <key>normal</key>
                <styleUrl>#FIVE</styleUrl>
            </Pair>
            <Pair>
                <key>highlight</key>
                <styleUrl>#FIVE_HL</styleUrl>
            </Pair>
        </StyleMap>
        <StyleMap id="6">
            <Pair>
                <key>normal</key>
                <styleUrl>#SIX</styleUrl>
            </Pair>
            <Pair>
                <key>highlight</key>
                <styleUrl>#SIX_HL</styleUrl>
            </Pair>
        </StyleMap>
        <StyleMap id="7">
            <Pair>
                <key>normal</key>
                <styleUrl>#SEVEN</styleUrl>
            </Pair>
            <Pair>
                <key>highlight</key>
                <styleUrl>#SEVEN_HL</styleUrl>
            </Pair>
        </StyleMap>
        <StyleMap id="8">
            <Pair>
                <key>normal</key>
                <styleUrl>#EIGHT</styleUrl>
            </Pair>
            <Pair>
                <key>highlight</key>
                <styleUrl>#EIGHT_HL</styleUrl>
            </Pair>
        </StyleMap>
        <StyleMap id="9">
            <Pair>
                <key>normal</key>
                <styleUrl>#NINE</styleUrl>
            </Pair>
            <Pair>
                <key>highlight</key>
                <styleUrl>#NINE_HL</styleUrl>
            </Pair>
        </StyleMap>"""
        self.begin_folder = """
            <Folder>
                <name>{} Magnitudes</name>"""
        self.placemark = """
                <Placemark>
                    <name>{} - {}</name>
                    <visibility>0</visibility>
                    <description>
                        <![CDATA[
                            <table width='300'>
                                <tr>
                                    <td>Yer</td>
                                    <td>{}</td>
                                </tr>
                                <tr>
                                    <td>Enlem</td>
                                    <td>{}</td>
                                </tr>
                                <tr>
                                    <td>Boylam</td>
                                    <td>{}</td>
                                </tr>
                                <tr>
                                    <td>Derinlik</td>
                                    <td>{}</td>
                                </tr>
                                <tr>
                                    <td>M</td>
                                    <td>{}</td>
                                </tr>
                                <tr>
                                    <td>Tarih-Saat</td>
                                    <td>{}</td>
                                </tr>
                            </table>
                        ]]>
                    </description>
                    <styleUrl>{}</styleUrl>
                    <Point>
                        <coordinates>{},{},0</coordinates>
                        <drawOrder>1</drawOrder>
                    </Point>
                </Placemark>"""
        self.end_folder = """
        </Folder>"""
        self.end_kml = """
    </Document>
</kml>"""
    def Style(self):
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
            if i >= self and self < i+1:
                return styles[i]
        return styles[-1]
    def ColumnCreator(self):
        with open(self, 'r') as temp_f:
            #get No of columns in each line
            col_count = [len(l.split("\t")) for l in temp_f.readlines()]
        ### Generate column names  (names will be 0, 1, 2, ..., maximum columns - 1)
        column_names = [i for i in range(max(col_count))]
        return column_names
    def DataFrameExtract(self, columns):
            return read_csv(self, delimiter="\t", header=None, names=columns)
    def Convert(self):
        self[4] = self[4].astype(float)
        self[3] = self[3].astype(float)
        mag = self[4]
        mags = []
        for i in range(10):
            tmp = mag.between(i, i + 0.9)
            mags.append(self[tmp].reset_index())
        return mags
    def Create(self):
        join_list = []
        join_list.append(KmlCreate().begin_kml)
        for i in range(10):
            count = self[i].shape[0]
            if count == 0:
                continue
            join_list.append(KmlCreate().begin_folder.format(i))
            STYLE = KmlCreate.Style(i)
            for j in range(count):
                """
                    Column Order
                    0 = Date
                    1 = Latitude
                    2 = Longitude
                    3 = Depth
                    4 = Magnitude
                    5 = Location
                """
                join_list.append(KmlCreate().placemark.format(
                    self[i][5][j],
                    self[i][4][j],
                    self[i][5][j],
                    self[i][1][j],
                    self[i][2][j],
                    self[i][3][j],
                    self[i][4][j],
                    self[i][0][j],
                    STYLE,
                    self[i][2][j],
                    self[i][1][j],
                ))
            join_list.append(KmlCreate().end_folder)
        join_list.append(KmlCreate().end_kml)
        return "\n".join(join_list)
    def Out(self):
        columns = KmlCreate.ColumnCreator(self)
        df = KmlCreate.Convert(KmlCreate.DataFrameExtract(self, columns))
        return '\n'.join(KmlCreate.Create(df))
