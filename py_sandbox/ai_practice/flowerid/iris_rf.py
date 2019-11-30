'''
datecreated: 191123
objective: use random forest classifier to ID flowers in iris dataset based on 4
    parameters. for more information see iris_nn.py.

NOTES:
* there's a lot of non-matrix operations to do, so will need to break things
    down in pieces
* seems like some use ordered dicts to generate random forests
* realized that binary data is a subset of discrete data, and discrete is a
    subset of continuous data, and have unified mask function

General Steps:
1. create simple, small binary dataset (e.g. heart disease from src)
2. create data boostrappig function / bagging function
3. create gini impurity calculator (generalized both for leaves and nodes)
4. create continuous data node?
4. generate a randomized decision tree?
5. generate random forest?
6. evaluate on a random forest?


Current Goals
STAT | DESCRIPTION
--------------------------------------------------
done | be able to get gini / entropy score for a given set of data / parameter
done | create node for binary data
done | create node for continuous data
done | create node for discrete data?
done | unify masking function for binary, discrete, and continuous data
done | create a single decision node
done | automatically determine best node to add (function)
done | get rid of condition argument, not needed
done | single-node decision tree, capable of train and eval
done | make custom counting function, based on number of classes given
done | create decision node with children
done | make tree node with all functions:
done | tree=DecisionTree(dict_format,nclasses)
done | tree.train(data) # take output from training one node, give it to children, etc
done | tree.query(idat) # if result is integer, go to node. if list, give result
???? | create a single node decision tree automatically
???? | create a random forest
???? | bootstrap a dataset
???? | ??
???? | ??

want to create a tree based on an format, such as:
treedef=dict()
treedef[0]=[[props],[children]] # root node
treedef[1]=[[props],[children]]


for partitioning help, want a function that:
    0. given a dataset in matrix form
    1. looks at each parameter
    2. determines if binary, discrete, or continuous
    3. check entropy across all parameters / thresholds
    4. print results (or return best option)



'''

selfdat=[ # taken from DataScienceFromScratch, p221
#Lv La Tw Ph dw
[2, 0, 0, 0, 0], # parameters: level / language / tweets / has phd / did well
[2, 0, 0, 1, 0], # 0/1/2 = junior / mid / senior
[1, 1, 0, 0, 1], # 0/1/2 = java / python / r
[0, 1, 0, 0, 1], # 0/1 = False / True
[0, 2, 1, 0, 1],
[0, 2, 1, 1, 0],
[1, 2, 1, 1, 1],
[2, 1, 0, 0, 0],
[2, 2, 1, 0, 1],
[0, 1, 1, 0, 1],
[2, 1, 1, 1, 1],
[1, 1, 0, 1, 1],
[1, 0, 1, 0, 1],
[0, 1, 0, 1, 0]
]

# first, work on getting a decision tree to work (with a single node)
import numpy as np
from klib import data as da
from klib import listContents as lc
dat=np.array(selfdat,dtype=object) # using this type keeps ints as ints
# will now modify data to match how iris dataset is loaded, to see if the decision tree behaves properly

def convertToDS(data):
    ''' take an input array with ians at final column and convert to local convention '''
    ds = []
    for irow in data:
        idat=irow[:=1]
        ians=np.zeros(2)+0.01
        ians[irow[-1]]=0.99
        ds.append([idat,ians])
    return ds
ds = convertToDS(dat)

def findthresholds(data):
    ''' find thresholds, and assume that data is a vector '''
    temp=data[np.argsort(data)]
    inds=np.where(temp[1:]-temp[:-1])[0]
    threshs=[temp[i:i+2].mean() for i in inds]
    return threshs
