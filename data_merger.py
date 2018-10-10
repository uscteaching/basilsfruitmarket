# import python extraction library
# we can install it by using 'pip install petl
#
import petl

#
# List of source and target files for merge
#
healthcsvfile = './datafiles/Vic_Health_Care.csv'
locationxmlfile = './datafiles/Vic_Locations.xml'
mergedcsvfile = './datafiles/practice_locations.csv'

#
# xmlfields is a dictionary to be used as key and values
#
xmlfields = {'Town_name': 'Town', 'Latitude': 'Lat', 'Longitude': 'Lon'}
# xml parent tag to start from
xmlparent = 'Town_location'
#
# Create a list to be used as final merged table
finaltabl_initialrow = ['Practice_Name', 'Latitude', 'Longitude', 'Town', 'State', 'Post_Code']
finaltabl = [finaltabl_initialrow]
#
# Tables in memory created from xml and csv files
#
csvtable = petl.fromcsv(healthcsvfile)
xmltable = petl.fromxml(locationxmlfile, xmlparent, xmlfields)
#
# Create a dictionary with key as town name and values as latitude, longitude and town name
lkupdictionary = petl.lookupone(xmltable, 'Town_name')
#
# Create named tuple instances accessible by attribute name
nmdtpl = petl.namedtuples(csvtable)

#
#
# Return the tuple from Dictionary using Town as key
for instance in nmdtpl:
    towntuple = lkupdictionary[instance.Town]

    latitude = towntuple[0]
    longitude = towntuple[1]


    # Create a list of values from comma delimited string
    insertline = (
            str(instance.Practice_Name + ',' + latitude + ',' + longitude + ',' + instance.Town + ','
            + instance.State + ',' + instance.Postcode)).split(
        ',')
    finaltabl.extend([insertline])
#

petl.tocsv(finaltabl, mergedcsvfile)

