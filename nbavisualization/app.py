import pymongo
from pymongo import MongoClient
from flask import(
    Flask,
    render_template,
    jsonify,
    request)
from collections import Counter
import numpy as np
import operator
import pandas as pd
import json

# Initialize the Flask application
app = Flask(__name__)  

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017')
# Initialize db as nba database
db = client.nba
# Initialize the collection to variables
nba_bio_collection = db.nba_bio 
nba_collg_collection = db.nba_collg

# App route definitions
@app.route("/")
@app.route("/index")
def landing():
    return(render_template("index.html"))

@app.route("/home")
def home():
    return(render_template("home.html"))

@app.route("/charts")
def charts():
    return(render_template("charts.html"))


@app.route("/data")
def data():
    return(render_template("data.html"))

@app.route("/nba-bio") 
def pymongo_nba_bio_display():
    nba_bio_result=[]
    print("About to call mongo")
    cursor = nba_bio_collection.find({})
    print("Cursor")
    for document in cursor:
        document.pop("_id")
        print(document)
        nba_bio_result.append(document)
    return jsonify(nba_bio_result)

@app.route("/nba-collg") 
def pymongo_nba_collg_display():
    nba_collg_result=[]
    cursor = nba_collg_collection.find({})
    for document in cursor:
        document.pop("_id")
        nba_collg_result.append(document)    
    return jsonify(nba_collg_result)

@app.route("/treevariable")
def treevariable():
    # Get the nba_collg collection stored in a list
    Collg=[]
    cursor = nba_collg_collection.find({})
    for document in cursor:
        document.pop("_id")
        Collg.append(document)

    # Get the unique list of colleges 
    college_list=[]
    for i in range(0,len(Collg)):
        # Only If the document has keys or if the College is not NA
        if (("College" in Collg[i].keys()) and (Collg[i]["College"] not in college_list) and (Collg[i]["College"]!="NA")):
            college_list.append(Collg[i]["College"])

    # Start creating the variable for tree format
    collg_container=[]
    for i in range(0,len(college_list)):
        # Find the players from each college
        playersbycolg=[]
        for j in range(0,len(Collg)):
            if(("College" in Collg[j].keys()) and (Collg[j]["College"]==college_list[i])):
                if(Collg[j]["picurl"]=="NA"):
                    playerstats = Collg[j]["collg-stats"]
                    player_info={"text":{
                                    "name":Collg[j]["FirstName"]+" "+Collg[j]["LastName"]
                                    },
                            "collapsed":"true"
                            }
                else:
                    playerstats = Collg[j]["collg-stats"]
                    player_info={"image":Collg[j]["picurl"],
                                "text":{
                                    "name":Collg[j]["FirstName"]+" "+Collg[j]["LastName"]
                                        },
                                "collapsed":"true",
                                 "children":{"text":"Statistics"}
                                }
                # Append the playerinfo to each colg (playersbycolg)
                playersbycolg.append(player_info)
        # Create a parent element as colg and child element as its players
        colg_child = {"text":{"name":college_list[i]},
                      "collapsed":"true",
                      "children":playersbycolg}
        # Append the colg child element into a list 
        collg_container.append(colg_child)
    # Create a parent element as NBA and child element as the list of child colleges
    node={"image":"http://icons.iconarchive.com/icons/chrisbanks2/cold-fusion-hd/128/nba-2-icon.png",
          "collapsed":"true",
            "children":collg_container}    
    return jsonify(node)

@app.route("/tachocalculatevars")
def tacho_calculation_parameters():
    # Get the nba_collg collection stored in a list
    Bio=[]
    Collg=[]
    Bio = list(nba_bio_collection.find())
    Collg = list(nba_collg_collection.find())
    firstnames=[]
    lastnames=[]
    months=[]
    minspergame=[]
    fgpct=[]
    fg3pct=[]
    ptspergame=[]
    astpergame=[]
    trbpergame=[]
    ftpct=[]
    for i in range(0,len(Bio)):
        firstnames.append(Bio[i]["FirstName"])
        lastnames.append(Bio[i]["LastName"])
        months.append(int(Bio[i]["BirthDate"][5:7]))
        try:
            if(Collg[i]["collg-stats"]["g"]!="NA" or Collg[i]["collg-stats"]["G"]!="NA"):
                stats=Collg[i]["collg-stats"]
                minspergame.append(float(stats["mp_per_g"]))
                fgpct.append(float(stats["fg_pct"]))
                fg3pct.append(float(stats["fg3_pct"]))
                ftpct.append(float(stats["ft_pct"]))
                ptspergame.append(float(stats["pts_per_g"]))
                astpergame.append(float(stats["ast_per_g"]))
                trbpergame.append(float(stats["trb_per_g"]))
        except:
            pass
    
    countfname=Counter(firstnames)
    countlname=Counter(lastnames)
    countmonth=Counter(months)
    mean_mpg = np.mean(minspergame)
    mean_fgpct = np.mean(fgpct)
    mean_fg3pct = np.mean(fg3pct)
    mean_ftpct = np.mean(ftpct)
    mean_ptspergame = np.mean(ptspergame)
    mean_astpergame = np.mean(astpergame)
    mean_trbpergame =np.mean(trbpergame)
    result={"fnames":countfname,
           "lnames":countlname,
           "months":countmonth,
           "mean_mpg":mean_mpg,
           "mean_fgpct":mean_fgpct,
           "mean_fg3pct":mean_fg3pct,
           "mean_ftpct":mean_ftpct,
           "mean_ptspergame":mean_ptspergame,
           "mean_astpergame":mean_astpergame,
           "mean_trbpergame":mean_trbpergame}
    print(result)
    
    return jsonify(result)

