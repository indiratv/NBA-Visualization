import pymongo
from pymongo import MongoClient
from flask import(
    Flask,
    render_template,
    jsonify,
    request)
from collections import Counter
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

@app.route("/")
@app.route("/index")
def home():
    return(render_template("index.html"))

@app.route("/nba-bio") 
def pymongo_nba_bio_display():
    nba_bio_result=[]
    cursor = nba_bio_collection.find({})
    for document in cursor:
        document.pop("_id")
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

# @app.route("/nba-monthday") 
# def pymongo_month_day():

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
    nba_collgstats_keys = ["Field Goal Percentage","3-Point Field Goal Percentage","Free Throw Percentage","Minutes Played Per Game","Points Per Game","Total Rebounds Per Game","Assists Per Game"]
    nba_collgstats_values = [meanfg_pct,meanfg3_pct,meanft_pct,meanmp_per_g,meanpts_per_g,meantrb_per_g,meanast_per_g]
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

@app.route("/nba-statsbypos") 
def pymongo_nba_statsbypos():
    nba_collg_statsr = []
    collg = nba_collg_collection.find({})
    for document in collg:
        document.pop("_id")
        nba_collg_statsr.append(document)

    nba_collg_statsr = pd.DataFrame(nba_collg_statsr)
    nba_collg_statsr["Position"] = ""
    nba_collg_statsr["fg_pct"] = ""
    nba_collg_statsr["fg3_pct"] = ""
    nba_collg_statsr["ft_pct"] = ""
    nba_collg_statsr["pts_per_g"] = ""
    nba_collg_statsr["trb_per_g"] = ""
    nba_collg_statsr["ast_per_g"] = ""

    for index,row in nba_collg_statsr.iterrows():
        try:
            nba_collg_statsr.set_value(index,"fg_pct",row["collg-stats"]["fg_pct"])
        except:
            nba_collg_statsr.set_value(index,"fg_pct",0)
        try:
            nba_collg_statsr.set_value(index,"fg3_pct",row["collg-stats"]["fg3_pct"])
        except:
            nba_collg_statsr.set_value(index,"fg3_pct",0)
        try:
            nba_collg_statsr.set_value(index,"ft_pct",row["collg-stats"]["ft_pct"])
        except:
            nba_collg_statsr.set_value(index,"ft_pct",0)
        try:
            nba_collg_statsr.set_value(index,"pts_per_g",row["collg-stats"]["pts_per_g"])
        except:
            nba_collg_statsr.set_value(index,"pts_per_g",0)
        try:
            nba_collg_statsr.set_value(index,"trb_per_g",row["collg-stats"]["trb_per_g"])
        except:
            nba_collg_statsr.set_value(index,"trb_per_g",0)
        try:
            nba_collg_statsr.set_value(index,"ast_per_g",row["collg-stats"]["ast_per_g"])
        except:
            nba_collg_statsr.set_value(index,"ast_per_g",0)
        try:
            p = nba_bio_collection.find({'ID': row["ID"]})
            temp = []
            for d in p:
                nba_collg_statsr.set_value(index,"Position",d['Position'])
        except:
            nba_collg_statsr.set_value(index,"Position",0)
    nba_collg_results = nba_collg_statsr[["ID","Position","fg_pct","fg3_pct","ft_pct","pts_per_g","trb_per_g","ast_per_g"]]
    nba_collg_results = nba_collg_results.loc[nba_collg_results["fg_pct"] != 0, :]
    nba_collg_results["fg_pct"] = pd.to_numeric(nba_collg_results["fg_pct"])
    nba_collg_results["fg3_pct"] = pd.to_numeric(nba_collg_results["fg3_pct"])
    nba_collg_results["ft_pct"] = pd.to_numeric(nba_collg_results["ft_pct"])
    nba_collg_results["pts_per_g"] = pd.to_numeric(nba_collg_results["pts_per_g"])
    nba_collg_results["trb_per_g"] = pd.to_numeric(nba_collg_results["trb_per_g"])
    nba_collg_results["ast_per_g"] = pd.to_numeric(nba_collg_results["ast_per_g"])
    final = {}
    g = nba_collg_results.groupby("Position").mean()
    a1 = pd.DataFrame(g["fg_pct"])
    b1 = a1.to_dict()
    final["fg_pct"] = b1["fg_pct"]
    a2 = pd.DataFrame(g["fg3_pct"])
    b2 = a2.to_dict()
    final["fg3_pct"] = b2["fg3_pct"]
    a3 = pd.DataFrame(g["ft_pct"])
    b3 = a3.to_dict()
    final["ft_pct"] = b3["ft_pct"]
    a4 = pd.DataFrame(g["pts_per_g"])
    b4 = a4.to_dict()
    final["pts_per_g"] = b4["pts_per_g"]
    a5 = pd.DataFrame(g["trb_per_g"])
    b5 = a5.to_dict()
    final["trb_per_g"] = b5["trb_per_g"]
    a4 = pd.DataFrame(g["ast_per_g"])
    b4 = a4.to_dict()
    final["ast_per_g"] = b4["ast_per_g"]
    res = [(pd.DataFrame(final).T).to_dict()]

    return jsonify(res)



if __name__ == "__main__":
    app.run(debug = True) 