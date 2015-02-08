'use strict';

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

var constraints = {audio: false, video: true};
var video = document.querySelector('video');
var cvs = document.querySelector('canvas');
var ctx = cvs.getContext('2d');
var img = document.querySelector('#tmp');
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
	img.src = cvs.toDataURL('image/png');
});