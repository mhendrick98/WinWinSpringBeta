'use strict';


function dashboard() {
  return rce("div", {id: "inWindow"},
			rce("div", {id: "page-wrap"},
				rce("h1", null,
					"Dashboard"),
				rce("h2", null,
					"Press menu to open sidebar.")));
}

function other() {
  return rce("div", {id: "inWindow"},
			rce("div", {id: "page-wrap"},
				rce("h1", null,
					"Other page"),
				rce("h2", null,
					"Press menu to open  sidebar!")));
}

class MainWindow extends React.Component {
	constructor(props) {
		super(props);
		this.state = { page: "dashboard" };
	}

	render() {
		if (this.state.page == "dashboard"){
			return dashboard();
		}
		else if (this.state.page == "other"){
			return other();
		}
	}
}



const domContainerWindow = document.querySelector('#react_window_container');
const mainWindowContents = ReactDOM.render(rce(MainWindow), domContainerWindow);

function changeWindow(stateVal){
    mainWindowContents.setState({ page: stateVal });
}


