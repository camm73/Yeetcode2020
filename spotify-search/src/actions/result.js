import {
	SET_ALBUMS,
	ADD_ALBUMS,
	SET_ARTISTS,
	ADD_ARTISTS,
	SET_PLAYLIST,
	ADD_PLAYLIST,
	ADD_TRACKS,
	SET_TRACKS,
} from '../utils/constants';
import { get } from '../utils/api';

export const setAlbums = (albums) => ({
	type: SET_ALBUMS,
	albums,
});

export const addAlbums = (albums) => ({
	type: ADD_ALBUMS,
	albums,
});

export const setArtists = (artists) => ({
	type: SET_ARTISTS,
	artists,
});

export const addArtists = (artists) => ({
	type: ADD_ARTISTS,
	artists,
});

export const setPlayList = (playlists) => ({
	type: SET_PLAYLIST,
	playlists,
});

export const addPlaylist = (playlists) => ({
	type: ADD_PLAYLIST,
	playlists,
});

export const addTracks = (tracks) => ({
	type: ADD_TRACKS,
	tracks,
});

export const setTracks = (tracks) => ({
	type: SET_TRACKS,
	tracks,
});

export const initiateGetResult = (searchTerm) => {
	return async (dispatch) => {
		try {
			const API_URL = `https://api.spotify.com/v1/search?query=${encodeURIComponent(
				searchTerm
			)}&type=album,playlist,artist,track`;
			const result = await get(API_URL);
			console.log(result);
			const { albums, artists, playlists, tracks } = result;
			dispatch(setAlbums(albums));
			dispatch(setArtists(artists));
			dispatch(setPlayList(playlists));
			return dispatch(setTracks(tracks));
		} catch (error) {
			console.log('error', error);
		}
	};
};

export const initiateLoadMoreAlbums = (url) => {
	return async (dispatch) => {
		try {
			const result = await get(url);
			return dispatch(addAlbums(result.albums));
		} catch (error) {
			console.log('error', error);
		}
	};
};

export const initiateLoadMoreArtists = (url) => {
	return async (dispatch) => {
		try {
			const result = await get(url);
			return dispatch(addArtists(result.artists));
		} catch (error) {
			console.log('error', error);
		}
	};
};

export const initiateLoadMorePlaylist = (url) => {
	return async (dispatch) => {
		try {
			const result = await get(url);
			return dispatch(addPlaylist(result.playlists));
		} catch (error) {
			console.log('error', error);
		}
	};
};

export const initiateLoadMoreTracks = (url) => {
	return async (dispatch) => {
		try {
			const result = await get(url);
			return dispatch(addTracks(result.tracks));
		} catch (error) {
			console.log('error', error);
		}
	};
};
