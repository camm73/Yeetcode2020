import React from 'react';
import Home from './views/Home';
import { Route, Switch, Redirect, BrowserRouter as Router } from 'react-router-dom';
import SignIn from './views/SignIn';

export const Routes = () => {
	return (
		<div>
			<Router>
				<Switch>
					<Route exact path="/Home" component={Home} />
					<Route exact path="/">
						<Redirect to="/Home" />
					</Route>
					<Route exact path="/signin" component={SignIn} />
				</Switch>
			</Router>
		</div>
	);
};
