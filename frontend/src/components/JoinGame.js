import React from 'react';
import { Alert, Col, ListGroup } from 'react-bootstrap';
import { connect } from 'react-redux';
import { Button } from 'react-bootstrap';
import Header from './Header';
import { Redirect } from 'react-router-dom';
import { TextField } from '@material-ui/core';
import Post from './Post';

const JoinGame = (props) => {
	const handleJoinGame = () => {};

	const { isValidSession, location } = props;

	const URL = 'wss://8mvqn1b54i.execute-api.us-east-1.amazonaws.com/production/'; // TODO: change in the future
	const ws = new WebSocket(URL);

	return (
		<React.Fragment>
			<form noValidate>
				<p>Join a Game!</p>
				<TextField
					variant="outlined"
					margin="normal"
					fullWidth
					name="party_id"
					label="Enter Party ID!"
					id="party_id"
				/>
				<ListGroup>
					<Button type="submit" fullWidth color="primary">
						Join Game!
					</Button>
					<p> </p>
					<Button type="submit" fullWidth color="secondary">
						Create Game!
					</Button>

					<Post />
				</ListGroup>
			</form>
		</React.Fragment>
	);
};

export default JoinGame;
