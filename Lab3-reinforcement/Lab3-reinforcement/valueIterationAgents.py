# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for iteration in range(self.iterations):
            #The self.values will be changed in the iteration
            newValue = util.Counter()
            #oldValues = self.values.copy()
            for state in self.mdp.getStates():
                #The terminal state will get no possible action, so, just continu to do next loop
                if self.mdp.isTerminal(state): continue
                #Get the q-value list for every aciton in this state
                valueList = [self.computeQValueFromValues(state,action) for action in self.mdp.getPossibleActions(state)]
                '''
                #update the value in counter with the max value in all possible aciton
                valueList = []
                for action in self.mdp.getPossibleActions(state):
                    #This part of logic I have tried it work
                    #Then, I optimize and replace this part with the function computeQValueFromValues
                    ''
                    #Get the next state and prob by the getTransionStatesAndProbs
                    transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state,action)
                    #initialize the value with 0 for next state value
                    value = 0
                    for stateAndProbs in transitionStatesAndProbs:
                        nextState = stateAndProbs[0]
                        prob = stateAndProbs[1]
                        reward = self.mdp.getReward(state, action, nextState)
                        #Using the formula to get the sum of the value for current aciton
                        value += prob * (reward + self.discount * oldValues[nextState])
                    #Recording all action value for one state
                    ''
                    value = self.computeQValueFromValues(state,action)
                    valueList.append(value)
                '''
                #update the self.values with max value in the value list.
                newValue[state] = max(valueList)
            self.values = newValue
            #self.values[state] = max(valueList)

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #Get the next state and prob by the getTransionStatesAndProbs
        transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state,action)
        #initialize the Q-value with 0 for the state value
        QValue = 0
        for stateProb in transitionStatesAndProbs:
            nextState = stateProb[0]
            prob = stateProb[1]
            reward = self.mdp.getReward(state, action, nextState)
            #Using the formula to compute the each Q-value for each possible action
            #And, sum them up for one this aciton
            QValue += prob * (reward + self.discount * self.values[nextState])
        return QValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #Terminal state will return None
        if self.mdp.isTerminal(state): return None
        actions = self.mdp.getPossibleActions(state)
        
        #list comprehension
        #valueAction_list will be [(QValue, action),(Qvalue, aciton),(...),(...)....]
        valueAction_list = [(self.computeQValueFromValues(state, action), action) for action in actions]
        #The comment is about loop for above one code
        '''
        valueAction_list = []
        for action in actions:
            valueAction_list.append(self.computeQValueFromValues(state, action))
        '''
        #Find the best value and action by using the max function with key as valueAction_list[0].
        best_valueAction = max(valueAction_list, key = lambda valueAction_list: valueAction_list[0])
        #Then, return the aciton in the best_valueAction(value, action)
        return best_valueAction[1]
        
        #This part of logic code I tried before, it's worked
        #But, I optimize and repalce it with above part of logic code
        '''
        bestValue = -999999
        bestAction = None
        for action in actions:
            value = self.computeQValueFromValues(state, action)
            if bestValue < value: 
                bestValue = value
                bestAction = action
        return bestAction
        '''

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)
        #print(self.mdp.getStates())

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        #init the index with -1 for state list
        index = -1
        states = self.mdp.getStates()
        for iteration in range(self.iterations):
            index += 1
            #Prevent the index extend the max number of state
            if index == len(states): index =0
            #print("index", index)
            state = states[index]
            #Terminal state will just get next iteration
            if state == 'TERMINAL_STATE': continue
            action = self.computeActionFromValues(state)
            #update the self value to the best action q-value
            self.values[state] = self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)
    
    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        #Compute predecessors of all states.
        predecessors = {}
        for state in self.mdp.getStates():
            actions = self.mdp.getPossibleActions(state)
            for action in actions:
                for nextStateProb in self.mdp.getTransitionStatesAndProbs(state,action):
                    if nextStateProb[1] > 0: 
                        nextState = nextStateProb[0]
                        if not nextState in predecessors.keys(): 
                            predecessors[nextState] = set()
                        predecessors[nextState].add(state)
                        
        #Initialize an empty priority queue
        queue = util.PriorityQueue()
        #For each non-terminal state s
        for state in self.mdp.getStates():
            #Find the all q-value for every 
            possibleActions = self.mdp.getPossibleActions(state)
            qValue = [self.computeQValueFromValues(state, action) for action in possibleActions]
            #For the terminal state, it will get the 0 value in qValue list, so, it will be 0 in the list
            if len(qValue) == 0: qValue = [0]
            #Find the absolute value of the difference
            diff = abs(self.values[state] - max(qValue))
            queue.push(state, -diff)

        for itertion in range(self.iterations):
            #If the priority queue is empty, then terminate.
            if queue.isEmpty(): break
            #Pop a state s off the priority queue.
            state = queue.pop()
            #Update the value of s (if it is not a terminal state) in self.values
            possibleActions = self.mdp.getPossibleActions(state)
            qValue = [self.computeQValueFromValues(state, action) for action in possibleActions]
            if len(qValue) == 0: qValue = [0]
            self.values[state] = max(qValue)

            #For each predecessor p of s
            for preState in predecessors[state]:
                possibleActions = self.mdp.getPossibleActions(preState)
                qValue = [self.computeQValueFromValues(preState, action) for action in possibleActions]
                if len(qValue) == 0: qValue = [0]
                #Find the absolute value of the difference
                diff = abs(self.values[preState] - max(qValue))
                if diff > self.theta: 
                    queue.update(preState,-diff)
    

