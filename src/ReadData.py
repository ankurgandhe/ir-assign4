import sys 
import scipy
import scipy.sparse
import numpy 
import math 
# Read Transition matrix given in sparse format
def ReadTransitionMatrix(FileName):
    item=0
    i=[]
    n_i = {}
    j=[]
    data=[]
    try:
        for l in open(FileName):
            l=l.strip().split()
            doc_i = int(l[0])-1
            i.append(doc_i)
	    if doc_i not in n_i:
		n_i[doc_i] = 0
	    n_i[doc_i] = n_i[doc_i]+1
	
            j.append(int(l[1])-1)
            data.append(int(l[2]))

        maxN = max(max(i),max(j))+1
        print >> sys.stderr, "Number of Documents with out links:", len(n_i)
	for idx in range(len(i)):	
            if i[idx] not in n_i:
                print >> sys.stderr, i[idx],": 0"
                continue 
	    data[idx] = data[idx]/n_i[i[idx]]
	    #print >> sys.stderr, I[idx],":",n_i[I[idx]], 1./n_i[I[idx]]
        DocsAdded=0
        '''for doci in range(maxN):
            if doci not in n_i:
                for docj in range(maxN):
                    i.append(doci)
                    j.append(docj)
                    data.append(1./maxN)
                DocsAdded=DocsAdded+1
                print >> sys.stderr,"Added ",doci
        print >> sys.stderr, DocsAdded," docs added to T matrix with prob: ", 1./maxN'''
        I = numpy.asarray(i)
        J = numpy.asarray(j)
        maxN = max(max(I),max(J))+1
        Data = numpy.asarray(data)

        TransitionMatrix = scipy.sparse.coo_matrix((Data,(I,J)),shape = (maxN,maxN))
        return (TransitionMatrix,n_i)

    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        return 0


#Given nrows, ncolumns, generate Teleportaion matrix in sparse format 
def GetTeleportationMatrix(nrows, ncols, N,doclist,alpha):
    i=[]
    j=[]
    data=[]
    for idx in range(nrows):
        i.append(idx)
        j.append(0)
        if idx in doclist:
            data.append(1./N)
        else:
            data.append(1./(N))
    I = numpy.asarray(i)
    J = numpy.asarray(j)
    Data = numpy.asarray(data)
    print >> sys.stderr, "Creating sparse.. "
    TeleportationMatrix = scipy.sparse.coo_matrix((Data,(I,J)),shape=(nrows,1))
    
    return TeleportationMatrix
    
def CreatePageRankMatrix(M,p0,alpha):
    alpha = float(alpha)
    p1 = numpy.ones((1, M.get_shape()[0]))
    #p1 = scipy.sparse.coo_matrix(tmp)
    #print p0.get_shape() , p1.get_shape()
    E = p0.todense() * p1
    B  = (1. - alpha) * M.todense() + alpha * E #p0 * p1.transpose()
    return B.transpose()

def GetPageRank(TransitionMatrix,TeleportationMatrix,alpha,method):
    #Create page rank r , using give method :
    Mt = TransitionMatrix.transpose()
    p0 = TeleportationMatrix 
    epsilon = 0.000000001
    iter = 0
    n_docs = int(Mt.get_shape()[0])
    r = scipy.sparse.coo_matrix(([1],([0],[0])),shape=(n_docs,1))

    print >> sys.stderr, "initial vector is of shape: ", r.shape, "and sums to", r.sum()
    if method=="iterate":
        conv=False
        while not conv:
            rold = r
            r =  (1-alpha)*Mt* rold + alpha*p0
	    diff = numpy.sum(numpy.absolute((rold.todense() - r.todense())))
            if diff <=epsilon:
                conv=True
	    iter = iter+1
	    if iter%10==0:
		print >> sys.stderr,iter,"...",
    print >> sys.stderr, str(iter)+":",str(diff)
    return r 
                  
           
def CheckSparseMatrix(M):
    M = M.todense()
    for i in range(len(M)):
        print >> sys.stderr, sum(M[ii])
