
//----------------------------
// Form Code
//-----------------------------

function Validate_colg(){
  if(document.getElementById('CollegeAttending').checked){
  document.getElementById("ColgNameHide").style.visibility="visible";
  document.getElementById("ColgStatsLabel").style.visibility="visible";
  document.getElementById("ColgStats").style.visibility="visible";
  }
  else {
  document.getElementById("ColgNameHide").style.visibility="hidden";
  document.getElementById("ColgStatsLabel").style.visibility="hidden";
  document.getElementById("ColgStats").style.visibility="hidden";
  }
}

function updateAge(){
  var date = new Date(document.getElementById("DOB").value);
  var today = new Date();
  
  var timeDiff = Math.abs(today.getTime() - date.getTime());
  
  var age1 = Math.round(timeDiff / (1000 * 3600 * 24)) / 365;

  document.getElementById("Age").value=age1;


  if(age1<18){
  document.getElementById("ParentHt").style.visibility="visible";
  document.getElementById("Colg").style.visibility="hidden";
  document.getElementById("ColgNameHide").style.visibility="hidden";
  document.getElementById("ColgStatsLabel").style.visibility="hidden";
  document.getElementById("ColgStats").style.visibility="hidden";
  }
  else{
  document.getElementById("ParentHt").style.visibility="hidden";
  document.getElementById("Colg").style.visibility="visible";
  }
}


//----------------------------
//  Plot Code
//-----------------------------

