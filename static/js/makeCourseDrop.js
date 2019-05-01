'use strict';


var fs = require('fs');
var textByLine = fs.readFileSync('static/data/courses.txt').toString().split("\n");
console.log(textByLine);


function makeInner() {
	const values =
		rce("option", {
			value: toString(i),
		}, "courseName"),
		rce("a", {
			href: "/courseSelect",
		}, "Course Selection"),
		rce("a", {
			href: "#"
		}, "Page 3"),
		rce("a", {
			href: "#"
		}, "Page 4");
}




class courseDrop extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		return makeInner();
	}
}

const domContainerMenu = document.querySelector('#courseSelect');
const courseDropContents = ReactDOM.render(rce(courseDrop), domContainerMenu);
