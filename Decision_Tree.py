import StringIO
import sys
import csv
import math
import numpy as np
from itertools import groupby
import collections
import copy

class Node(object):

    def __init__(self):
        self.split_variable = None
        self.left_child = None
        self.right_child = None

    def get_name(self):
        return 'Node'
    
    

class Leaf(object):
    def __init__(self):
        self.value = None

    def get_name(self):
        return 'Leaf'

###########################################

f1 = open(sys.argv[1], 'r')
#f1 = open("education_train.csv", 'r')
table = [line.strip().split(',') for line in f1.readlines()]

f2 = open(sys.argv[2], 'r')
#f2 = open("education_test.csv", 'r')
test_table = [line.strip().split(',') for line in f2.readlines()] 

###########################################
 
posList=['y','A','yes','before1950','morethan3min','fast','expensive','high','Two','large']
negList=['n','notA','no','after1950','lessthan3min','slow','cheap','low','MoreThanTwo','small']


mapper=[[' Anti_satellite_test_ban','y','n'],['Anti_satellite_test_ban','y','n'],[' Aid_to_nicaraguan_contras','y','n'],['Aid_to_nicaraguan_contras','y','n'],[' Mx_missile','y','n'],['Mx_missile','y','n'],[' Immigration','y','n'],['Immigration','y','n'],[' Superfund_right_to_sue','y','n'],['Superfund_right_to_sue','y','n'],[' Duty_free_exports','y','n'],['Duty_free_exports','y','n'],[' Export_south_africa','y','n'],['Export_south_africa','y','n'],['M1','A','notA'],['M2','A','notA'],['M3','A','notA'],['M4','A','notA'],['M5','A','notA'],['P1','A','notA'],['P2','A','notA'],['P3','A','notA'],['P4','A','notA'],['F','A','notA'],['year','before1950','after1950'],['solo','yes','no'], ['vocal','yes','no'],['length','morethan3min','lessthan3min'],['original','yes','no'],['tempo','fast','slow'],['folk','yes','no'],['classical','yes','no'],['rhythm' ,'yes','no'],['jazz','yes','no'],['rock','yes','no'],['buying','expensive', 'cheap'],['maint', 'high','low'],['doors','Two','MoreThanTwo'],['person','Two','MoreThanTwo'],['boot','large','small'],['safety','high','low']] 

posLabels=['yes','democrat','A']
negLabels=['no','republican','notA'] 

###########################################


king_keys=['0','0']



def getattrkeys(i,table):
    vals=[]

    for j in range(1,len(table)):
        vals.append(table[j][i])
 
                         
    counter=collections.Counter(vals)
    keys= counter.keys()
    return keys



def changeattrkeys(table):
    

    for i in range(0,len(table[0])-1):

        for j in range(1,len(table)):
            if (table[j][i]) in posList:
        table[j][i]='1'
        elif (table[j][i]) in negList:             
        table[j][i]='0'
   
        


def countlabels(labels,king_keys):
    
    freq0=0
    freq1=0
    for i in range(len(labels)):
    if labels[i]==king_keys[1]:
        freq1=freq1+1
    else:
        freq0=freq0+1
    freq=[freq1,freq0]
    return freq


def getentropy(_list):

    total=float(len(_list))
    types=list(set(_list))

    entropy=0

    for element in types:
    prob=list(_list).count(element)/total

        entropy+=prob*math.log(prob,2)

    return -1.0*entropy


def mutual_info(i,table):

    labels=[]
    freq=[]
    labelkeys=[]
    for n in range(1,len(table)):
        labels.append(table[n][-1])
 
    counter=collections.Counter(labels)

    freq= counter.values()
    labelkeys= counter.keys()


    Hlabels=getentropy(labels)
    
    l1=[]
    l2=[]
    

    for k in range(1,len(table)):
    if table[k][i]=='0':
        l1.append(table[k][-1])
    elif table[k][i]=='1':
        l2.append(table[k][-1])


    Hlabels1=getentropy(l1)
    Hlabels2=getentropy(l2)
    total=float(len(l1)+len(l2))
    p1=len(l1)/total
    p2=len(l2)/total

    I=Hlabels-(p1*Hlabels1)-(p2*Hlabels2)

    return I,freq,labelkeys

king_keys=changeattrkeys(table)

changeattrkeys(test_table)


#main####################################################

labels_table0=[]
for i in range(1,len(table)):
    labels_table0.append(table[i][-1])


counter_freq_table=collections.Counter(labels_table0)
freq_table=counter_freq_table.values()


