function openNav() {
	var ow = window.outerWidth;
    if (ow < 460){
        document.getElementById("myNav").style.width = "50%";
    }
    else{
        document.getElementById("myNav").style.width = "25%";
    }
}

function closeNav() {
	document.getElementById("myNav").style.width = "0%";
}