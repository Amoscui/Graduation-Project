function leftTimer(){
  var minutes = 119;//计算剩余的分钟
  var seconds = 59;//计算剩余的
  minutes = checkTime(minutes);
  seconds = checkTime(seconds);
  if (seconds < 0) {
      seconds = 59;
      minutes -= 1;
  }
  if (minutes < 0){
     document.getElementById("timer").innerText = "考试结束";
  }
  minutes = checkTime(minutes);
  seconds = checkTime(seconds);
  document.getElementById("timer").innerHTML = minutes + ':' + seconds;
}

var clock;
function startTimer(){
    clock = setInterval("leftTimer()",1000 );
}

function checkTime(i){ //将0-9的数字前面加上0，例1变为01
  if(i<10)
  {
    i = "0" + i;
  }
  return i;
}
