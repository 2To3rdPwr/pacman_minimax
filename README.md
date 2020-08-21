# pacman_minimax
Just a simple implementation of minimax to play Pac-Man.

Minimax is an algorithm used to determine which action should be taken in adversarial games. It creates a tree to represent the state of the game following each player's turn. Minimax assumes that other players will always take actions to the detriment of the agent player, resulting in the agent taking actions that reduce the worst-case scenario instead of actively seeking out the best-case scenario.

Please note, the VAST majority of the code here is not mine. Any function not preceeded by "@author: Jake Sage" came from [this assignment](https://web.stanford.edu/class/archive/cs/cs221/cs221.1196/assignments/pacman/index.html). I just wanted to make a minimax agent for Pac-Man without having to first create an entire Pac-Man game. Credit for everything else goes to Moses Charikar and Dorsa Sadigh of the University of Stanford Computer Science department.

## Running Pac-Man
This project can be run using
```python pacman.py```
with the following commands
* ```-n GAMES```
  * Run GAMES times and return winrate (Default 1)
* ```-l LAYOUT```
  * Load the map from the layout file LAYOUT in layouts (Default mediumClassic)
    * capsuleClassic
    * contestClassic
    * mediumClassic
    * minimaxClassic
    * openClassic
    * originalClassic
    * smallClassic
    * testClassic
    * trappedClassic
    * trickyClassic
* ```-p AGENT```
  * Which type of agent is used to control Pac-Man (Dafault Keyboard)
    * ReflexAgent
    * MinimaxAgent (mine)
    * AlphaBetaAgent (mine)
    * ExpectimaxAgent (Not Implemented)
* ```-q```
  * Prevent rendering and output to console only
* ```-k NUMGHOSTS```
  * The number of ghosts to use (Default 4)
* ```-g GHOSTTYPE```
  * Ghost AI to use (Default RandomGhost)
    * RandomGhost
    * DirectionalGhost

### My Code
* [Minimax](https://github.com/2To3rdPwr/pacman_minimax/blob/797fde4c788f45ad3c0c17db187c0c50e001e246/submission.py#L168)
