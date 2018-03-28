var mapbox = 'https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1Ijoia2pnMzEwIiwiYSI6ImNpdGRjbWhxdjAwNG0yb3A5b21jOXluZTUifQ.T6YbdDixkOBWH_k9GbS8JQ'

var birthPlaces = new L.LayerGroup();
var colleges = new L.LayerGroup();
var highSchools = new L.LayerGroup();


//Create overlay object
var overlayMaps = {
"Birth Place Locations": birthPlaces,
"College Locations": colleges,
"High School Locations": highSchools
};

//Create map layers
var myMap = L.map('map', {
  center: [25.698277, 1.240623],
  zoom: 2,
  layers: [birthPlaces]
});

var baseMaps = L.tileLayer(mapbox).addTo(myMap);


//BIRTHPLACE HEATMAP

d3.json("nba-bio", function(response){
  //console.log(response);
  var heatArray = [];
  for (var i = 0; i < response.length; i++) {
    var location = response[i];
    if ((location["BirthPlaceLat"] != "NA") || (location["BirthPlaceLong"] != "NA")) {
      if(typeof location["BirthPlaceLat"] !== "undefined") {
        heatArray.push([location["BirthPlaceLat"], location["BirthPlaceLong"]])
      }     
    }
  }
  var heat = L.heatLayer(heatArray, {
  radius: 45,
  blur: 50,
  minOpacity: 0.9,
  max: 100
  }).addTo(birthPlaces); 
});


// //COLLEGE HEATMAP

d3.json("/nba-collg", function(response){
  var heatArray1 = [];
  for (var i = 0; i < response.length; i++) {
    var location = response[i];
    if ((location["Cglat"] != "NA") || (location["Cglong"] != "NA")) {
      if(typeof location["Cglat"] !== "undefined") {
        heatArray1.push([location["Cglat"], location["Cglong"]])
      }   
    }
  }
  var heat1 = L.heatLayer(heatArray1, {
  radius: 45,
  blur: 70,
  minOpacity: 0.9,
  max: 100
  }).addTo(colleges);   
});


// //HIGH SCHOOL HEATMAP

d3.json("/nba-collg", function(response){
  var heatArray2 = [];
  for (var i = 0; i < response.length; i++) {
    // console.log(response[i])
    var location = response[i];
    if ((location["Hslat"] != "NA") || (location["Hslong"] != "NA")) {
      if(typeof location["Hslat"] !== "undefined") {
        heatArray2.push([location["Hslat"], location["Hslong"]])
      }  
    }
  }
  var heat2 = L.heatLayer(heatArray2, {
  radius: 45,
  blur: 70,
  minOpacity: 0.9,
  max: 100
  }).addTo(highSchools);    
});

L.control.layers(overlayMaps).addTo(myMap);

//---------------
// HEAT CHART SHOWING BIRTHDAYS
//---------------
d3.json("/nba-birthdays", function(error, response) {
  console.log(response["data"]);
   // this is your data
  // console.log(response.to_list());
  // console.log(response.keys);
  var data = [
  {
    z: response["data"],
    x: ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'],
    y: ['January','Feburary','March','April','May','June','July','August','September','October','November','December'],
    type: 'heatmap',
    colorscale:
    [[0,"#fff7f3"],[0.1,"#fde0dd"],[0.2,"#fcc5c0"],[0.3,"#fa9fb5"],[0.4,"#f768a1"],[0.5,"#dd3497"],[0.6,"#ae017e"],[0.7,"#7a0177"],[1,"#49006a"]],
    // [[0,"#ffffd9"],[0.1,"#edf8b1"],[0.2,"#c7e9b4"],[0.3,"#7fcdbb"],[0.4,"#41b6c4"],[0.5,"#1d91c0"],[0.6,"#225ea8"],[0.7,"#253494"],[1,"#081d58"]]
    // [[0.1,"#ffffe5"],[0.2,"#f7fcb9"],[0.3,"#d9f0a3"],[0.4,"#addd8e"],[0.5,"#78c679"],[0.6,"#41ab5d"],[0.7,"#238443"],[0.8,"#006837"],[1,"#004529"]]
    // [[0,"#ffffe5"],[0.1,"#f7fcb9"],[0.2,"#d9f0a3"],[0.3,"#addd8e"],[0.4,"#78c679"],[0.5,"#41ab5d"],[0.6,"#238443"],[0.7,"#006837"],[1,"#004529"]]
  xgap: 3,
  ygap: 3
  },
  ];
  var layout = {
  annotations: [],
  xaxis: {
    tickvals: ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31'],
    side: 'top',
    ticks: ''
  },
  yaxis: {
    ticksvals:['January','Feburary','March','April','May','June','July','August','September','October','November','December'],
    side: 'left',
    ticks: '',
    width: 700,
    height: 700,
    autosize: true
  }
  };

  Plotly.newPlot("myBarChart", data,layout);
});

//---------------
//-POLAR CHART
//----------------
var data = []

d3.json("/nba-names", function(error, response) {
   //console.log(response); // this is your data
   //console.log(response["values"]);
   //console.log(response["labels"]);
  // Chart1: Polar Area
  var ctx = document.getElementById('myChart').getContext('2d');
  Chart.defaults.global.defaultColor = 'rgba(0, 0, 0, 0.1)';
  Chart.defaults.polarArea.animation.animateScale = true;
  Chart.defaults.polarArea.animation.animateRotate = true;
  data = {
    datasets: [{
        data: response["values"],
        backgroundColor: ["#e66cd8", "#e8c56d","#00ffff","#e8c3b9","#c45850",
        "#b3fedf","#e6e6fa","#73922f","#f6fdbc","#a004f2"]
    }],

    // These labels appear in the legend and in the tooltips when hovering different arcs
    labels: response["labels"]
  };

  var chart = new Chart(ctx, {
    data: data,
    type: 'polarArea',
    options: {
      title: {
        display: true,
        text: 'Top 10 Frequent First names in NBA'
      }
    }    
  });
});