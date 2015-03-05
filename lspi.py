from numpy import *
from pybrain.rl.learners.valuebased.valuebased import ValueBasedLearner
from pybrain.rl.learners.valuebased.ActionValueLinear import featureValue



class LSPI(ValueBasedLearner):
    """ least squares policy iteration """

    def __init__(self, maxEpochs = 20):
        ValueBasedLearner.__init__(self)
        self.gamma = 0.9;
        self.maxEpochs = maxEpochs
        self.A = eye(30)*0.01;
        self.b = zeros((30,1));

    def learn(self):
        # using another module instead of neural network!!
        self.A = eye(30)*0.1;
        self.b = zeros((30,1));
        for seq in self.dataset:
            lastexperience = None;
            for state, action, reward in seq:
                if not lastexperience:
                    # delay each experience in sequence by one
                    lastexperience = (state, action, reward)

                (state_, action_, reward_) = lastexperience
                phi_ = array(featureValue(state_, action_));
                phi = array(featureValue(state, self.module.getMaxAction(state)));
                self.A = self.A + dot(phi_, (phi_ - self.gamma*phi).T);
                self.b = self.b + phi_ * reward_;


        w = dot(linalg.inv(self.A), self.b);
        self.module.coefficents = w.reshape(-1).tolist();   
    
