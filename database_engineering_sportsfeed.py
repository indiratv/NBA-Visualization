# Install MySportsFeed and simplejson
# pip install ohmysportsfeedspy
# pip install simplejson
from ohmysportsfeedspy import MySportsFeeds
import pymongo
import requests
import json

# Authenticating the MySportsFeeds API
Data_query = MySportsFeeds('1.2',verbose=True)
Data_query.authenticate('Aiyana410', '04101993mad')

# The default port used by MongoDB is 27017
# https://docs.mongodb.com/manual/reference/default-mongodb-port/
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Declare the database
db = client.nba

# Declare the collection
collection = db.nba_bio


# Google API Servcies key
gkey ="AIzaSyC5rGYUddVUFDYwhmshYciMpNeQxpa2YmQ"

# List of seasons needed
season=['2015-2016','2016-2017']
# Intializing the index for each document being stored
index=1

# For 2 seasons
for j in range(0,2):
    # Calling the API to get response for each season
    Output = Data_query.msf_get_data(league='nba',season=season[j]+'-regular',feed='roster_players',format='json')
    player = Output["rosterplayers"]["playerentry"]
    
    # For each player in the season
    for i in range(0,len(player)):
        # Try and except in case the Height is not available
        try:
            height=player[i]["player"]["Height"]
        except:
            height="NA"
        # Try and except in case the Weight is not available
        try:
            weight=player[i]["player"]["Weight"]
        except:
            weight="NA"
        # Try and except in case the BirthCity is not available
        try:
            birthcity = player[i]["player"]["BirthCity"]
        except:
            birthcity = "NA"
        # Try and except in case the BirthCountry is not available
        try:
            birthcountry = player[i]["player"]["BirthCountry"]
        except:
            birthcountry = "NA"
        
        # Initialize the target city to retrive the latitude and longitude of place of birth
        target_city = birthcity+","+birthcountry
        try:
            target_url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s"%(target_city,gkey)
            geo_data = requests.get(target_url).json()
            lat = geo_data["results"][0]["geometry"]["location"]["lat"]
            long =geo_data["results"][0]["geometry"]["location"]["lng"]
        except:
            lat="NA"
            long="NA"
            
        post = {
            'PlayerID':index ,
            'Year': season[j],
            'FirstName': player[i]["player"]["FirstName"],
            'LastName': player[i]["player"]["LastName"],
            'Position':player[i]["player"]["Position"],
            'BirthDate':player[i]["player"]["BirthDate"],
            "BirthCity":birthcity,
            "BirthCountry":birthcountry,
            "BirthPlaceLat": lat,
            "BirthPlaceLong": long,
            "Height":height,
            'Weight':weight,
            'TeamCity':player[i]["team"]["City"],
            'TeamName':player[i]["team"]["Name"],
            'TeamAbb':player[i]["team"]["Abbreviation"]
        }
        # Insert the document into the collection
        collection.insert_one(post)
        # Incrementing the index by 1 for the next document
        index=index+1

# Verify results:
results = db.nba_bio.find()
for result in results:
    print(result)