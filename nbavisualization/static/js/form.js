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
    document.getElementById("Parent1Ht").style.visibility="visible";
    document.getElementById("Parent2Ht").style.visibility="visible";
    document.getElementById("Colg").style.visibility="hidden";
    document.getElementById("ColgNameHide").style.visibility="hidden";
    document.getElementById("ColgStatsLabel").style.visibility="hidden";
    document.getElementById("ColgStats").style.visibility="hidden";
    }
    else{
    document.getElementById("Parent1Ht").style.visibility="hidden";
    document.getElementById("Parent2Ht").style.visibility="hidden";
    document.getElementById("Colg").style.visibility="visible";
    }
}