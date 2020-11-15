import React, { Component } from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import List from '@material-ui/core/List';
import ListItemText from '@material-ui/core/ListItemText';
import Avatar from '@material-ui/core/Avatar';
import { Card, CardContent } from '@material-ui/core';
import { ToggleButtonGroup, ToggleButton } from 'react-bootstrap';

// List Item that displays a song
class Post extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			disabledUpvote: false,
			disabledDownvote: false,
		};

		this.handleUpvoteClicked = this.handleUpvoteClicked.bind(this);
		this.handleDownvoteClicked = this.handleDownvoteClicked.bind(this);
	}

	handleUpvoteClicked() {
		if (!this.state.disabledUpvote) {
			this.setState({
				disabledUpvote: true,
				disabledDownvote: false,
			});
		}
	}

	handleDownvoteClicked() {
		if (!this.state.disabledDownvote) {
			this.setState({
				disabledUpvote: false,
				disabledDownvote: true,
			});
		}
	}

	render() {
		const { content, createdAt, votes } = this.props.post;

		return (
			<div className="post-container">
				<Card>
					<CardContent>
						<div>
							<ListItem>
								{/* <ListItemAvatar>
									<Avatar>

                  </Avatar>
								</ListItemAvatar> */}
								<ListItemText primary={this.props.songName} secondary={this.props.artist} />
							</ListItem>
						</div>
						<div style={{ textAlign: 'right' }}>
							<ToggleButtonGroup orientation="horizontal" exclusive>
								<ToggleButton value="upvote" aria-label="list" onChange={this.handleUpvoteClicked}>
									Upvote
								</ToggleButton>
								<ToggleButton
									value="downvote"
									aria-label="module"
									onChange={this.handleDownvoteClicked}
								>
									Downvote
								</ToggleButton>
							</ToggleButtonGroup>
						</div>
					</CardContent>
				</Card>
			</div>
		);
	}
}

export default Post;
