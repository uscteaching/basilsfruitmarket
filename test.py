# import python extraction library
# we can install it by using 'pip install petl
from typing import Dict, Any, Union, Tuple

import petl

# List of source and target files for merge

healthcsvfile = './datafiles/Vic_Health_Care.csv'
locationxmlfile = './datafiles/Vic_Locations.xml'
mergedcsvfile = './datafiles/practice_locations.csv'

# xmlfields is a dictionary to be used as 

xmlfields = {'Town_name': 'Town', 'Latitude': 'Lat', 'Longitude': 'Lon'}  # type: Dict[str, str]
xmlparent = 'Town_location'
initialrow = ['Practice_Name', 'Latitude', 'Longitude', 'Town', 'State', 'Post_Code']

# tables in memory created from xml and csv files

csvtable = petl.fromcsv(healthcsvfile)
xmltable = petl.fromxml(locationxmlfile, xmlparent, xmlfields)

# Find the row in xmltable matching town from csv 
lktbl = petl.lookupone(xmltable, 'Town_name')  # type: Union[Dict[Any, Union[tuple[Any], Tuple[Any]]], Any]
nmdtbl = petl.namedtuples(csvtable)
finaltabl = [initialrow]

for lin in nmdtbl:
    tabl = lktbl[lin.Town]
    latitude = tabl[0]
    longitude = tabl[1]

    insertline = (str(lin.Practice_Name) + ',' + latitude + ',' + longitude + ',' + str(
        lin.Town) + ',' + str(lin.State) + ',' + str(lin.Postcode)).split(',')
    print insertline
    finaltabl.extend([insertline])

petl.tocsv(finaltabl, mergedcsvfile)
