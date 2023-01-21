# Autodraft2.0
Using Deep Q-Learning, I am attempting to create an Autodraft feature for fantasy football that can effectively draft a well-rounded team.

The current roadblock is my team rating function. It takes in the ADP and position of each player on a team and returns a one number power rating for the team's strength. This will take trial and error to correctly tune.

The neural network will initially choose the best player at a random position and update the gradients based on how the team rating changed. As the network is trained,
it will use the policy net to make decisions, hopefully leading to higher team ratings.

It runs now!!! And the policy net is significantly better at drafting than random actions.
