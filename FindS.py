import StringIO
from collections import OrderedDict
import json
import sys

f = open("9Cat-Train.labeled", "r")   
f1= open("partA4.txt", "w")
f2= open("9Cat-Dev.labeled", "r")
f3= open(sys.argv[1], "r")

ninputs=512
print ninputs

cspace=155
print cspace

hspace=19684
print hspace

step=30
count=0
correct=0
wrong=0

h=['null','null','null','null','null','null','null','null','null']
                            
for line in f.readlines(): 
    
    count=count+1 
    s=line
    k=s.replace("\r\n","")
    g=k.split("\t")
    g=[i.split(' ')[1] for i in g]
    
    if g[-1]=="high":
    g9=g[0:-1]

        for i in range(0,len(g9)):

        if h[i]=="null" and h[i]!=g9[i]:
        h[i]=g9[i]

        elif h[i]==g9[i]:
        pass

        else:
        h[i]='?'
     
    if (count%30) == 0:
        
    p=str(h)
        p=p.replace("[","")
    p=p.replace("]","")
    p=p.replace("'","")
    p=p.replace(", ","\t")
           
    f1.write(p+'\n')



for line in f2.readlines():
    s=line
    k=s.replace("\r\n","")
    g=k.split("\t")
    g=[i.split(' ')[1] for i in g]
    g9=g[0:-1]

    for i in range(0,len(g9)):
    
    if h[i]=='?':
        result="high"
    elif h[i]==g9[i]:
        result="high"
    else:
        result="low"
        break 

    g9.append(result)
    if g[-1]==g9[-1]:
    correct=correct+1
    else:
    wrong=wrong+1

    
    p=str(g9)
    p=p.replace("[","")
    p=p.replace("]","")
    p=p.replace("'","")
    p=p.replace(", ","\t")

mcr= wrong/float(wrong+correct)
print mcr


for line in f3.readlines():
    s=line
    k=s.replace("\r\n","")
    g=k.split("\t")
    g=[i.split(' ')[1] for i in g]
    g9=g[0:-1]

    for i in range(0,len(g9)):
    
    if h[i]=='?':
        result="high"
    elif h[i]==g9[i]:
        result="high"
    else:
        result="low"
        break 

    
    print result
  

f.close()
f1.close()
f2.close()
f3.close()
