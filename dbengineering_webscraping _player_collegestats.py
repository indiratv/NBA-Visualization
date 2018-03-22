#Webscraping the https://www.basketball-reference.com website to get the nba college stats for all the nba players in our masterdata collection - nba_bio in the nba database

#Start the mongodb server in the console. Run this file to scrape the web for all the players in the nba_bio collection in nba database. The result is a collection - nba_collg in the nba database with the data scraped.

#Import Dependencies
from bs4 import BeautifulSoup
import requests
import re
comm = re.compile("<!--|-->")
from ohmysportsfeedspy import MySportsFeeds
import pymongo

#Initialize nba_collg - the final results of our webscraping
nba_collg = []

# Function definition for get_allurls() - To construct college stats url for every player in nba_bio collection in nba db
def get_allurls():
#Placeholder for the data to be returned
    collg_stats_list = []
    baseurl = "https://www.basketball-reference.com/players/"
#Connect to mongodb
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
#From nba db,get nba_bio collection
    db = client.nba
    bio_results = db.nba_bio.find()
#Get url for each player
    for result in bio_results:
        collg_stats_dict = {}
        collg_stats_dict['ID'] = result['ID']
        collg_stats_dict['FirstName'] = result['FirstName']
        collg_stats_dict['LastName'] = result['LastName']
        playerurl = result['LastName'][:1].lower() + '/' + result['LastName'][:5].lower() + result['FirstName'][:2].lower() + '01' + ".html#all_all_college_stats"
        collg_stats_dict['url'] = baseurl + playerurl
        collg_stats_list.append(collg_stats_dict)
#Return a list of dictionaries, each dictionary representing a player info
    return collg_stats_list

# Function definition for make_soup() - To return a bs object corresponding to the url to scrape player's college stats 
def make_soup(url):
    page = requests.get(url)
    soupdata = BeautifulSoup(comm.sub("", page.text), 'lxml')
#Returns a bs object for the url to be scraped
    return soupdata

# Function definition for get_player_totals() - To scrape the college stats for 1 player, takes url to be scraped as parameter
def get_player_totals(url):
#Initiaize the dictionary to hold college stats for a player
    collg_stats = {}
#Do not append the dictionary with keys that are always blank 
    keys_to_remove = ['age','college_id']
#Get soup object for url
    soup = make_soup(url)
#Get college stats for the player from the url
    try:
        allStats = soup.find('table', {'id':'all_college_stats'}).find('tfoot').findAll('td')
    except:
#If no college stats found, append an empty list
        allStats = []
#For players with no college stats available, the key - 'G' will have a value of 'NA' for analysis
    if not allStats:
        collg_stats['G'] = 'NA'
        return collg_stats
    else:
        for stat in allStats:
            collg_stats = { stat['data-stat']: stat.text   for stat in allStats if stat['data-stat'] not in keys_to_remove}
#Returns a dictionary of college stats for each player
    return collg_stats

# Function definition for scrape_all_players() - To scrape the college stats for all players
def scrape_all_players():
#Get urls to be scraped for all players 
    collg_stats_list_intital = get_allurls()
#Intitalize the list to hold all the players stats
    collg_stats_list = []
#     print(collg_stats_list)
#Loop thru each player
    for player in collg_stats_list_intital:
        collg_stats_listitem = {}
        url = player['url']
#Get college stats for each player
        collg_stats_byplayer = get_player_totals(url)
        collg_stats_listitem['ID'] = player['ID']
        collg_stats_listitem['FirstName'] = player['FirstName']
        collg_stats_listitem['LastName'] = player['LastName']
        collg_stats_listitem['collg-stats'] = collg_stats_byplayer
#Add all elements to a list
        collg_stats_list.append(collg_stats_listitem)
#Returns a list of dictionaries containing all players info and college stats
    return collg_stats_list

#Call the scrape_all_players() function.Returns a list of dictionaries containing all players info and college stats
nba_collg = scrape_all_players()

#In nba db, create a nba_collg collection
db = client.nba
collection = db.nba_collg

#Insert the nba_collg data in the nba_collg collection
collection.insert(nba_collg)