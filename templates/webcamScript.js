let imgTags = document.getElementsByClassName("image");
let days = [ //consider changing to json
    {%for img in imgs%}
        "{{img.datetime.strftime("%b %d")}}",
    {%endfor%}
];
let times = [{%for img in imgs%}"{{img.datetime.strftime("%I:%M %p")}}",{%endfor%}];
days.push("{{nextDT.strftime("%b %d")}}"); //change to standalone variable?
times.push("{{nextDT.strftime("%I:%M %p")}}");

let i = 0;
visible(0);
updateDateTime();
document.getElementById("next").innerHTML = days[days.length - 1] + "<br>" + times[times.length - 1];

let playButton = document.getElementById("play");
let pauseButton = document.getElementById("pause");
let playing = false;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function checkBounds(){
    if (i < 0){
        i = imgTags.length - 1;
    } else if (i >= imgTags.length){
        i = 0;
    }
}
function updateDateTime(){
    document.getElementById("this").innerHTML = days[i] + "<br>" + times[i];
}

function regress(){
    invisible(i);
    i--;
    checkBounds();
    visible(i);
    updateDateTime();
}
function advance(){
    invisible(i);
    i++;
    checkBounds();
    visible(i);
    updateDateTime();
}
async function play(){
    playing = true;
    playButton.className = playButton.className.replace("active", "hidden");
    pauseButton.className = pauseButton.className.replace("hidden", "active");
    while(playing){
        advance();
        await sleep(500);
    }
    playButton.className = playButton.className.replace("hidden", "active");
    pauseButton.className = pauseButton.className.replace("active", "hidden");
}
function pause(){
    playing = false;
}

function visible(index){
    imgTags[index].className = imgTags[index].className.replace("transparent", "visible");
}
function invisible(index){
    imgTags[index].className = imgTags[index].className.replace("visible", "transparent");
}