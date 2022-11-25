# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    fringe = util.Stack()
    fringe.push(problem.getStartState())
    closedSet = []
    temps = util.Stack()
    path = []
    allNodes = []
    while(not fringe.isEmpty()):
        state = fringe.pop()
        if (state in closedSet): continue
        if (problem.isGoalState(state)): return path
        closedSet.append(state)
        successors = problem.getSuccessors(state)
        successorsState = []
        for successor in successors:
            if (successor[0] not in closedSet): 
                fringe.push(successor[0])
                successorsState.append(successor[0])
                temps.push(successor)               
                allNodes.append(successor[0])       #Need to be changed according to the strategy

        temp = temps.pop()
        if (all(elem in closedSet for elem in successorsState)): 
            while(allNodes.pop() != temp[0]): path.pop()
            #print("find a no more leaf node")
        
        path.append(temp[1])
        """
        print("allNodes: ", allNodes)
        print("state: ", state)
        print("temp: ", temp)
        print("path: ", path)
        print("  ")
        """
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    fringe.push((problem.getStartState(), []))
    closedSet = []
    while(not fringe.isEmpty()):
        state, paths = fringe.pop()
        if (state in closedSet): continue
        if (problem.isGoalState(state)): return paths
        closedSet.append(state)
        #print(state)
        #print(paths)
        successors = problem.getSuccessors(state)
        for nextState, dir, cost in successors:
            if (nextState not in closedSet): 
                fringe.push((nextState,paths + [dir])) 
        
    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    fringe.push((problem.getStartState(), [], 0),0)
    closedSet = []
    while(not fringe.isEmpty()):
        state, paths, cost = fringe.pop()
        if (state in closedSet): continue
        if (problem.isGoalState(state)): 
            print("UCS:",len(paths))
            return paths
        closedSet.append(state)
        successors = problem.getSuccessors(state)
        for nextState, dir, nextCost in successors:
            if (nextState not in closedSet): 
                nextCost += cost
                fringe.push((nextState,paths + [dir], nextCost),nextCost) 
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    fringe = util.PriorityQueue()
    fringe.push((startState, [], 0),heuristic(startState,problem))
    closedSet = []
    while(not fringe.isEmpty()):
        state, paths, cost = fringe.pop()
        if (state in closedSet): continue
        if (problem.isGoalState(state)): 
            print("aStart: " , len(paths))
            return paths
        closedSet.append(state)
        successors = problem.getSuccessors(state)
        for nextState, dir, nextCost in successors:
            if (nextState not in closedSet): 
                nextCost += cost
                fringe.push((nextState, paths + [dir], nextCost), nextCost + heuristic(nextState,problem)) 
    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