def findsplit(data):
    ''' Given an input array (assume last parameter is ground truth), determine
        type of parameter, check entropy for each combination, and return
        results.
    '''
    assert data.dtype =='O',"Dataset not loaded as dtype=object, param types might be ambiguous"
    nparams = len(data[0])-1
    # determine nature of each parameter
    ptype=[] # 0=binary,1=discrete,2=continuous
    for i in range(nparams):
        if(type(data[:,i].max())==float):
            # non-integer: continuous data
            ptype.append(2)
        elif(data[:,i].max()>1):
            # int, larger than 1: discrete
            ptype.append(1)
        else:
            ptype.append(0)

    # check each parameter's thresholds and report all combos
    arr=[]
    desmetric=1 # 0=gini, 1 = entropy
    for iparam in range(nparams):
        # for now, will not worry about continuous data and massive number of splits there can be...
        threshs=findthresholds(data[:,iparam])
        for ithresh in threshs:
            inode = Node(iparam,thresh=ithresh,met=desmetric)
            score=round(inode.check(data)[2][0],3)
            arr.append([iparam,ithresh,score])
    return np.array(arr)

def countClasses(data,nclasses):
    ''' given some data and set of classes, count each class out
    ASSUMPTIONS:
        * classes range from 0 to n
        * data is a 1-D array of integers
    '''
    s=np.zeros(nclasses)
    for i in data:
        s[i]+=1
    return s

class Node:
    '''
    INITIALIZATION INPUTS:
    * param: parameter index (0,1,2,...). default=0
    * thresh: threshold to test condition default=0
    * metric: metric to identify best separation of values. 0=gini, 1=entropy.
        default=0
    '''
    _METRICS=[0,1] # gini, entropy
    def __init__(self,param=0,thresh=0.5,nclasses=2,met=0):
        assert met in self._METRICS,"invalid metric specified: "+met
        self.param=param # index, 0...n
        self._thresh = thresh # req if cond=thresh
        self._metric = met
        self.parent=None
        self.ncls = nclasses # will simply receive number of classes (such as from Tree object)
        self.yes_kid=None # index of child branch for "yes" (True) answer
        self.no_kid=None
        self.yes_ans=None # index of child branch for "no" (False) answer
        self.no_ans=None
        if(self._metric==self._METRICS[1]):
            self.metric=self.entropy
        else:
            self.metric=self.gini

    @property
    def children(self):
        return self.yes_kid,self.no_kid

    def _addchildren(self,children):
        ''' Give a 2-item list of either None or some index value for another
            node. only intended to be used by DecisionTree class '''
        self.yes_kid=children[0]
        self.no_kid = children[1]

    def check(self,input):
        ''' get mask and obtain separated result arrays and metrices (3-values) '''
        mask=input[:,self.param]>self._thresh # bin/disc/cont all calculate mask same way
        res0=input[mask] # first check yes, then no...
        res1=input[np.logical_not(mask)]
        resMetric=self.metric(res0,res1)
        # get gini score
        return res0,res1,resMetric

    def train(self,data,_nodes=None):
        ''' given a set of input data, decide what the outcome of a node would be
        variable _nodes only intended for use by DecisionTree class

        first, transform data from local convention to more usual array
        local convention: ds_train[0] = [input_array_normalized,ans_array]
            input_array = [0.01,0.43,0.99,...]
            ans_array   = [0.01,0.01,0.99] # 3-class example
        usual array:
            ds_train[0] = [*input_array,2]
        '''
        res0,res1=self.check(data)[:2]
        count0=countClasses(res0[:,-1],self.ncls)
        count1=countClasses(res1[:,-1],self.ncls)

        self.yes_ans=count0/count0.sum()
        self.no_ans =count1/count1.sum()

        if(type(_nodes)==type(None)):
            # no need to recursively train
            return res0,res1
        # otherwise, will then tell children to train as well
        if(self.yes_kid != None):
            _nodes[self.yes_kid].train(res0,_nodes)
        if(self.no_kid != None):
            _nodes[self.no_kid].train(res1,_nodes)

    def query(self,idat):
        ''' given a single sample, return what node thinks classification would be '''
        if(idat[self.param]>self._thresh):
            if(self.yes_kid==None):
                return self.yes_ans
            else:
                return self.yes_kid # should be an integer
        else:
            if(self.no_kid==None):
                return self.no_ans
            else:
                return self.no_kid # should be an integer

    def gini(self,res0,res1=None):
        ''' Get the gini impurity based on the output of an entire node (both
            binary results). can have any number of classes, which are
            determined when running. If only one result is given, then gini
            score of just that result is given (leaf?)
        '''
        count0=countClasses(res0[:,-1],self.ncls)
        gini0=1-sum( (count0/count0.sum())**2 )
        if(type(res1)==type(None)):
            return gini0
        # otherwise, continue and return complete gini score
        count1=countClasses(res1[:,-1],self.ncls)
        gini1=1-sum( (count1/count1.sum())**2 )
        sum01=len(res0)+len(res1)
        giniN = (len(res0)/sum01)*gini0+(len(res1)/sum01)*gini1
        return giniN,gini0,gini1

    def entropy(self,res0,res1=None):
        ''' Another way to find how "pure" a list of classes are. based on
            example from Data Science from Scratch
        '''
        s0=countClasses(res0[:,-1],self.ncls)
        pcls0=s0/s0.sum()
        ent0=sum([-ip*np.log(ip) for ip in pcls0 if(ip>0)]) # per book, ignore '0'
        if(type(res1)==type(None)):
            return ent0
        # otherwise get weighted sum of combined entropy if have both results
        s1=countClasses(res1[:,-1],self.ncls)
        pcls1=s1/s1.sum()
        ent1=sum([-ip*np.log(ip) for ip in pcls1 if(ip>0)]) # per book, ignore '0'
        entN = ( ent0*len(res0) + ent1*len(res1) )/( len(res0) + len(res1) )
        return entN, ent0, ent1

