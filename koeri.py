import requests
import pandas as pd
import re
import xml.etree.ElementTree as ET
import sys
import calendar
from datetime import date,datetime
from typing import List, Optional, Union
import logging
from Kml2 import KmlGenerator

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KOERI:
    """Class for handling Kandilli Observatory and Earthquake Research Institute (KOERI) data."""
    
    # Class constants for URLs and parameters
    LASTQUAKE_URL = "http://www.koeri.boun.edu.tr/scripts/lst0.asp"
    MONTHPRINT_URL_TEMPLATE = "http://udim.koeri.boun.edu.tr/zeqmap/xmlt/{}{}.xml"
    XML_TREE_TAG = "earhquake"
    CODEPAGE = "cp1254"
    
    @classmethod
    def last_day(year: int, month: int) -> str:
        """Get the last day of the given month and year."""
        return str(calendar.monthrange(int(year), int(month))[1])
    
    @classmethod
    def fetch_url(cls, url: str, encoding: Optional[str] = None) -> str:
        """Fetch URL content with error handling."""
        try:
            response = requests.get(url, timeout=30)
            if encoding:
                response.encoding = encoding
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return ""
    
    @classmethod
    def lasteq(cls):
        """Fetch the latest earthquake data."""
        # Get data from KOERI website
        content = cls.fetch_url(cls.LASTQUAKE_URL, cls.CODEPAGE)
        if not content:
            return pd.DataFrame()
        # Split into lines
        lines = content.strip().split('\n')
        main_data = []
        
        # Process each line
        pattern = r'(\d{4}.\d{2}.\d{2} \d{2}:\d{2}:\d{2})\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(\d+\.\d+)\s*(-\.-|\d+\.\d+)\s*(-\.-|\d+\.\d+)\s*(-\.-|\d+\.\d+)\s*(.*)'
        compiled_pattern = re.compile(pattern)
        
        for line in lines:
            match = compiled_pattern.search(line)
            if match:
                date = match.group(1)
                lat = match.group(2)
                long = match.group(3)
                depth = match.group(4)
                md = match.group(5)
                ml = match.group(6)
                mw = match.group(7)
                
                # Determine magnitude
                pmag = ml if mw == "-.-" else mw
                
                # Process location
                loc = match.group(8).split()
                if loc and loc[-1] == "İlksel":
                    loc.pop()
                elif len(loc) >= 3:
                    loc = loc[:-3]  # Remove last three elements
                    
                location = " ".join(loc)
                main_data.append([date, lat, long, depth, pmag, location])
        # Create DataFrame)
        return main_data

    @classmethod
    def month_print(cls, year: Union[str, int], month: Union[str, int]) -> List[List[str]]:
        """Get earthquake data for a specific month and year."""
        # Format URL
        month=datetime(int(year),int(month),1).strftime('%m')
        url = cls.MONTHPRINT_URL_TEMPLATE.format(year,month)
        # Get XML content
        content = cls.fetch_url(url, cls.CODEPAGE)
        if not content:
            return []
        try:
            # Parse XML
            tree = ET.fromstring(content)
            data = []
            
            # Column order mapping
            column_order = [0, 1, 3, 4, 6, 5, 2]
            
            # Process each earthquake entry
            for item in tree.findall(cls.XML_TREE_TAG):
                # Get attributes as list
                attrs = list(item.attrib.values())
                
                # Format date
                attrs[0] = re.sub(' ', '\t', attrs[0])
                
                # Join values with tab
                data.append('\t'.join(attrs))
            
            # Process each data row
            processed_data = []
            for row in data:
                # Split by tab
                row_items = row.split('\t')
                
                # Reorder columns
                ordered_items = [row_items[i] for i in column_order if i < len(row_items)]
                
                # Combine date and time
                ordered_items[0] += " " + ordered_items[1]
                
                # Replace missing magnitude
                if ordered_items[5] == "-.-":
                    ordered_items[5] = "0.0"
                    
                # Remove redundant time
                del ordered_items[1]
                
                processed_data.append(ordered_items)
                
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing XML for {year}-{month}: {e}")
            return []

    @classmethod
    def generate_kml(cls, data, output_file: str = None) -> str:
        """Generate KML from earthquake data."""
        try:
            # Initialize KML generator
            generator = KmlGenerator()
            
            # Process data and create KML
            data_frames = generator.process_data(data)
            kml_content = generator.create_kml(data_frames)
            
            # Save to file if specified
            if output_file:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(kml_content)
                logger.info(f"KML saved to {output_file}")
                
            return kml_content
            
        except Exception as e:
            logger.error(f"Error generating KML: {e}")
            return ""

    @classmethod
    def all_month_print(cls, start_year: int = 2003, end_year: int = None) -> None:
        """Generate KML files for all months in the specified year range."""
        # Default end year to current year if not specified
        if end_year is None:
            end_year = date.today().year
            
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                # Skip future months
                current_date = date.today()
                if year > current_date.year or (year == current_date.year and month > current_date.month):
                    continue
                    
                # Format month
                month_str = f"0{month}" if month < 10 else str(month)
                
                # Output filename
                output_file = f"{year}_{month_str}.kml"
                
                try:
                    # Get data and generate KML
                    data = cls.month_print(year, month_str)
                    if data:
                        cls.generate_kml(data, output_file)
                        
                except Exception as e:
                    logger.error(f"Error processing {year}-{month_str}: {e}")

def main():
    """Main function to handle command-line arguments."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  month_print <year> <month>: Get earthquakes for specific month")
        print("  lasteq: Get latest earthquakes")
        print("  allyear [start_year] [end_year]: Generate KMLs for all months")
        return

    command = sys.argv[1]
    
    try:
        if command == "month_print" and len(sys.argv) >= 4:
            year, month = sys.argv[2], sys.argv[3]
            data = KOERI.month_print(year, month)
            if data:
                output_file = f"{year}-{month}.kml"
                KOERI.generate_kml(data, output_file)
                
        elif command == "lasteq":
            data = KOERI.lasteq()
            if data:
                KOERI.generate_kml(data, "lasteq.kml")
                
        elif command == "allyear":
            start_year = int(sys.argv[2]) if len(sys.argv) >= 3 else 2003
            end_year = int(sys.argv[3]) if len(sys.argv) >= 4 else None
            KOERI.all_month_print(start_year, end_year)
        
        else:
            print(f"Unknown command: {command}")
            
    except Exception as e:
        logger.error(f"Error executing command {command}: {e}")


if __name__ == "__main__":
    main()