'use strict';

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

var constraints = {audio: false, video: true};
var video = document.querySelector('video');
var cvs = document.querySelector('canvas');
var ctx = cvs.getContext('2d');
var file = document.querySelector('#tmp');
var streaming = false;

function successCallback(stream) {
  window.stream = stream; // stream available to console
  if (window.URL) {
    video.src = window.URL.createObjectURL(stream);
  } else {
    video.src = stream;
  }
  streaming = true;
}

function errorCallback(error){
  console.log('navigator.getUserMedia error: ', error);
  streaming = false;
}

navigator.getUserMedia(constraints, successCallback, errorCallback);


$("#the_button").click(function(e) {
	if (!streaming) return;
	ctx.drawImage(video,0,0);
	console.log(cvs.toDataURL('image/png'));
	file.src = cvs.toDataURL('image/png');
});

$("#override").click(function(e) {
  var encoded = file.src.replace(/^data:image\/(png|jpg);base64,/, "");

  var grad=$("#grad").val();
  $.ajax({
    type: "post", 
    url: "grab",
    data : {
      photo: encoded,
      gradient: grad
    },
    success: function(data, textStatus, jqXHR) {
      $(".ctnr").html("<div class='main'><img src='" + data + "'><a href='/'><h4>sloth again</h4></a></div>");
    }
  });
  return false;
});