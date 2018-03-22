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
gkey ="Use your Google API Service Key"

# List of seasons needed
season=['2015-2016','2016-2017']
# Intializing the index for each document being stored
index=1

# Initialize a variable to store the documents
player_list=[];

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
        # Construct the target URL    
        target_url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s"%(target_city,gkey)
        
        # If it is for the season 2015-2016
        # OR if it is not the above season but the player is a rookie
        # Then add the player details to the player_list
        if (j == 0) or (j!=0 and player[i]["player"]["IsRookie"]=="true"):
            try:
                print(target_url)
                geo_data = requests.get(target_url).json()
                lat = geo_data["results"][0]["geometry"]["location"]["lat"]
                long =geo_data["results"][0]["geometry"]["location"]["lng"]
            except:
                lat="NA"
                long="NA"
                
            player_info={
                'ID':index ,
                'UniqueID': player[i]["player"]["ID"],
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
                'Team':  [{'TeamCity':player[i]["team"]["City"],
                            'TeamName':player[i]["team"]["Name"],
                            'TeamAbb':player[i]["team"]["Abbreviation"],
                            'Year': season[j]}]
                }
            index= index+1
            player_list.append(player_info)
            
        # If player is already available in the list then find the corresponding element in player_info 
        # And append to the already existing team info
        else:
            for k in range(0,len(player_list)):
                if player_list[k]["UniqueID"]==player[i]["player"]["ID"]:
                    player_list[k]["Team"].append({'TeamCity':player[i]["team"]["City"],
                        'TeamName':player[i]["team"]["Name"], 
                        'TeamAbb':player[i]["team"]["Abbreviation"],
                        'Year': season[j]})
                        
# Insert each document into the database collection
for b in range(0,len(player_list)):
    collection.insert_one(player_list[b])

# Verify results:
results = db.nba_bio.find()
for result in results:
    print(result)