var colgchild=[];
d3.json("nba_collg.json", function(error,response){
    if(error){console.warn(error);}
    //console.log(response);
    var college_list=[];
    for(var i=0;i<response.length;i++){
        if((!college_list.includes(response[i]["College"])) && (response[i]["College"]!="NA") && (typeof response[i]["College"]!="undefined"))
        {
            college_list.push(response[i]["College"]);
        }
    }

    for(var i=0;i<college_list.length;i++){
        var playerbycolg=[];
        for(var j=0;j<response.length;j++){
            if(response[j]["College"] === college_list[i]){
                var playerinfo={image:response[j]["picurl"],text:{name:response[j]["FirstName"].concat(" ",response[j]["LastName"])},children:{text:"Statistics"}};
                playerbycolg.push(playerinfo);
            }    
        }
        var colg_container={text:{name:college_list[i]},children:playerbycolg};
        colgchild.push(colg_container);
    }
})

var nodejson = {text:{name:"NBA"},children:colgchild};
console.log(nodejson);

var output = document.getElementById("output");
output.innerText=nodejson;


