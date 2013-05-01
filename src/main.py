from PageRank import * 
from RankDocuments import * 
import scipy.sparse.linalg
import os

def PrintRankList(PageRankVector,indri_dir):
    no_files=0
    for files in os.listdir(indri_dir):
        if files.endswith(".txt"):
            uid,qid,RankList = RankIndriFile(indri_dir+'/'+files,PageRankVector)
            PrintTrecFormat(uid,qid,RankList)
            no_files = no_files+1
    print >> sys.stderr, "Read",no_files,"files."
    
    
def PrintTrecFormat(uid,qid,RankList):
    rank=1
    for score,docid in RankList:
        print str(uid)+'-'+str(qid),'Q0',docid,rank,score,"pagerank"
        rank = rank+1
    return 1



if __name__ == '__main__':
    if len(sys.argv)<4:
        print >> sys.stderr, " usage : python main.py <TransitionMatrix-File> <damping-factor> <indri-files-dir>"
        sys.exit(0)
    TMatrixFile = sys.argv[1]
    alpha = 1 - float(sys.argv[2])
    indri_dir = sys.argv[3]

    print >> sys.stderr, "Reading Transition Matrix file:", TMatrixFile
    TransitionMatrix,doclist = ReadTransitionMatrix(TMatrixFile)
    N_docs = int(TransitionMatrix.get_shape()[0])
    print >> sys.stderr,"Read ", N_docs," documents"

    print >> sys.stderr, "Creating Teleportation Matrix"
    TeleportationMatrix = GetTeleportationMatrix(N_docs,N_docs,N_docs,doclist,alpha)

    print >> sys.stderr, "Creating page rank vector"
    r = GetPageRank(TransitionMatrix,TeleportationMatrix,alpha,"iterate")
    
    r = r.todense()
    
    print >> sys.stderr, "Size of PageRank Matrix:", r.shape
    print >> sys.stderr, "Sum of all elements of PageRank matrix:",sum(r)
    
    PrintRankList(r,indri_dir)
    
    #B = CreatePageRankMatrix(TransitionMatrix, TeleportationMatrix,alpha)
    #(lam,r) = scipy.sparse.linalg.eigs(B,k=1,which='LM')
    #rint lam
    #or i in range(len(r)):
    #	print r[i]
    #rint len(r),max(r)
    
