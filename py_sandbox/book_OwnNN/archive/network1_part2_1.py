'''
Author: Kris Gonzalez
DateCreated: 190213
Objective: follow along in "make your own neural network" and make a self-made
    network.
    
NOTES:
    * sigmoid function: y = 1/(1+exp(-x))
'''
import numpy as np
# import matplotlib.pyplot as plt
import time

class NeuralNetwork:
    def __init__(self,inputnodes,hiddennodes,outputnodes,learningrate):
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes
        self.lr = learningrate
        self.wih = np.random.rand(self.hnodes,self.inodes)-0.5
        self.who = np.random.rand(self.onodes,self.hnodes)-0.5
        
        # scipy.special.expit replacement
        self.activation_function = lambda x:1/(1+np.exp(-np.array(x))) 

    def train(self,inputs_list,targets_list):
        # train network
        # prepare input arguments
        inputs = np.array(inputs_list,ndmin=2).T # not sure why T or ndmin
        targets = np.array(targets_list,ndmin=2).T # not sure why T or ndmin
        
        
        # signals into hidden layer
        hidden_inputs  = np.dot(self.wih,inputs)
        #signals leaving hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # signals into output layer
        final_inputs = np.dot(self.who,hidden_outputs)
        final_outputs = self.activation_function(final_inputs)      
        
        # do some backpropagation / SGD solving:
        # error is (target-actual)
        output_errors=targets-final_outputs
        
        # hidden layer error gets split by weights
        hidden_errors = np.dot(self.who.T,output_errors)
        
        # update weights for links between hidden and output layers
        # kjg190304: remember, THIS IS THE KEY LINE
        self.who +=self.lr*np.dot( (output_errors * final_outputs * (1.0-final_outputs) ), np.transpose(hidden_outputs) )
        # update weights for links between input and hidden layers
        self.wih +=self.lr*np.dot( (hidden_errors * hidden_outputs *(1.0-hidden_outputs)), np.transpose(inputs)) 

    def query(self,inputs_list):
        # test network on something
        
        # prepare input arguments
        inputs = np.array(inputs_list,ndmin=2).T # not sure why T or ndmin
        
        # signals into hidden layer
        
        hidden_inputs  = np.dot(self.wih,inputs)
        #signals leaving hidden layer
        hidden_outputs = self.activation_function(hidden_inputs)
        
        # signals into output layer
        final_inputs = np.dot(self.who,hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        return final_outputs
        
# class NeuralNetwork


# run if main program
if(__name__=='__main__'):

    # NETWORK INITIALIZATION ===============================
    print('Starting network')
    i_n=784 # affected by input data
    h_n=200 # this value is arbitrary
    o_n=10  # affected by output data
    LR=0.1  # this value is arbitrary
    nn=NeuralNetwork(i_n,h_n,o_n,LR)
    
    # DATA LOADING =========================================
    print('will load data')
    # format labels and answers as needed to be read by network
    dataset=[]
    for irow in open('mnist_5k.csv'):
        iraw=irow.strip().split(',')
        ival=int(iraw[0])
        
        # don't need to reshape, but do need to remap to 0.01-0.99
        iimg=(.98/255)*(np.array(iraw[1:]).astype(float))+.01 
        ians=np.zeros(10)+0.01 # initialize all values as "low"
        ians[ival]=0.99 # set location of answer to be the "high" value
        dataset.append([iimg,ians]) # aka inputs and targets
    # forloop
    print('done')
    # split dataset into training and validation
    ntrain=4500
    ds_train=dataset[:ntrain]
    ds_test =dataset[ntrain:] 

    # TRAINING PHASE =======================================
    # start of training (note: about 1130samples/second at 100 hidden nodes. 
    #   about 54s to train 60k)
    t0=time.time()
    for idat in ds_train:
        nn.train(*idat)
    time_train=time.time()-t0
    print('time to train:',time_train)
    print('number of training samples:',len(ds_train))
    print('samples/second in training:',len(ds_train)/time_train)
    
    # TESTING PHASE ========================================
    # at this point, need to actually "score" the networkn=0
    scorecard=[] # append 1 if right, 0 if wrong
    for idat in ds_test:
        answer=np.argmax(idat[1])   # load ground truth answer
        pred_raw=nn.query(idat[0])  # get raw values from network
        predict=np.argmax(pred_raw) # interpret prediction
        scorecard+= [1] if(answer==predict) else [0] # append answer
        # import ipdb;ipdb.set_trace()
    # once the test set has been iterated through, get (%) correct as score:
    print('network performance:',sum(scorecard)/len(scorecard))
    # import ipdb;ipdb.set_trace()

# eof
