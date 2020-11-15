import React from 'react';
import { Card } from 'react-bootstrap';
import _ from 'lodash';
import music from '../images/music.jpeg';

const TracksList = ({ tracks }) => {
	console.log(tracks);
	return (
		<React.Fragment>
			{Object.keys(tracks).length > 0 && (
				<div className="tracks">
					{tracks.items.map((track, index) => {
						return (
							<React.Fragment key={index}>
								<Card style={{ width: '18rem' }}>
									<a
										target="_blank"
										href={track.external_urls.spotify}
										rel="noopener noreferrer"
										className="card-image-link"
									>
										{!_.isEmpty(track.images) ? (
											<Card.Img variant="top" src={track.images[0].url} alt="" />
										) : (
											<img src={music} alt="" />
										)}
									</a>
									<Card.Body>
										<Card.Title>{track.name}</Card.Title>
										<Card.Text>
											<small>{track.artists.map((artist) => artist.name).join(', ')}</small>
										</Card.Text>
									</Card.Body>
								</Card>
							</React.Fragment>
						);
					})}
				</div>
			)}
		</React.Fragment>
	);
};

export default TracksList;
