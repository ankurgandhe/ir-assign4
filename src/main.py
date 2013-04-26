from ReadData import * 
import scipy.sparse.linalg

if __name__ == '__main__':
    if len(sys.argv)<3:
        print >> sys.stderr, " usage : python main.py <TransitionMatrix-File> <alpha>"
        sys.exit(0)
    TMatrixFile = sys.argv[1]
    alpha = float(sys.argv[2])

    print >> sys.stderr, "Reading Transition Matrix file:", TMatrixFile
    TransitionMatrix,doclist = ReadTransitionMatrix(TMatrixFile)
    N_docs = int(TransitionMatrix.get_shape()[0])
    print >> sys.stderr,"Read ", N_docs," documents"

    print >> sys.stderr, "Creating Teleportation Matrix"
    TeleportationMatrix = GetTeleportationMatrix(N_docs,N_docs,N_docs,doclist,alpha)

    print >> sys.stderr, "Creating page rank vector"
    r = GetPageRank(TransitionMatrix,TeleportationMatrix,alpha,"iterate")
    
    r = r.todense()
    print >> sys.stderr, r.shape
    print >> sys.stderr, sum(r)
    
    
    #B = CreatePageRankMatrix(TransitionMatrix, TeleportationMatrix,alpha)
    #(lam,r) = scipy.sparse.linalg.eigs(B,k=1,which='LM')
    #rint lam
    #or i in range(len(r)):
    #	print r[i]
    #rint len(r),max(r)
    