sys.stdout.write(str('['+str(freq_table[1])+'+/'+str(freq_table[0])+'-]'))         #THIS IS FINAL PRINT (1)
print

Ilist=[]
bin1=[]
bin2=[]
s = []
for i in range(len(table[0])):
    s.append(table[0][i])
a = copy.deepcopy(s)

    
t1=[list(a)]
t2=[list(a)]



for i in range(0,len(table[0])-1):
   
    I,freq,labelkeys=mutual_info(i,table)
    Ilist.append(I)

max_value = max(Ilist)

max_index = Ilist.index(max_value)
 


if max_value <=0.1:
    
    node1=Leaf()

    if len(freq)==1:
    node1.value=labelkeys[0]
    elif len(freq)==0:

        pass
    else:
        sel=max(freq)
        selindex=freq.index(sel)
    node1.value=labelkeys[selindex]



else:
    

    for m in range(1,len(table)):     #changed here

    if table[m][max_index]=='1':         #MAJOR CHANGE HERE
        bin1.append(table[m][-1])
        s1=[]

        for i in range(len(table[m])):

            s1.append(table[m][i])

        a1 = copy.deepcopy(s1)

        t1.append(list(a1))


    else:
        bin2.append(table[m][-1])
        s2=[]
        for i in range(len(table[m])):
            s2.append(table[m][i])
        a2 = copy.deepcopy(s2)
        t2.append(list(a2))


 
   
    [l.pop(max_index) for l in t1]
    [l.pop(max_index) for l in t2]

    
    labels_t1=[0,0]
    labels_t2=[0,0]
 
    for element in bin1:
    if element in posLabels:
        labels_t1[0]+=1
    else:
        labels_t1[1]+=1

    for element in bin2:
    if element in posLabels:
        labels_t2[0]+=1
    else:
        labels_t2[1]+=1

    node1=Node()
    node1.split_variable = table[0][max_index]                 #Parent attribute name

    
    for i in range(len(mapper)):

        if mapper[i][0]==node1.split_variable:
        val1=mapper[i][1]
        val2=mapper[i][2]

    sys.stdout.write(str(node1.split_variable+' = '+val1+': ['+str(labels_t1[0])+'+/'+str(labels_t1[1])+'-]'))
    print
    
    
###################################


Ilist=[]
bin11=[]
bin12=[]

s1_ = []
for i in range(len(t1[0])):
    s1_.append(t1[0][i])
a1_ = copy.deepcopy(s1_)

    
t11=[list(a1_)]
t12=[list(a1_)]


for i in range(0,len(t1[0])-1):
    
    I,freq,labelkeys=mutual_info(i,t1)
    Ilist.append(I)

max_value = max(Ilist)

max_index = Ilist.index(max_value)



if max_value <=0.1:

    node2=Leaf()
    node1.left_child = node2

    if len(freq)==1:
    node2.value=labelkeys[0]
    elif len(freq)==0:

        pass
    else:
        sel=max(freq)
        selindex=freq.index(sel)
    node2.value=labelkeys[selindex]
#    print "Tree terminated"
    
    sys.stdout.write(str(node1.split_variable+' = '+val2+': ['+str(labels_t2[0])+'+/'+str(labels_t2[1])+'-]')) 
    print   

else:


    for m in range(1,len(t1)):


    if t1[m][max_index]=='1':
        s11=[]
        bin11.append(t1[m][-1])
        for i in range(len(t1[m])):
            s11.append(t1[m][i])
        a11 = copy.deepcopy(s11)
        t11.append(list(a11))


    else:
        bin12.append(t1[m][-1])
        s12=[]
        for i in range(len(t1[m])):
            s12.append(t1[m][i])
            a12 = copy.deepcopy(s12)
        t12.append(list(a12))


    [l.pop(max_index) for l in t11]
    [l.pop(max_index) for l in t12]


    node2=Node()
    node1.left_child = node2

    node2.split_variable = t1[0][max_index]         #Left child attribute name
    
    leaf1=Leaf()
    max11=max(bin11)
    leaf1.value=max11
    node2.left_child = leaf1

    leaf2=Leaf()
    max12=max(bin12)
    leaf2.value=max12  
    node2.right_child = leaf2  

