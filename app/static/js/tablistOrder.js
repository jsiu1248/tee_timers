const findButton = document.getElementById("find");
const messageButton = document.getElementById("message");
const playButton = document.getElementById("play");

findButton.addEventListener("click", () => {
  document.getElementById("find-row").style.order = 2;
  document.getElementById("message-row").style.order = 4;
  document.getElementById("play-row").style.order = 5;
});

messageButton.addEventListener("click", () => {
  document.getElementById("find-row").style.order = 3;
  document.getElementById("message-row").style.order = 2;
  document.getElementById("play-row").style.order = 5;
});

playButton.addEventListener("click", () => {
  document.getElementById("find-row").style.order = 3;
  document.getElementById("message-row").style.order = 4;
  document.getElementById("play-row").style.order = 2;
});