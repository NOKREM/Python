import xml.etree.ElementTree as ET
from xml.dom import minidom
from pandas import read_csv, DataFrame
import calendar
from datetime import date
from typing import List, Optional, Tuple, Union

# Constants for better maintainability
KML_NAMESPACE = "http://www.opengis.net/kml/2.2"
DEFAULT_ICON_URL = 'http://maps.google.com/mapfiles/kml/pal2/icon18.png'
DEFAULT_LABEL_COLOR = "00ffffff"

class KmlGenerator:
    def __init__(self):
        self.now = date.today()
        self.toyear = self.now.year
        self.tomonth = self.now.month
        self.today = self.now.day
        
        # Style configuration
        self.ids = ['ZERO_TO_ONE', 'ZERO_TO_ONE_HL', 'TWO', 'TWO_HL', 'THREE', 'THREE_HL', 
                   'FOUR', 'FOUR_HL', 'FIVE', 'FIVE_HL', 'SIX', 'SIX_HL', 'SEVEN', 'SEVEN_HL', 
                   'EIGHT', 'EIGHT_HL', 'NINE', 'NINE_HL']
        self.scales = ['0.2', '0.29', '0.3', '0.39', '0.5', '0.59', '0.7', '0.79', '0.8', '0.89', 
                       '0.9', '0.99', '1.0', '1.09', '2.0', '2.09', '3.0', '3.09']
        self.colors = ['00ffffff', '00ffffff', '00ffffff', '00ffffff', 'ff0295f0', 'ff0295f0', 
                      'ff00ff00', 'ff00ff00', 'ffffaa00', 'ffffaa00', 'ff7f0000', 'ff7f0000', 
                      'ff0000ff', 'ff0000ff', 'ff4d1c31', 'ff4d1c31', 'ff000000', 'ff000000']
        self.map_ids = ['0-1', '0-1', '2', '2', '3', '3', '4', '4', '5', '5', 
                        '6', '6', '7', '7', '8', '8', '9', '9']
        
        # Style map lookup
        self.style_map = {
            0: "#0-1",
            1: "#0-1",
            2: "#2", 
            3: "#3",
            4: "#4",
            5: "#5",
            6: "#6",
            7: "#7",
            8: "#8",
            9: "#9"
        }
        
        # Initialize XML escape function
        self._setup_xml_escape()

    def _setup_xml_escape(self):
        """Configure XML CDATA escape handling"""
        def _escape_cdata(text, encoding="utf-8"):
            try:
                if "&" in text:
                    text = text.replace("&", "&amp;")
                return text
            except TypeError:
                raise TypeError(f"cannot serialize {text!r} (type {type(text).__name__})")
        
        ET._escape_cdata = _escape_cdata

    def create_element(self, parent: ET.Element, tag: str, 
                      text: Optional[str] = None, **attrs) -> ET.Element:
        """Helper method to create XML elements with optional text and attributes"""
        element = ET.SubElement(parent, tag, **attrs)
        if text is not None:
            element.text = text
        return element

    def create_kml_document(self, visibility: str = "0", open_val: str = "0", 
                           name: Optional[str] = None) -> Tuple[ET.Element, ET.Element]:
        """Create base KML and Document elements"""
        kml = ET.Element('kml', xmlns=KML_NAMESPACE)
        document = self.create_element(kml, 'Document')
        
        if visibility:
            self.create_element(document, 'visibility', visibility)
        if name:
            self.create_element(document, 'name', name)
        if open_val:
            self.create_element(document, 'open', open_val)
            
        return kml, document

    def create_styles(self, document: ET.Element) -> None:
        """Create all styles and style maps in one go"""
        # Create styles
        for i, (style_id, scale, color) in enumerate(zip(self.ids, self.scales, self.colors)):
            if i < 4:
                self._create_style(document, style_id, scale)
            else:
                self._create_style(document, style_id, scale, color)
        
        # Create style maps
        for i in range(0, len(self.ids), 2):
            self._create_style_map(document, self.map_ids[i], 
                                  f"#{self.ids[i]}", f"#{self.ids[i+1]}")

    def _create_style(self, document: ET.Element, style_id: str, 
                     scale: str, color: Optional[str] = None) -> ET.Element:
        """Create a style element with icon style"""
        style = self.create_element(document, 'Style', id=style_id)
        icon_style = self.create_element(style, 'IconStyle')
        
        if color:
            self.create_element(icon_style, 'color', color)
        
        icon = self.create_element(icon_style, 'Icon')
        self.create_element(icon, 'href', DEFAULT_ICON_URL)
        self.create_element(icon_style, 'scale', scale)
        
        label_style = self.create_element(style, 'LabelStyle')
        self.create_element(label_style, 'color', DEFAULT_LABEL_COLOR)
        
        return style

    def _create_style_map(self, document: ET.Element, style_map_id: str, 
                         normal_style_url: str, highlight_style_url: str = None) -> ET.Element:
        """Create a style map with normal and highlight pairs"""
        style_map = self.create_element(document, 'StyleMap', id=style_map_id)
        
        # Normal style
        normal_pair = self.create_element(style_map, 'Pair')
        self.create_element(normal_pair, 'key', 'normal')
        self.create_element(normal_pair, 'styleUrl', normal_style_url)
        
        # Highlight style
        if highlight_style_url:
            highlight_pair = self.create_element(style_map, 'Pair')
            self.create_element(highlight_pair, 'key', 'highlight')
            self.create_element(highlight_pair, 'styleUrl', highlight_style_url)
        
        return style_map

    def create_placemark(self, parent: ET.Element, name: str, coordinates: str, 
                        location: str, lat: str, lon: str, depth: str, magnitude: str, 
                        datehour: str, visibility: str = "0", style_url: str = None) -> ET.Element:
        """Create a placemark with all earthquake data"""
        placemark = self.create_element(parent, 'Placemark')
        
        if visibility:
            self.create_element(placemark, 'visibility', visibility)
            
        if style_url:
            self.create_element(placemark, 'styleUrl', style_url)
            
        self.create_element(placemark, 'name', name)
        # Create description with CDATA
        description = f"""<![CDATA[<table width='300'>
            <tr><td>Yer</td><td>{location}</td></tr>
            <tr><td>Enlem</td><td>{lat}</td></tr>
            <tr><td>Boylam</td><td>{lon}</td></tr>
            <tr><td>Derinlik</td><td>{depth}</td></tr>
            <tr><td>M</td><td>{magnitude}</td></tr>
            <tr><td>Tarih-Saat</td><td>{datehour}</td></tr>
            </table>]]>"""
        
        self.create_element(placemark, 'description', description)
        
        point = self.create_element(placemark, 'Point')
        self.create_element(point, 'coordinates', coordinates)
        self.create_element(point, 'drawOrder', "1")
        
        return placemark

    def process_data(self, data_source: Union[str, List]) -> List[DataFrame]:
        """Process earthquake data and return magnitude-sorted dataframes
        
        Args:
            data_source: Either a file path or list of earthquake data
        """
        # Handle list input directly from KOERI module
        if isinstance(data_source, list):
            return self.process_data_from_list(data_source)
        
        # Otherwise process from file
        return self.process_data_from_file(data_source)
    
    def process_data_from_list(self, data_list: List) -> List[DataFrame]:
        """Process earthquake data from a list returned by KOERI module"""
        # Convert list data to DataFrame
        df = DataFrame(data_list)
        
        # Ensure consistent format - KOERI returns data in a different order 
        # than the file version, so remap columns as needed
        # Assuming the KOERI list structure has: date, lat, lon, depth, magnitude, location
        df_mapped = df.copy()
        
        # Convert numeric columns
        df_mapped[3] = df_mapped[3].astype(float)  # Depth
        df_mapped[4] = df_mapped[4].astype(float)  # Magnitude
        
        # Split by magnitude ranges
        mag_frames = []
        for i in range(10):
            tmp = df_mapped[df_mapped[4].between(i, i + 0.9)].reset_index()
            mag_frames.append(tmp)
            
        return mag_frames
    
    def process_data_from_file(self, file_path: str) -> List[DataFrame]:
        """Process earthquake data from file and return magnitude-sorted dataframes"""
        # Read column structure
        columns = self._get_column_count(file_path)
        
        # Read and process data
        df = read_csv(file_path, delimiter="\t", header=None, names=columns)
        df[4] = df[4].astype(float)  # Magnitude
        df[3] = df[3].astype(float)  # Depth
        
        # Split by magnitude ranges
        mag_frames = []
        for i in range(10):
            tmp = df[df[4].between(i, i + 0.9)].reset_index()
            mag_frames.append(tmp)
            
        return mag_frames
    
    def _get_column_count(self, file_path: str) -> List[int]:
        """Get column structure from data file"""
        try:
            with open(file_path, 'r') as f:
                col_count = [len(line.split("\t")) for line in f]
            return [i for i in range(max(col_count))]
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return [i for i in range(10)]  # Default fallback

    def create_kml(self, data_frames: List[DataFrame]) -> str:
        """Create full KML document from processed data frames"""
        # Create base KML structure
        kml, document = self.create_kml_document(visibility="0", open_val="0")
        
        # Add styles
        self.create_styles(document)
        
        # Process each magnitude range
        for i in range(10):
            count = data_frames[i].shape[0]
            if count == 0:
                continue
                
            folder = self.create_element(document, 'Folder')
            self.create_element(folder, 'name', f"{i} Magnitudes")
            
            style_url = self.style_map.get(i, "#0-1")
            
            # Add all placemarks for this magnitude range
            for j in range(count):
                row = data_frames[i].iloc[j]
                datehour = row[0]
                latitude = row[1]
                longitude = row[2]
                depth = row[3]
                magnitude = row[4]
                location = row[5]
                
                self.create_placemark(
                    parent=folder,
                    name=f"{location} - {magnitude}",
                    coordinates=f"{longitude},{latitude},0",
                    location=location,
                    lat=latitude,
                    lon=longitude,
                    depth=depth,
                    magnitude=magnitude,
                    datehour=datehour,
                    visibility="0",
                    style_url=style_url
                )
                
        # Convert to pretty XML
        return minidom.parseString(ET.tostring(kml)).toprettyxml(indent="    ")

    @staticmethod
    def save_kml(kml_content, output_file):
        """Save KML content to file"""
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(kml_content)
            print(f"KML saved successfully to {output_file}")
        except Exception as e:
            print(f"Error saving KML to {output_file}: {e}")

# Helper functions for backward compatibility
def last_day(year, month):
    return str(calendar.monthrange(int(year), int(month))[1])

def create_date_string(year, month, day, is_start=True):
    date_string = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}T"
    time_suffix = "00:00:00.000Z" if is_start else "23:59:59.999Z"
    return date_string + time_suffix

def outFile(file_name, data):
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(data)
    except Exception as e:
        print(f"Error writing to {file_name}: {e}")

# Example usage
def process_earthquake_data(data):
    generator = KmlGenerator()
    data_frames = generator.process_data(data)
    kml_content = generator.create_kml(data_frames)
    return kml_content