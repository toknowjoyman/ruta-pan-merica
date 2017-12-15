var jshelper = parent.jshelper;
var name = document.getElementById("name").textContent;
// var imageURL = document.getElementById("image-url").textContent;
jshelper.pathClicked(name);

// console.log(document.getElementById("myBtn"));
document.getElementById("encodedPath").style.display = "none";
document.getElementById("startLat").style.display = "none";
document.getElementById("startLong").style.display = "none";
document.getElementById("endLat").style.display = "none";
document.getElementById("endLong").style.display = "none";

// document.getElementById("image-url").style.display = "none";




var startLat = document.getElementById("startLat").textContent;
var startLong = document.getElementById("startLong").textContent;
var endLat = document.getElementById("endLat").textContent;
var endLong = document.getElementById("endLong").textContent;
var pathEncoded = document.getElementById("encodedPath").textContent;


// document.getElementById("NoteBtn").addEventListener("click", function(){
//       jshelper.pathClicked(name);
// });

document.getElementById("MyBtn").addEventListener("click", function(){
    console.log("okay");
    jshelper.pathSelected(startLat, startLong, endLat, endLong, name, pathEncoded);
});
 
