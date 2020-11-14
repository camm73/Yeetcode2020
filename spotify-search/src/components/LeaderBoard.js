import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import Post from './Post';

const useStyles = makeStyles((theme) => ({
	root: {
		width: '100%',
		maxWidth: 360,
		backgroundColor: theme.palette.background.paper,
	},
}));

export default function LeaderBoard() {
	const classes = useStyles();

	const listItems = tracks.map((t) => <Post songName={t.songName} artist={t.artist} />);

	return <List className={classes.root} {...listItems}></List>;
}
