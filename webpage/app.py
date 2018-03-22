import pymongo
from pymongo import MongoClient
from flask import(
    Flask,
    render_template,
    jsonify,
    request)

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

@app.route("/charts")
def charts():
    return(render_template("charts.html"))

@app.route("/form")
def forms():
    return(render_template("form.html"))

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
                player_info={"image":Collg[j]["picurl"],
                            "text":{
                                "name":Collg[j]["FirstName"]+" "+Collg[j]["LastName"]
                                    },
                            "children":{
                                "text": "Statistics"
                            }}
                # Append the playerinfo to each colg (playersbycolg)
                playersbycolg.append(player_info)
        # Create a parent element as colg and child element as its players
        colg_child = {"text":{"name":college_list[i]},
                      "children":playersbycolg}
        # Append the colg child element into a list 
        collg_container.append(colg_child)
    # Create a parent element as NBA and child element as the list of child colleges
    node={"text":{"name":"NBA"},
              "children":collg_container}    

    # Return the json response for tree variable
    return jsonify(node)

if __name__ == "__main__":
    app.run(debug = True) 