'use strict';



class MainWindow extends React.Component {
	constructor(props) {
		super(props);
		this.state = { liked: false };
	}

	render() {
		if (this.state.liked) {
			return 'You liked this.';
		}

		return rce(
			'button',
			{ onClick: () => this.setState({ liked: true }) },
			'Like'
		);
	}
}

const domContainerWindow = document.querySelector('#react_window_container');
ReactDOM.render(rce(MainWindow), domContainerWindow);