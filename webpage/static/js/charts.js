d3.json("nba_collg.json", function(error,response){
  if(error){console.warn(error);}
  console.log(response);
})


var tachocanvas=d3.select("#TachometerChart");
var tachosvg= tachocanvas.append("svg").attr("width","450").attr("height","400");
var g=tachosvg.append("g").attr("transform","translate(240,200)");
var domain = [0,100];

var gg = viz.gg()
  .domain(domain)
  .outerRadius(200)
  .innerRadius(30)
  .value(0.5*(domain[1]+domain[0]))
  .duration(1000);

gg.defs(tachosvg);
g.call(gg);  

d3.select(self.frameElement).style("height", "700px");
setInterval( function(){gg.setNeedle(domain[0]+Math.random()*(domain[1]-domain[0]));},2000);