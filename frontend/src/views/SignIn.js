import React from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';
import { Scopes, SpotifyAuth } from 'react-spotify-auth';

class SignIn extends React.Component {
	constructor(props) {
		super(props);
		this.redirectHome = this.redirectHome.bind(this);
	}

	redirectHome(token) {
		this.props.history.push('/home');
	}

	render() {
		return (
			<Container component="main" maxWidth="xs">
				<CssBaseline />
				<div>
					<form noValidate>
						<div
							style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}
						>
							<SpotifyAuth
								redirectUri="http://localhost:3000/callback"
								clientID="1a70ba777fec4ffd9633c0c418bdcf39"
								scopes={[Scopes.userReadPrivate, Scopes.userReadEmail]} // TODO: add the necessary
								onAccessToken={this.redirectHome}
							/>
						</div>
					</form>
				</div>
			</Container>
		);
	}
}

export default SignIn;
