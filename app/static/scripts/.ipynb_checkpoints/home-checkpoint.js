


function toast() {
  document.getElementById('toaster').style.backgroundImage = 'url(/static/images/toaster_down.png)';
  document.getElementById('toast').style.backgroundImage = 'url(/static/images/toast.png)';
  document.getElementById('toaster').style.transform = 'translate(-53%, 0%)';
  document.getElementById('toast').style.transform = 'translate(-53%, 54%)';


}


function untoast() {
  document.getElementById('toaster').style.backgroundImage = 'url(/static/images/toaster_up.png)';
  document.getElementById('toaster').style.transform = 'translate(-53%, 0%)';
  document.getElementById('toast').style.backgroundImage = 'url(/static/images/toast.png)';
  document.getElementById('toast').style.transform = 'translate(-53%, 7%)';

}

function finish_toasting() {
  //your code to be executed after 1 second

  document.getElementById('toaster').style.backgroundImage = 'url(/static/images/toaster_up.png)';
  document.getElementById('toaster').style.transform = 'translate(-53%, 0%)';
  document.getElementById('toast').style.backgroundImage = 'url(/static/images/toast.png)';
  document.getElementById('toast').style.transform = 'translate(-53%, 7%)';
  document.getElementById("search").click();
}

function burnToast() {
  var delayInMilliseconds = 800; //1 second

  document.getElementById('toaster').style.backgroundImage = 'url(/static/images/toaster_down.png)';
  document.getElementById('toast').style.backgroundImage = 'url(/static/images/toast.png)';
  document.getElementById('toaster').style.transform = 'translate(-53%, 0%)';
  document.getElementById('toast').style.transform = 'translate(-53%, 54%)';

  setTimeout(finish_toasting, delayInMilliseconds);
}