function PlotCharts(){
  d3.json("/tachocalculatevars", function(error,response){
    if(error){console.warn(error);}
    console.log("Tachovars");
    console.log(response);
    // Initialize DOM variable for the form 
    var FName = document.getElementById("FirstName").value;
    var LName = document.getElementById("LastName").value;
    var DOB = document.getElementById("DOB").value;
    var Age = document.getElementById("Age").value;
    var Month = DOB.slice(5,7);
    var CurrentCity = document.getElementById("CurrentLocation").value;
    var Heightin = document.getElementById("inches").value;
    var Heightft = document.getElementById("feet").value;
    var P1Htin = document.getElementById("P1inches").value;
    var P1Htft = document.getElementById("P1feet").value;
    var P2Htin = document.getElementById("P2inches").value;
    var P2Htft = document.getElementById("P2feet").value;
    var ColgName = document.getElementById("CollegeName").value;
    var ColgFG = document.getElementById("FG").value;
    var Colg3PFG = document.getElementById("3PFG").value;
    var ColgFT = document.getElementById("FT").value;
    var ColgPTS = document.getElementById("PTS").value;
    var ColgTRB = document.getElementById("TRB").value;
    var ColgAST = document.getElementById("AST").value;
    console.log(FName+","+LName+","+Age+","+DOB+","+CurrentCity+","+Heightft+"'"+Heightin);//+","+P1Height+","+P2Height);
    console.log(ColgName+":"+ColgFG+","+Colg3PFG+","+ColgFT+","+ColgPTS+","+ColgAST+","+ColgTRB);
    //Calculate the tachometer value    
    var htscore=0;

    if(Age>28){
      htscore=0;
    }
    else if((Age>18) && (Age<=28)){
      if(Heightft>=6){
        htscore=1;
      }
      else if((Heightft>=5) && (Heightin>=7)){
        htscore=0.7;
      }
      else if((Heightft>=5) && (Heightin>=3)){
        htscore=0.4;
      }
      else if(Heightft<5){
        htscore=0;
      }
    }
    else{
      if((P2Htft>=5)&&(P2Htin>=8)){
        if(P1Htft>=6){
          htscore=1;
        }
        else if((P1Htft>=5)&&(P1Htin>=7)){
          htscore=0.7;
        }
        else if((P1Htft>=5)&&(P1Htin>=3)){
          htscore=0.4;
        }
        else if(P1Htft<5){
          htscore=0;
        }

      }
      else if((P2Htft>=5)&&(P2Htin>=5)){
        if((P1Htft>6)){
          htscore=0.9;
        }
        else if((P1Htft>=5)&&(P1Htin>=7)){
          htscore=0.6;
        }
        else if((P1Htft>=5)&&(P1Htin>=3)){
          htscore=0.3;
        }
        else if(P1Htft<5){
          htscore=0;
        }
      }
      else{
        if(P1Htft>=6){
          htscore=0.8;
        }
        else if((P1Htft>=5)&&(P1Htin>=7)){
          htscore=0.5;
        }
        else if((P1Htft>=5)&&(P1Htin>=3)){
          htscore=0.2;
        }
        else if(P1Htft<5){
          htscore=0;
        }
      }
    }
   // console.log("Height Score: "+htscore);

    var stats_fg=0;
    if((ColgFG!="")||(typeof ColgFG!="undefined")){
      var stats_fg_val=((response["mean_fgpct"]-ColgFG)/response["mean_fgpct"]);
      if(stats_fg_val<0){
        stats_fg=1;
      }
      else{
        stats_fg=1-stats_fg_val;
      }
    }
    //console.log(stats_fg);

    var stats_3pfg=0;
    if((Colg3PFG!="")||(typeof Colg3PFG!="undefined")){
      var stats_fg3_val=((response["mean_fg3pct"]-Colg3PFG)/response["mean_fg3pct"]);
      if(stats_fg3_val<0){
        stats_3pfg=1;
      }
      else{
        stats_3pfg=1-stats_fg3_val;
      }
    }
    //console.log(stats_3pfg);

    var stats_ft=0;
    if((ColgFT!="")||(typeof ColgFT!="undefined")){
      var stats_ft_val=((response["mean_ftpct"]-ColgFT)/response["mean_ftpct"]);
      if(stats_ft_val<0){
        stats_ft=1;
      }
      else{
        stats_ft=1-stats_ft_val;
      }
    }
    //console.log(stats_ft);

    var stats_ast=0;
    if((ColgAST!="")||(typeof ColgAST!="undefined")){
      var stats_ast_val=((response["mean_astpergame"]-ColgAST)/response["mean_astpergame"]);
      if(stats_ast_val<0){
        stats_ast=1;
      }
      else{
        stats_ast=1-stats_ast_val;
      }
    }
    //console.log(stats_ast);
    var stats_trb=0;
    if((ColgTRB!="")||(typeof ColgTRB!="undefined")){
      var stats_trb_val=((response["mean_trbpergame"]-ColgTRB)/response["mean_trbpergame"]);
      if(stats_trb_val<0){
        stats_trb=1;
      }
      else{
        stats_trb=1-stats_trb_val;
      }
    }
    //console.log(stats_trb);
    var stats_pts=0;
    if((ColgPTS!="")||(typeof ColgPTS!="undefined")){
      var stats_pts_val=((response["mean_ptspergame"]-ColgPTS)/response["mean_ptspergame"]);
      if(stats_pts_val<0){
        stats_pts=1;
      }
      else{
        stats_pts=1-stats_pts_val;
      }
    }
    //console.log(stats_pts);
    // Calculating total score as per the data
    var fnameprob=0;
    if(response["fnames"][FName]!="undefined"){
      fnameprob=10*(response["fnames"][FName]/555);
    }
    if(isNaN(fnameprob)){
      fnameprob=0;
    }
    console.log("FName Prob:"+fnameprob);

    var lnameprob=0;
    if(response["lnames"][LName]!="undefined"){
      lnameprob=10*(response["lnames"][LName]/555);
    }
    if(isNaN(lnameprob)){
      lnameprob=0;
    }
    console.log("LName Prob:"+lnameprob);

    var monthprob=0;
    if(response["months"][Month]!="undefined"){
      monthprob=10*(response["months"][Month]/555);
    }
    if(isNaN(monthprob)){
      monthprob=0;
    }
    console.log("Month Prob:"+monthprob);
   

    var score = (fnameprob + lnameprob + monthprob + htscore + stats_pts + stats_trb + stats_ast + stats_ft + stats_3pfg + stats_fg);
    console.log("Calculating Score: "+score)
    score_pct= Math.round(score*10);
    console.log(score_pct);

    //-----------------------------
    // TACHO PLOT
    //-----------------------------
    var tachocanvas=d3.select("#TachometerChart");
    // Remove the previous content
    tachocanvas.select("svg").remove();
    var tachosvg= tachocanvas.append("svg").attr("width","450").attr("height","400");
    var g=tachosvg.append("g").attr("transform","translate(240,200)");
    var domain = [0,100];
    console.log("Score");
    console.log(score_pct)
    var gg = viz.gg()
    .domain(domain)
    .outerRadius(200)
    .innerRadius(30)
    .value(0.0*(domain[1]+domain[0]))
    .duration(1000);
    
    gg.defs(tachosvg);
    g.call(gg);  
    d3.select(self.frameElement).style("height", "700px");
    setInterval( function(){gg.setNeedle(score_pct);},3000);

    //-----------------------------
    // RADAR PLOT
    //-------------------------------
    console.log(ColgName+":"+ColgFG+","+Colg3PFG+","+ColgFT+","+ColgPTS+","+ColgAST+","+ColgTRB);
    d3.json("/nba-stats", function(error, response) {
      console.log(response); // this is your data
      console.log(response.values);
      console.log(response.keys);
   
    var ctx = document.getElementById('myChart').getContext('2d');
    data = {
        labels: response["nba_collgstats_keys"],
        datasets: [
        {
              label: "Mean NBA Stats (per game)",
              fill: true,
              backgroundColor: "rgba(249, 207, 149,0.2)",
              borderColor: "rgba(230, 155, 51, 1)",
              pointBorderColor: "rgba(230, 155, 51, 1)",
              pointBackgroundColor: "rgba(207, 126, 12, 1)",
              data: response["nba_collgstats_values"]
        },
        {
              label: "Comparing your NBA Stats (per game)",
              fill: true,
              backgroundColor: "rgba(127, 146, 240,0.2)",
              borderColor: "#5e97ed",
              pointBorderColor: "#2371e7",
              pointBackgroundColor: "#2371e7",
              data: [ColgFG,Colg3PFG,ColgFT,ColgPTS,ColgTRB,ColgAST]
              // response["your_collgstats_values"]
        },
        ]
    }
    var myRadarChart = new Chart(ctx, {
        type: 'radar',
        data: data,
        options: {
          title: {
            display: true,
            text: 'NBA Stats'
          }
        }
    });

    //-----------------------------
    // MAP PLOT CODE
    //-----------------------------
    var mapbox = 'https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2pnMzEwIiwiYSI6ImNpdGRjbWhxdjAwNG0yb3A5b21jOXluZTUifQ.T6YbdDixkOBWH_k9GbS8JQ'
    var colleges = new L.LayerGroup();
    var highSchools = new L.LayerGroup();
    //Create overlay object
    var overlayMaps = {
    "College Locations": colleges,
    "High School Location": highSchools
    };
    //Target City
    var targetCity = CurrentCity;
    var gkey = "AIzaSyCxKPSTYYmUq6eMQqv3gZnAT-v4zPzp5pY"
    var queryURL = "https://maps.googleapis.com/maps/api/geocode/json?address=" + targetCity + "s&key=" + gkey;
    d3.json(queryURL, function(error, response) {
      var geocenter=[25.698277, 1.240623];
      var zoomval=3;
      if((response.results!=[])||(response["status"]=="OK")){
        geocenter=[response["results"][0]["geometry"]["location"]["lat"],response["results"][0]["geometry"]["location"]["lng"]];
        zoomval= 5;
      }
      var myMap = L.map("map2", {
        center: geocenter,
        zoom: zoomval,
        layers: [colleges]
        });

      // Create a baseMaps object
      var baseMaps = L.tileLayer(mapbox).addTo(myMap);
      //HIGH SCHOOL LOCATIONS
      d3.json("/nba-collg", function(response){
        console.log(response);
        for (var i = 0; i < response.length; i++) {
          var collegeLocation = response[i];
          if ((collegeLocation.Cglat != "NA" )|| (collegeLocation.Cglong != "NA")) {
            if(typeof collegeLocation.Cglat !== "undefined") {(
              L.marker([collegeLocation["Cglat"], collegeLocation["Cglong"]]).addTo(colleges).bindPopup("<h1>" + collegeLocation.College + "</h1>")
              )
            } 
          }
        };
        for (var i = 0; i < response.length; i++) {
          var highSchoolLocation = response[i];
          if ((highSchoolLocation.Hslat != "NA") || (highSchoolLocation.Hslong != "NA")) {
            if(typeof highSchoolLocation.Cglat !== "undefined") {
              L.marker([highSchoolLocation["Hslat"], highSchoolLocation["Hslong"]]).addTo(highSchools).bindPopup("<h1>" + highSchoolLocation.HighSchool + "</h1> <hr> <h3>" + highSchoolLocation.Hscity + ", " + highSchoolLocation.Hsstate + "</h3")
              console.log()
            }
          }
        }
      });

      // Plot the filter circle
      //console.log(response);
      if((response.results==[])||(response["status"]=="ZERO_RESULTS")){
        console.log("No Location Found")
      }
      else{
        console.log(response["results"][0]["geometry"]["location"]["lat"]);
        // var location1 = [response.results.geometry.location.lat, response.results.geometry.location.lng];
        // console.log(location1)
        L.circle([response["results"][0]["geometry"]["location"]["lat"],response["results"][0]["geometry"]["location"]["lng"]], {
          fillOpacity: 0.7,
          color: "navy",
          fillColor: "lightblue",
          radius: 500000
        }).addTo(myMap);
      }
      L.control.layers(overlayMaps).addTo(myMap);
    });
    
   });
  });

}


//----------------------------
//Submit Button Code
//----------------------------
$("#nbaform").submit(function(e){
  e.preventDefault();
  console.log("Activating Charts");
  //----------------------------
  // PLOTTING ALL PLOTS
  //----------------------------
  PlotCharts();
});


