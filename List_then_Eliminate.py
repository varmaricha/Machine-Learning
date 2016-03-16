import StringIO
from collections import OrderedDict
import json
import sys
import numpy as np

f = open("4Cat-Train.labeled", "r")   
f1= open(sys.argv[1], "r")


def perm(n):
    if not n:
        return

    for i in xrange(2**n):
        s = bin(i)[2:]
        s = "0" * (n-len(s)) + s
        yield s

lookup= list(perm(16))


high=0
low=0


X=[['Male', 'Young', 'Yes', 'Yes'],
['Male', 'Young', 'Yes', 'No'],
['Male', 'Young', 'No', 'Yes'],
['Male', 'Young', 'No', 'No'],
['Male', 'Old', 'Yes', 'Yes'],
['Male', 'Old', 'Yes', 'No'],
['Male', 'Old', 'No', 'Yes'],
['Male', 'Old', 'No', 'No'],
['Female', 'Young', 'Yes', 'Yes'],
['Female', 'Young', 'Yes', 'No'],
['Female', 'Young', 'No', 'Yes'],
['Female', 'Young', 'No', 'No'],
['Female', 'Old', 'Yes', 'Yes'],
['Female', 'Old', 'Yes', 'No'],
['Female', 'Old', 'No', 'Yes'],
['Female', 'Old', 'No', 'No']]

nX=len(X)
print nX

nC=pow(2,16)
print nC

l=[]

for line in f.readlines():
    s=line
    k=s.replace("\r\n","")
    g=k.split("\t")
    g=[i.split(' ')[1] for i in g]
    if g[-1]=='low':
    g[-1]='0'
    else:
    g[-1]='1'
   
    
    for i in range(0,16):
    
    if g[0:4]==X[i][0:4]:  
            
            for j in lookup:
        
        if j[i]!=g[-1]:
           l.append(j)
         
VS=[x for x in lookup if x not in l]
                
print len(VS)

for line in f1.readlines():
    s=line
    k=s.replace("\r\n","")
    g=k.split("\t")
    g=[i.split(' ')[1] for i in g]
    if g[-1]=='low':
    g[-1]='0'
    elif g[-1]=='high':
    g[-1]='1'

    
    for i in range(0,16):
    if g[0:4]==X[i][0:4]:  
            for j in VS:
        if j[i]=='1':
            high=high+1
        else:
            low=low+1
    else:
            pass
    print high,low
    high=0
    low=0


 

f.close()
f1.close()
