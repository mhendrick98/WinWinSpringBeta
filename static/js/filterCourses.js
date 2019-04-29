function addclass(coursename) {
  document.getElementById("addedcourses").innerHTML += "<p>"+coursename+"</p>";
}

function filterFunction() {
	var input, filter, ul, li, buttonVar, i;
	input = document.getElementById("inputField");
	filter = input.value.toUpperCase();
	div = document.getElementById("myDropdown");
	buttonVar = div.getElementsByTagName("button");
	for(i = 0; i < buttonVar.length; i++){
		txtValue = buttonVar[i].textContent || buttonVar[i].innerText;

		if(txtValue.toUpperCase().indexOf(filter) > -1){
			buttonVar[i].style.display = "";
		}
		else{
			buttonVar[i].style.display = "none";
		}
	}
}
var courses = ['CAS CS111','CAS CS112','CAS CS400','CAS BI100','CAS LX250','ENG CE100','CFA MP105']

window.onload = function populate(){
	endvalue = courses.length;
	for (i = 0; i < endvalue; i=i+1){
		document.getElementById("availablecourses").innerHTML += "<button onclick=\"addclass(&quot;" + courses[i] + "&quot;)\">" + courses[i] + "</button>";
	}
}