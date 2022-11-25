# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        #print(legalMoves)
        #print(scores)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        #newGhostStates = successorGameState.getGhostStates()
        #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #Get the list for all true dot position
        foodList = list(newFood)
        rowCount = 0
        colCount = 0
        newFoodList = []
        for row in foodList:
            for ele in row:
                if ele: newFoodList.append((rowCount,colCount))
                colCount += 1
            colCount = 0
            rowCount += 1

        #Find the closest dot with the Pacman
        minDistance = -1
        for foodPos in newFoodList:
            distance = manhattanDistance(foodPos,newPos)
            if minDistance == -1: minDistance = distance
            else: minDistance = min(minDistance,distance)

        #In case, Pacman is too close with the ghost
        allGhosts = successorGameState.getGhostPositions()
        for ghost in allGhosts:
            if(manhattanDistance(newPos,ghost)) < 2:
                return -1000000
        #print("successorGameStare: ",successorGameState)
        #print("newPos: ",newPos)
        #print("newFood: ",newFood)
        #print("newGhostStates:",newGhostStates)
        #print("newScaredTimes:" ,newScaredTimes)
        #print(successorGameState.getScore())
        #print(" ")
        #minDistance = minDistance * 10
        #print(minDistance)
        #print(successorGameState.getScore())
        #print("")
        
        "*** YOUR CODE HERE ***"
        return successorGameState.getScore() + 1/minDistance

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

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #pacmanAction = gameState.getLegalActions(0)
        #agentNum = gameState.getNumAgents()

        currDepth = 0
        nextAgent = "max"
        action = self.max_value(gameState,currDepth, nextAgent)[0]
        return action
        #util.raiseNotDefined()
    
    def max_value(self,states,currDepth,nextAgent):
        #print("max depth:", currDepth)
        agentIndex = currDepth % states.getNumAgents()
        #print("max agent index: ", agentIndex)
        #print("agentIndex: ", agentIndex)
        nextAgent = "min"
        pacmanActions = states.getLegalActions(0)
        #valueList = []
        bestValue =("",-99999)
        for action in pacmanActions:
            actionState = states.generateSuccessor(agentIndex, action)
            value = (action,self.value(actionState,currDepth + 1,nextAgent))
            if bestValue[1] < value[1]: bestValue = value
        """
        bestValue = valueList
        for value in valueList:
            if bestValue[1] < value[1]: bestValue = value 
        """
        return bestValue
    
    def min_value(self,states,currDepth,nextAgent):
        #print("min depth: ", currDepth)
        agentIndex = currDepth % states.getNumAgents()
        #print("agentIndex: ", agentIndex)
        if agentIndex == 0: nextAgent = "max"
        agentActions = states.getLegalActions(agentIndex)
        #valueList = []
        bestValue = (" ",99999)
        for action in agentActions:
            actionState = states.generateSuccessor(agentIndex,action)
            value = (action, self.value(actionState,currDepth + 1, nextAgent))
            #print("11",bestValue[1])
            #print("22",value)
            if bestValue[1] > value[1]: bestValue = value
            #valueList.append((action, self.value(actionState,currDepth + 1, nextAgent)))

        #bestValue = valueList[0]
        #print("best value:",bestValue)
        #print(type(bestValue[0][1]))
        #for value in valueList:
            #if bestValue[1] < value[0][1]: bestValue = value 
        return bestValue

    def value(self,state,currDepth,nextAgent):
        limitDepth = self.depth * state.getNumAgents()
        if state.isWin() or state.isLose() or (currDepth == limitDepth):
            return scoreEvaluationFunction(state)
        if (currDepth % state.getNumAgents()) == 0: nextAgent = "max"
        if nextAgent ==  "max": return self.max_value(state,currDepth,nextAgent)[1]
        else: return self.min_value(state, currDepth,nextAgent)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        currDepth = 0
        nextAgent = "max"
        beta = 99999
        alpha = -99999
        action = self.max_value(gameState,currDepth, nextAgent,alpha,beta)[0]
        return action
        #util.raiseNotDefined()

    def value(self,state,currDepth,nextAgent,alpha,beta):
        limitDepth = self.depth * state.getNumAgents()
        if state.isWin() or state.isLose() or (currDepth == limitDepth):
            return scoreEvaluationFunction(state)
        if (currDepth % state.getNumAgents()) == 0: nextAgent = "max"
        if nextAgent ==  "max": return self.max_value(state,currDepth,nextAgent,alpha,beta)[1]
        else: return self.min_value(state, currDepth,nextAgent,alpha,beta)[1]
    
    def max_value(self,state,currDepth,nextAgent,alpha,beta):
        agentIndex = currDepth % state.getNumAgents()
        nextAgent = "min"
        pacmanActions = state.getLegalActions(agentIndex)
        bestValue =("",-99999)
        for action in pacmanActions:
            actionState = state.generateSuccessor(agentIndex, action)
            value = (action,self.value(actionState,currDepth + 1,nextAgent,alpha,beta)) 
            #print(value[1])
            if bestValue[1] < value[1]: bestValue = value
            if bestValue[1] > beta: return bestValue
            #alpha = max(alpha,bestValue[1])
            #print("Max:", alpha," ",bestValue[1])
            if alpha < bestValue[1]: alpha = bestValue[1]
            #print(alpha)
        return bestValue
    
    def min_value(self,state,currDepth,nextAgent,alpha,beta):
        agentIndex = currDepth % state.getNumAgents()
        if agentIndex == 0: nextAgent = "max"
        agentActions = state.getLegalActions(agentIndex)
        bestValue = (" ",99999)
        for action in agentActions:
            actionState = state.generateSuccessor(agentIndex,action)
            value = (action, self.value(actionState,currDepth + 1, nextAgent,alpha,beta))
            #print(value[1])
            if bestValue[1] > value[1]: bestValue = value
            if bestValue[1] < alpha: return bestValue
            #beta = min(beta,bestValue[1])
            #print("Min:", beta," ",bestValue[1])
            if beta > bestValue[1]: beta = bestValue[1]
            #print(beta)
        return bestValue
    

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        currDepth = 0
        nextAgent = "max"
        action = self.max_value(gameState,currDepth, nextAgent,"action")[0]
        return action
        #util.raiseNotDefined()

    def value(self,state,currDepth,nextAgent,pacmanAction):
        limitDepth = self.depth * state.getNumAgents()
        if state.isWin() or state.isLose() or (currDepth == limitDepth):
            return scoreEvaluationFunction(state)
        if (currDepth % state.getNumAgents()) == 0: nextAgent = "max"
        if nextAgent ==  "max": return self.max_value(state,currDepth,nextAgent,pacmanAction)[1]
        else: return self.exp_value(state, currDepth,nextAgent,pacmanAction)[1]
    
    def max_value(self,state,currDepth,nextAgent,pacmanAction):
        agentIndex = currDepth % state.getNumAgents()
        nextAgent = "exp"
        pacmanActions = state.getLegalActions(agentIndex)
        bestValue =("",-99999)
        for action in pacmanActions:
            actionState = state.generateSuccessor(agentIndex, action)
            value = (action,self.value(actionState,currDepth + 1,nextAgent,action)) 
            if bestValue[1] < value[1]: bestValue = value
        return bestValue

    def exp_value(self,state,currDepth,nextAgent,pacmanAction):
        agentIndex = currDepth % state.getNumAgents()
        if agentIndex == 0: nextAgent = "max"
        agentActions = state.getLegalActions(agentIndex)
        score = 0
        #bestValue = (" ",99999)
        for action in agentActions:
            actionState = state.generateSuccessor(agentIndex,action)
            value = self.value(actionState, currDepth + 1, nextAgent, pacmanAction)
            score += value / len(agentActions)
        return (pacmanAction,score)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()
    value = 0
    pacmanPosition = currentGameState.getPacmanPosition()
    ghostPositions = currentGameState.getGhostPositions()

    #Take care abou the distance between ghost and pacman, if it is too close, return small number 
    ghostDis = 10
    for ghostPos in ghostPositions:
        ghostDis = manhattanDistance(ghostPos,pacmanPosition)
        if ghostDis < 2: return -99999
    value += ghostDis

    #Get the min distance between pacman and dot
    foods = currentGameState.getFood()
    foodList = foods.asList()
    foodArray = []
    for foodPos in foodList:
        foodArray.append(manhattanDistance(foodPos,pacmanPosition))
    minFoodDistance = min(foodArray)
    value += minFoodDistance

    if currentGameState.isWin(): value += 99999
    if currentGameState.isLose: value -= 99999

    return value
    
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
