from pybrain.structure.modules import Module
from pybrain.rl.learners.valuebased.interface import ActionValueInterface
from scipy import argmax, array, r_, asarray, where
from random import choice
from math import exp

class ActionValueLinear(Module, ActionValueInterface):
    
    def __init__(self, dimState, numActions, name = None):
        Module.__init__(self, dimState, 1, name)
        self.coefficients = [0 for x in range(30)];
        self.numActions = numActions

    def _forwardImplementation(self, inbuf, outbuf):
        outbuf[0] = self.getMaxAction(asarray(inbuf));

    def getMaxAction(self, state):
        return argmax(self.getActionValues(state));

    def getActionValues(self, state):
        values = array([self.getValue(state, i) for i in range(self.numActions)])
        return values

    def getValue(self, state, action):
        Q_value = sum([self.coefficients[i] * featureValue(state, action)[i] for i in range(30)]);  
        return Q_value


def featureValue(state, action):
    base_value = [1];
    s = [-1, 0, 1];
    th = [-0.852, 0, 0.852];
    
    for i in range(3):
        for j in range(3):
            base_value.append(exp(-((state[0]-s[i])**2 + (state[2]-th[j])**2)/2));

    feature_value = [0 for x in range(30)];
    action = int(round(action));
    feature_value[action*10:(action+1)*10] = base_value;
    return feature_value;
    