# # # printing method # # # #

    labels_t11=[0,0]
    labels_t12=[0,0]
 
    for element in bin11:
    if element in posLabels:
        labels_t11[0]+=1
    else:
        labels_t11[1]+=1

    for element in bin12:
    if element in posLabels:
        labels_t12[0]+=1
    else:
        labels_t12[1]+=1


    for i in range(len(mapper)):

        if mapper[i][0]==node2.split_variable:
        val11=mapper[i][1]
        val12=mapper[i][2]

    sys.stdout.write(str('| '+node2.split_variable+' = '+val11+': ['+str(labels_t11[0])+'+/'+str(labels_t11[1])+'-]'))
    print
    sys.stdout.write(str('| '+node2.split_variable+' = '+val12+': ['+str(labels_t12[0])+'+/'+str(labels_t12[1])+'-]'))
    print  
    sys.stdout.write(str(node1.split_variable+' = '+val2+': ['+str(labels_t2[0])+'+/'+str(labels_t2[1])+'-]'))
    print 
  


##########################################



Ilist=[]
bin21=[]
bin22=[]

s2_ = []
for i in range(len(t1[0])):
    s2_.append(t1[0][i])
a2_ = copy.deepcopy(s2_)

    
t21=[list(a2_)]
t22=[list(a2_)]

for i in range(0,len(t2[0])-1):

    I,freq,labelkeys=mutual_info(i,t2)
    Ilist.append(I)

max_value = max(Ilist)

max_index = Ilist.index(max_value)


if max_value <=0.1:

    node3=Leaf()
    node1.right_child = node3

    if len(freq)==1:
    node3.value=labelkeys[0]
    elif len(freq)==0:
#    node3.value=None
        pass
    else:
        sel=max(freq)
        selindex=freq.index(sel)
    node3.value=labelkeys[selindex]
#    print "Tree terminated"


else:
    

    for m in range(1,len(t2)):


    if t2[m][max_index]=='1':
        s21=[]
        bin21.append(t2[m][-1])
        for i in range(len(t2[m])):
            s21.append(t2[m][i])
        a21 = copy.deepcopy(s21)
        t21.append(list(a21))


    else:
        bin22.append(t2[m][-1])
        s22=[]
        for i in range(len(t2[m])):
            s22.append(t2[m][i])
        a22 = copy.deepcopy(s22)
        t22.append(list(a22))


    [l.pop(max_index) for l in t21]
    [l.pop(max_index) for l in t22]


    node3=Node()
    node1.right_child = node3

    node3.split_variable = t2[0][max_index]    #Right child attribute name
   
    leaf3=Leaf()
    max21=max(bin21)
    leaf3.value=max21
    node3.left_child = leaf3

    
    leaf4=Leaf()
    max22=max(bin22)
    leaf4.value=max22 
    node3.right_child = leaf4   

# # # printing method # # # #

    labels_t21=[0,0]
    labels_t22=[0,0]
 
    for element in bin21:
    if element in posLabels:
        labels_t21[0]+=1
    else:
        labels_t21[1]+=1

    for element in bin22:
    if element in posLabels:
        labels_t22[0]+=1
    else:
        labels_t22[1]+=1


    for i in range(len(mapper)):

        if mapper[i][0]==node3.split_variable:
        val21=mapper[i][1]
        val22=mapper[i][2]

    sys.stdout.write(str('| '+node3.split_variable+' = '+val21+': ['+str(labels_t21[0])+'+/'+str(labels_t21[1])+'-]'))
    print
    sys.stdout.write(str('| '+node3.split_variable+' = '+val22+': ['+str(labels_t22[0])+'+/'+str(labels_t22[1])+'-]')) 
    print 
 



######  CLASSIFY  #######
 

def evaluate_tree(header, your_data, node):
    
    if node.get_name() == 'Leaf':
        return node.value

        

    else:
        for i in range(0,len(your_data)-1):

        if header[i]==node.split_variable and your_data[i]=='1':

                if node.left_child.get_name() == 'Node':
                    return (evaluate_tree(header,your_data, node.left_child))
                elif node.left_child.get_name() == 'Leaf':

                    return node.left_child.value


            elif header[i]==node.split_variable and your_data[i]=='0':

                if node.right_child.get_name() == 'Node':
                    return (evaluate_tree(header,your_data, node.right_child))
                elif node.right_child.get_name() == 'Leaf':

                    return node.right_child.value

        

    


nerr_train=0
for k in range(1,len(table)):

    classify=evaluate_tree(table[0], table[k], node1)
    if classify!=table[k][-1]:

    nerr_train=nerr_train+1

train_error=nerr_train/float(k)
print 'error(train):', train_error




nerr_test=0
for p in range(1,len(test_table)):

    classify=evaluate_tree(test_table[0], test_table[p], node1)
    if classify!=test_table[p][-1]:
    nerr_test=nerr_test+1

test_error=nerr_test/float(p)
print 'error(test):', test_error


f1.close()
f2.close()
