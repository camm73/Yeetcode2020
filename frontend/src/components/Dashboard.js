import React, { useState } from 'react';

import {
	initiateGetResult,
	initiateLoadMoreAlbums,
	initiateLoadMorePlaylist,
	initiateLoadMoreArtists,
	initiateLoadMoreTracks,
} from '../actions/result';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';
import SearchResult from './SearchResult';
import SearchForm from './SearchForm';
import Header from './Header';
import Loader from './Loader';

// Dashboard is for song selection
const Dashboard = (props) => {
	const defaultPage = 'tracks';
	const [isLoading, setIsLoading] = useState(false);
	const [selectedCategory, setSelectedCategory] = useState(defaultPage);
	const { isValidSession, history } = props;

	const handleSearch = (searchTerm) => {
		if (isValidSession()) {
			setIsLoading(true);
			props.dispatch(initiateGetResult(searchTerm)).then(() => {
				setIsLoading(false);
				setSelectedCategory(defaultPage);
			});
		} else {
			history.push({
				pathname: '/',
				state: {
					session_expired: true,
				},
			});
		}
	};

	const loadMore = async (type) => {
		if (isValidSession()) {
			const { dispatch, albums, artists, playlist, tracks } = props;
			setIsLoading(true);
			switch (type) {
				case 'tracks':
					await dispatch(initiateLoadMoreTracks(tracks.next));
					break;
				case 'albums':
					await dispatch(initiateLoadMoreAlbums(albums.next));
					break;
				case 'artists':
					await dispatch(initiateLoadMoreArtists(artists.next));
					break;
				case 'playlist':
					await dispatch(initiateLoadMorePlaylist(playlist.next));
					break;
				default:
			}
			setIsLoading(false);
		} else {
			history.push({
				pathname: '/',
				state: {
					session_expired: true,
				},
			});
		}
	};

	const setCategory = (category) => {
		setSelectedCategory(category);
	};

	const { albums, artists, playlist, tracks } = props;
	const result = { albums, artists, playlist, tracks };

	return (
		<React.Fragment>
			{isValidSession() ? (
				<div>
					<Header />
					<SearchForm handleSearch={handleSearch} />
					<Loader show={isLoading}>Loading...</Loader>
					<SearchResult
						result={result}
						loadMore={loadMore}
						setCategory={setCategory}
						selectedCategory={selectedCategory}
						isValidSession={isValidSession}
					/>
				</div>
			) : (
				<Redirect
					to={{
						pathname: '/',
						state: {
							session_expired: true,
						},
					}}
				/>
			)}
		</React.Fragment>
	);
};

const mapStateToProps = (state) => {
	return {
		albums: state.albums,
		artists: state.artists,
		playlist: state.playlist,
		tracks: state.tracks,
	};
};

export default connect(mapStateToProps)(Dashboard);
