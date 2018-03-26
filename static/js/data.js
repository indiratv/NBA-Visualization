//var chart_config ={}
d3.json("/treevariable", function(error,response){
    if(error){console.warn(error);}
    console.log(response);
    var chart_config = {
        chart: {
            container: "#treechart",
    
            animateOnInit: true,
            
            node: {
                collapsable: true
            },
            connectors:{
                type: "step"
            },
            rootOrientation:"WEST",
            levelSeparation:100,
            animation: {
                nodeAnimation: "easeOutBounce",
                nodeSpeed: 700,
                connectorsAnimation: "bounce",
                connectorsSpeed: 700
            }
        },
        nodeStructure: response
    };
    console.log(chart_config);      

    tree = new Treant(chart_config);

    console.log(tree);
})



