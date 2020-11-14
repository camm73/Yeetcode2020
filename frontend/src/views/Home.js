import React from 'react';
import { SpotifyApiContext } from 'react-spotify-api';
import Cookies from 'js-cookie';

import { SpotifyAuth, Scopes } from 'react-spotify-auth';
import 'react-spotify-auth/dist/index.css';

const Home = () => {
	const token = Cookies.get('spotifyAuthToken');
	console.log(token);
	return (
		<div className="app">
			{token ? (
				<SpotifyApiContext.Provider value={token}>
					{/* Your Spotify Code here */}
					<p>You are authorized with token: {token}</p>
				</SpotifyApiContext.Provider>
			) : (
				// Display the login page
				<SpotifyAuth
					redirectUri="http://localhost:3000/callback"
					clientID="1a70ba777fec4ffd9633c0c418bdcf39"
					scopes={[Scopes.userReadPrivate, 'user-read-email']} // either style will work
				/>
			)}
		</div>
	);
};
export default Home;
