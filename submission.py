import sys

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """
  def __init__(self):
    self.lastPositions = []
    self.dc = None


  def getAction(self, gameState):
    """
    getAction chooses among the best options according to the evaluation function.

    getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
    ------------------------------------------------------------------------------
    Description of GameState and helper functions:

    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes. In this function, the |gameState| argument
    is an object of GameState class. Following are a few of the helper methods that you
    can use to query a GameState object to gather information about the present state
    of Pac-Man, the ghosts and the maze.

    gameState.getLegalActions():
        Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

    gameState.generateSuccessor(agentIndex, action):
        Returns the successor state after the specified agent takes the action.
        Pac-Man is always agent 0.

    gameState.getPacmanState():
        Returns an AgentState object for pacman (in game.py)
        state.configuration.pos gives the current position
        state.direction gives the travel vector

    gameState.getGhostStates():
        Returns list of AgentState objects for the ghosts

    gameState.getNumAgents():
        Returns the total number of agents in the game

    gameState.getScore():
        Returns the score corresponding to the current state of the game


    The GameState class is defined in pacman.py and you might want to look into that for
    other helper methods, though you don't need to.
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best


    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following:
      pacman won, pacman lost or there are no legal moves.
    """
    return self.minimax(gameState, self.depth, 0)

  def minimax(self, state, depth, player):
    """
      Minimax adversarial search.
      @author: Jake Sage
      :param state: gameState at the given node of the minimax tree
      :param depth: How deep in the minimax tree we are currently
      :param player: 0 = Pac-Man, 1+ = Ghosts
      :return: While recurring, the score chosen by minimax at this node
                At the tree root, return the action Pac-Man will take
    """
    if depth == 0 or state.isWin() or state.isLose():
      # End States
      return better(state)
    elif player == 0:
      # Pac-Man (Max Agent)
      maxAction = -1 * sys.maxint
      actions = state.getLegalActions(player)
      for action in actions:
        result = self.minimax(state.generateSuccessor(player, action), depth, player + 1)
        if maxAction == result:     # randomize result of ties to help break up thrashing
          bestAction = random.choice([bestAction, action])
        elif maxAction < result:
          maxAction = result
          bestAction = action
      if depth == self.depth:
        return bestAction
      else:
        return maxAction
    else:
      # Ghosts (Min Agent)
      minAction = sys.maxint
      actions = state.getLegalActions(player)
      for action in actions:
        if player + 1 < state.getNumAgents():
          result = self.minimax(state.generateSuccessor(player, action), depth, player + 1)
        else:
          result = self.minimax(state.generateSuccessor(player, action), depth - 1, 0)
        if minAction > result:
          minAction = result
      return minAction

######################################################################################
# Problem 2a: implementing alpha-beta

class AlphaBetaAgent(MultiAgentSearchAgent):

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """

    return self.alphaBetaMinimax(gameState, self.depth, 0, -1 * sys.maxint, sys.maxint)

  def alphaBetaMinimax(self, state, depth, player, alpha, beta):
    """
      @author: Jake Sage
      Minimax using alpha-beta pruning.
      alpha-beta pruning is an optimization of
      minimax that eliminates entire branches of
      the game state tree that will never be selected.
      :param state: gameState at the given node of the minimax tree
      :param depth: How deep in the minimax tree we are currently
      :param player: 0 = Pac-Man, 1+ = Ghosts
      :param alpha: the highest value Pac-Man can achieve at the given level or above
      :param beta: the lowest value the ghosts can achieve at the given level or above
      :return: While recurring, the score chosen by minimax at this node
                At the tree root, return the action Pac-Man will take
    """
    if depth == 0 or state.isWin() or state.isLose():
      # End States
      return better(state)
    elif player == 0:
      # Pac-Man (Max Agent)
      maxAction = -1 * sys.maxint
      actions = state.getLegalActions(player)
      for action in actions:
        result = self.alphaBetaMinimax(state.generateSuccessor(player, action), depth, player + 1, alpha, beta)
        if maxAction == result:  # randomize result of ties to help break up thrashing
          bestAction = random.choice([bestAction, action])
        elif maxAction < result:
          maxAction = result
          bestAction = action
        alpha = max(alpha, maxAction)
        if beta <= alpha:
          break
      if depth == self.depth:
        return bestAction
      else:
        return maxAction
    else:
      # Ghosts (Min Agent)
      minAction = sys.maxint
      actions = state.getLegalActions(player)
      for action in actions:
        if player + 1 < state.getNumAgents():
          result = self.alphaBetaMinimax(state.generateSuccessor(player, action), depth, player + 1, alpha, beta)
        else:
          result = self.alphaBetaMinimax(state.generateSuccessor(player, action), depth - 1, 0, alpha, beta)
        if minAction > result:
          minAction = result
        beta = min(beta, minAction)
        if beta <= alpha:
          break
      return minAction

######################################################################################
# Problem 3b: implementing expectimax

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (problem 3)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """

    # BEGIN_YOUR_CODE (our solution is 25 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function

def intersectionEvaluationFunction(state):
  """
    @author: Jake Sage
    Evaluation function that attempts to take the safety of
    intersections into account. This tries to ensure that
    Pac-Man is the closest player to at least one intersection.
    This is meant to keep Pac-Man in situations where it always
    has an escape route, but reliance on manhattan distance
    and the fact that the rule that Pac-Man may not enter the
    Ghost House is not enforced in this implementation means
    this is better in theory than in practice.
  """
  pacmanPosition = state.getPacmanPosition()

  unsafeIntersectionPenalty = -1000
  for intersection in state.getIntersections():
    intersectionIsSafe = True
    pacmanDistance = manhattanDistance(pacmanPosition, intersection)
    for ghost in state.getGhostPositions():
      ghostDistance = manhattanDistance(ghost, intersection)
      if ghostDistance < pacmanDistance + 2:
        intersectionIsSafe = False
        break
    if(intersectionIsSafe):
      unsafeIntersectionPenalty = 0
      break
  return unsafeIntersectionPenalty

def foodEvaluationFunction(state):
  """
    @author: Jake Sage
    Pretty simple. Apply a penalty for being far away
    from food. This lets Pac-Man work towards food
    that isn't immediately visible within the depth
    it searches.
  """
  pacmanPosition = state.getPacmanPosition()
  foodPenalty = 0
  foodPositions = state.getFood()
  for x in range(state.data.layout.width):
    for y in range(state.data.layout.height):
      if(foodPositions[x][y]):
        foodPenalty += manhattanDistance(pacmanPosition, [x, y])

  return -1 * (foodPenalty / 4)

def betterEvaluationFunction(state):
  """
    @author: Jake Sage
    aggregate of all my evaluation functions
  """
  return state.getScore() + foodEvaluationFunction(state) + intersectionEvaluationFunction(state)

# Abbreviation
better = betterEvaluationFunction
