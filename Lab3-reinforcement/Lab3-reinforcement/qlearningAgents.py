# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.qValues = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        #No state, return 0.0
        if state == None: return 0
        #Return Q(state, action)
        return self.qValues[(state, action)]
        


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        actions = self.getLegalActions(state)
        #No legal actions, return 0.0
        if len(actions) == 0:
          return 0.0
        #Get the list for all q-value
        qValue_list = []
        for action in actions:
          qValue_list.append(self.getQValue(state, action))
        #return the max value in the qValue list
        return max(qValue_list)

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        actions = self.getLegalActions(state)
        #No legal actions, return None
        if len(actions) == 0:
          return None

        #Get the q-value list with the all legal action's tuple (value, action)
        qValue_list = [(self.getQValue(state, action), action) for action in actions]
        #The below comment is about loop for above one code
        '''
        qValue_list = []
        for action in actions:
          value = self.getQValue(state, action)
          qValue_list.append((value, action))
        '''
        #Get the the max point that has highest value by comparing the qValue_list[0]
        maxPoint = max(qValue_list, key = lambda qValue_list: qValue_list[0])  
        #return the action in the maxPoint(value,action)
        return maxPoint[1]


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        #The no legal actions, return None
        if len(legalActions) == 0:
          action = None
        #Else the util.flipCoin function to decide to choose the risk action or not
        else:
          #True for risk action which select action from all legal actions
          #False for high q-value action
          if util.flipCoin(self.epsilon):
            action = random.choice(legalActions)
          else:
            action = self.computeActionFromQValues(state)
        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        #Using the Q-Learning formula to compute the q-Value for each state and action, and update the value to self's counter
        qValue_curr = self.getQValue(state, action)
        first_part = self.alpha * (reward + self.discount * self.computeValueFromQValues(nextState))
        second_part = (1 - self.alpha) * qValue_curr
        self.qValues[(state, action)] = first_part + second_part

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        w = self.weights
        featureVector = self.featExtractor.getFeatures(state, action)
        #Multiplication of two counters will gives the dot product of their vectors where each unique label is a vector element
        #The counter multiplication defined in the util
        qValue = w * featureVector
        return qValue

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        #Get the max q-value in every legal actions for next state
        max_qValue_next = self.computeValueFromQValues(nextState)
        #Get the q-value at the current state with the current action
        qValue = self.getQValue(state, action)
        #Compute the difference value in the equation. The difference value is unchanged value
        difference = (reward + self.discount * max_qValue_next) - qValue
        #Compute the every weight for every feature.
        featureVector = self.featExtractor.getFeatures(state, action)
        for feature in featureVector:
          w = self.weights[feature] + self.alpha * difference * featureVector[feature]
          self.weights[feature] = w

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            #print(self.weights)
            pass
