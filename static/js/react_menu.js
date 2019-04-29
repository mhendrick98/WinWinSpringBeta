'use strict';

function closeNav() {
	document.getElementById("myNav").style.width = "0%";
}

function navBar() {
	return rce("div", {
    className: "navWrap"
  }, rce("div", {
    id: "myNav",
    className: "overlay"
  }, rce("a", {
    href: "javascript:void(0)",
    className: "closebtn",
    onClick: closeNav
  }, "\xD7"), rce("div", {
    className: "overlay-content"
  }, rce("a", {
    href: "/dashboard",
  }, "Dashboard"), rce("a", {
    href: "/courseSelect",
  }, "Course Selection"), rce("a", {
    href: "#"
  }, "Page 3"), rce("a", {
    href: "#"
  }, "Page 4"))));
}




class SideMenu extends React.Component {
	constructor(props) {
		super(props);
	}
	
	render() {
		return navBar();
	}
}

const domContainerMenu = document.querySelector('#react_menu_container');
const menuContents = ReactDOM.render(rce(SideMenu), domContainerMenu);
