from bottle import run, route, request,response
import petl

csvdata=petl.fromcsv('./datafiles/practice_locations.csv')
lkupdictionary = petl.lookupone(csvdata, 'Post_Code')


def getjson(pcode):

    valueslist = list(lkupdictionary[str(pcode)])

    keyslist=['Practice_Name','Latitude','Longitude','Town','State','Post_Code']

    json_dictionary = {}

    for i in range(len(keyslist)):
         json_dictionary[keyslist[i]] = valueslist[i]

    return json_dictionary

@route('/getlocation')
def jsonreturn():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return getjson(request.query.postcode)

run(host='localhost', port=8081, debug=True)