class DecisionTree:
    ''' a decision tree will hold the structure of each node (parents /
        children each has) and will contain all the nodes themselves as well.
        this object also traverses the "tree" to each final classification
    NOTE:
    * should have train function (take in data and save final scores at each leaf)
    * should have eval function (traverse tree)
    Typical Usage:
    tree = DecisionTree(struct,2) # struct=(premade dict of nodes)
    tree.train(ds) # "train" on a dataset
    tree.query(ds[0][0]) # test on sample data
    '''
    def __init__(self,structure,numclasses,metric=0):
        self.node=dict()
        self.ncls = numclasses
        self._origStruct=structure
        self.metric=metric # 0=gini, 1 = entropy
        # will create structure of tree based on given structure (dict)
        for ind in structure.keys():
            p,t,kids=structure[ind]
            self.node[ind] = Node(p,t,self.ncls,met=metric)
            # here, need to create connection to children
            self.node[ind]._addchildren(kids)
        # import ipdb; ipdb.set_trace()
    def train(self,data):
        ''' will train recursively (depth first) by having any node that
        has children to tell its children to train on that data as well. this is
        done by the root node access to both the data as well as the dict of
        nodes, which all nodes will use as a guide during training. '''
        # need to change data back to slightly more typical array
        inp = []
        for idat in data:
            inp.append( np.append( idat[0],np.argmax(idat[1]) ) )
        inp=np.array(inp)
        import ipdb; ipdb.set_trace()

        self.node[0].train(inp,self.node)
        # import ipdb; ipdb.set_trace()

    def query(self,idat):
        ''' traverse branches of tree based on given input data '''
        res=tree.node[0].query(idat)
        # if a list, then has returned answer. if an integer, then has returned index to a child
        while(type(res)==int):
            res = tree.node[res].query(idat)
        return res


# will instead create trees based on what children they have, not which parents
# struct[index] = [param,thresh,[yes_child,no_child]]
struct = dict()
struct[0]=[0,1.5,[1,2]] # root node usually has children
struct[1]=[2,0.5,[None,None]] # node either has 0, 1, or 2 children
struct[2]=[0,0.5,[None,3]] #
struct[3]=[3,0.5,[None,None]] # for now, will use double none to denote no children
# assumption: if child is None, then use metric to determine solution
tree = DecisionTree(struct,2)
tree.train(ds)
tree.query(ds[0][0])

'''
KJG191130: at this point, have very good control over a single decision tree and
    manually generating one. now will work on bootstrapping and randomly
    generating a tree, which can then lead to making a forest
'''






# eof
