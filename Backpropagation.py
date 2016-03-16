import StringIO
import sys
import csv
import math
import numpy as np
import scipy as sp
from itertools import groupby
import collections
import copy
from scipy.special import expit

f1 = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'r')
table = [line.strip().split(',') for line in f1.readlines()]
table2 = [line.strip().split(',') for line in f2.readlines()]

eta=0.01

def RepresentsFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False


def mod_input(table):
    table_ = np.ones((np.shape(table)))
    for i in range(len(table[0])):
        if RepresentsFloat(table[1][i])==True:
            s=0
            for j in range(1,len(table)):
                table_[j][i]=float(table[j][i])

            if table[0][i]=='Year':
                min_=1900
                max_=2000
                range_=max_-min_

            if table[0][i]=='Length':
                min_=0
                max_=7
                range_=max_-min_

            for j in range(1,len(table)):
                table_[j][i]=float(table_[j][i]-min_)/range_

        if RepresentsFloat(table[1][i])==False:
            for j in range(1,len(table)):
                if table[j][i]=='yes':
                    table_[j][i]=1.0
                if table[j][i]=='no':
                    table_[j][i]=0.0
    return table_

table=mod_input(table)
table2=mod_input(table2)
table=np.array(table)
table2=np.array(table2)

ones=np.ones((len(table),1))
table=np.hstack((ones,table))
ones=np.ones((len(table2),1))
table2=np.hstack((ones,table2))
#print table[4][:]
    
#########################################################    

class Net(object):
    def __init__(self,table,table2,eta,num_inputs,num_hidden_neurons,num_outputs):
        self.weights1= np.random.uniform(-0.05,0.05,(num_hidden_neurons,num_inputs))
        self.weights2= np.random.uniform(-0.05,0.05,(num_outputs,num_hidden_neurons))
        self.inputs= np.empty((num_inputs,1))
        self.t_k= 0
        self.table=table
        self.table2=table2
        self.n_h=num_hidden_neurons
        self.n_i=num_inputs
        self.n_o=num_outputs
        return

    def feedforward(self):
        z_h=np.matrix(self.weights1)*np.transpose(np.matrix(self.inputs))
        #print z_h
        o_h=self.sigmoid(z_h)
        z_o=np.matrix(self.weights2)*(np.matrix(o_h))
        o_o=self.sigmoid(z_o)
        return o_o,o_h

    def Backpropagation(self,o_o,o_h):     ##pass in the output of the feedforward network
        del_k=o_o*(1-o_o)*(self.t_k-o_o)
        del_wk=eta*del_k[0,0]*o_h
    #    self.weights2=np.transpose(self.weights2)
        self.weights2+=np.transpose(del_wk)
        del_h=np.empty([self.n_h,1])
        for i in range(self.n_h):
            del_h[i]=o_h[i,0]*(1-o_h[i,0])*self.weights2[0,i]*del_k[0,0]
        del_wh=eta*np.matrix(del_h)*np.matrix(self.inputs)
        self.weights1+=del_wh
        return

    def sigmoid(self,y):
        return expit(y)

    def train(self):
        iterations = 0
        prev_err=10000000
        while(True):
            iterations+=1
            if(iterations >= 1000):
                break
            for i in self.table[1:,:]:
                self.inputs=np.transpose(i[:-1])
                self.t_k=i[-1]
                o_o,o_h=self.feedforward()
                self.Backpropagation(o_o,o_h)
            tot_err = 0

            for i in self.table[1:,:]:

                self.inputs=np.transpose(i[:-1])
                self.t_k=i[-1]
                o_o,o_h=self.feedforward()
                err_ = np.square(self.t_k - o_o)
                tot_err += err_

            if tot_err<prev_err:
                print str(tot_err[0,0])
            prev_err=tot_err

        print 'TRAINING COMPLETED! NOW PREDICTING.'

        for i in self.table2[1:,:]:
            self.inputs=np.transpose(i)
            o_o,o_h=self.feedforward()
            if o_o<0.5:
                print 'no'
            else:
                print 'yes'



        return


NN=Net(table,table2,eta,len(table[0])-1,16,1)
NN.train()