@app.route("/nba-names") 
def pymongo_nba_names():
    response  = db.nba_collg.find()
    nbacollgdata = list(response)
    names = []
    i = 0
    for data in nbacollgdata:
        try:
            name = data['FirstName']
            names.append(name)
            i = i + 1
        except:
            pass
    countnames = Counter(names)
    sortednames = sorted(countnames.items(), key=operator.itemgetter(1),reverse=True)
    sortednamesten = sortednames[:10]
    labels=[]
    values=[]
    for i in range(0,len(sortednamesten)):
        labels.append(sortednamesten[i][0])
        values.append(sortednamesten[i][1])
    namesresult = {"labels":labels,"values":values}
    return jsonify(namesresult)

@app.route("/nba-stats") 
def pymongo_nba_stats():
    nba_collgstats_result= {}
    sumfg_pct = 0
    countsumfg_pct = 0
    sumfg3_pct = 0
    countsumfg3_pct = 0
    sumft_pct = 0
    countsumft_pct = 0
    sumft_pct = 0
    countsummp_per_g = 0
    summp_per_g = 0
    countsumpts_per_g = 0
    sumpts_per_g = 0
    countsumtrb_per_g = 0
    sumtrb_per_g = 0
    countsumast_per_g = 0
    sumast_per_g = 0  
    cursor = nba_collg_collection.find({})
    for document in cursor:
        try:
            sumfg_pct = sumfg_pct + float(document['collg-stats']['fg_pct'])
            countsumfg_pct = countsumfg_pct + 1
        except:
            pass
        try:
            sumfg3_pct = sumfg3_pct + float(document['collg-stats']['fg3_pct'])
            countsumfg3_pct = countsumfg3_pct + 1
        except:
            pass
        try:
            sumft_pct = sumft_pct + float(document['collg-stats']['ft_pct'])
            countsumft_pct = countsumft_pct + 1
        except:
            pass
        try:
            summp_per_g = summp_per_g + float(document['collg-stats']['mp_per_g'])
            countsummp_per_g = countsummp_per_g + 1
        except:
            pass
        try:
            sumpts_per_g = sumpts_per_g + float(document['collg-stats']['pts_per_g'])
            countsumpts_per_g = countsumpts_per_g + 1
        except:
            pass  
        try:
            sumtrb_per_g = sumtrb_per_g + float(document['collg-stats']['trb_per_g'])
            countsumtrb_per_g = countsumtrb_per_g + 1
        except:
            pass
        try:
            sumast_per_g = sumast_per_g + float(document['collg-stats']['ast_per_g'])
            countsumast_per_g = countsumast_per_g + 1
        except:
            pass
    meanfg_pct = round(sumfg_pct/countsumfg_pct,2)    
    meanfg3_pct = round(sumfg3_pct/countsumfg3_pct,2)
    meanft_pct = round(sumft_pct/countsumft_pct,2)
    meanmp_per_g = round(summp_per_g/countsummp_per_g,2)
    meanpts_per_g = round(sumpts_per_g/countsumpts_per_g,2)
    meantrb_per_g = round(sumtrb_per_g/countsumtrb_per_g,2)
    meanast_per_g = round(sumast_per_g/countsumast_per_g,2)
    nba_collgstats_keys = ["Field Goal Percentage","3-Point Field Goal Percentage","Free Throw Percentage","Points Per Game","Total Rebounds Per Game","Assists Per Game"]
    nba_collgstats_values = [meanfg_pct,meanfg3_pct,meanft_pct,meanpts_per_g,meantrb_per_g,meanast_per_g]
    nba_collgstats_result["nba_collgstats_keys"] = nba_collgstats_keys
    nba_collgstats_result["nba_collgstats_values"] = nba_collgstats_values

    return jsonify(nba_collgstats_result)

@app.route("/nba-birthdays") 
def pymongo_nba_birthdays():
    nba_bio_result=[]
    cursor = nba_bio_collection.find({})
    for document in cursor:
        document.pop("_id")
        nba_bio_result.append(document)
    result = pd.DataFrame(nba_bio_result)
    Dates = pd.DataFrame(result["BirthDate"])
    Dates["Day"] = ""
    Dates["Month"] = ""
    for index, row in Dates.iterrows():
        Dates.set_value(index,"Month",(row["BirthDate"].split("-")[1]))
        Dates.set_value(index,"Day",(row["BirthDate"].split("-")[2]))
    d = pd.DataFrame({'count' : Dates.groupby( [ "Month", "Day"] ).size()}).reset_index()
    mon = d.loc[d["Month"]=='01'].reset_index(drop=True)
    resultz = []
    for month in range(0,12):
        smon = ""
        eachz = []
        if (month) < 9:
            monno = '0' + str(month+1)
        else:
            monno = str(month+1)
        smon = d.loc[d["Month"]==monno].reset_index(drop=True)
        for day in range(0,31):
            dayz = ""
            if (day) < 9:
                dayno = '0' + str(day+1)
            else:
                dayno = str(day+1)
            try:
                dayz = smon["count"][smon.loc[smon.Day == dayno].index.tolist()[0]]
            except:
                dayz = 0
            eachz.append(int(dayz))
        resultz.append(eachz)
        resultzj = {}
        monthz = []
        monthz = [1,2,3,4,5,6,7,8,9,10,11,12]
        resultzj["data"] = resultz
        # resultzj = dict(zip(monthz,resultz))
    print(resultzj)
    return (jsonify(resultzj))
    

# Run the Application
if __name__ == "__main__":
    app.run(debug = True) 