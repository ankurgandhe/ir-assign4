from PageRank import * 
from RankDocuments import * 
import scipy.sparse.linalg
import os

def PrintRankList(PageRankVector,indri_dir,distribution_file,method):
    no_files=0
    if method=="gpr":
        for files in os.listdir(indri_dir):
            if files.endswith(".txt"):
                uid,qid,RankList = RankIndriFile(indri_dir+'/'+files,PageRankVector,[],method)
                PrintTrecFormat(uid,qid,RankList)
                no_files = no_files+1
        print >> sys.stderr, "Read",no_files,"files."
    elif method=="qtspr":
        UserQueryTopic = GetUserQueryTopicDistribution(distribution_file)
        for files in os.listdir(indri_dir):
            if files.endswith(".txt"):
                uid,qid,RankList = RankIndriFile(indri_dir+'/'+files,PageRankVector,UserQueryTopic,method)
                PrintTrecFormat(uid,qid,RankList)
                no_files = no_files+1
        print >> sys.stderr, "Read",no_files,"files."

def GetUserQueryTopicDistribution(distribution_file):
    UserQueryTopic = {}
    no_queries = 0
    for l in open(distribution_file):
        l=l.strip().split()
        uid = int(l[0])
        qid = int(l[1])
        UserQueryTopic[(uid,qid)] = {}
        for w in l[2:]:
            w = w.split(':')
            t=int(w[0])-1
            prob = float(w[1])
            UserQueryTopic[(uid,qid)][t]=prob
        no_queries = no_queries + 1
    print >> sys.stderr, "Read ", no_queries, " topics distributions "
    return UserQueryTopic

def PrintTrecFormat(uid,qid,RankList):
    rank=1
    for score,docid in RankList:
        print str(uid)+'-'+str(qid),'Q0',docid,rank,score,"pagerank"
        rank = rank+1
    return 1



def DoRetrieval_GPR(method,TMatrixFile,alpha,indri_dir):
    print >> sys.stderr, "Reading Transition Matrix file:", TMatrixFile
    TransitionMatrix,doclist = ReadTransitionMatrix(TMatrixFile)
    N_docs = int(TransitionMatrix.get_shape()[0])
    print >> sys.stderr,"Read ", N_docs," documents"

    print >> sys.stderr, "Creating Global Teleportation Matrix"
    #doclist = dict(range(1,N_docs+1))
    TeleportationVector = GetTeleportationVector(N_docs,N_docs,N_docs,doclist,alpha)
    
    print >> sys.stderr, "Creating page rank vector"
    r = GetPageRankVector(TransitionMatrix,TeleportationVector,alpha,"iterate")
    
    #r = r/float(sum(r))
    
    PrintRankList(r,indri_dir,"","gpr")
    
def DoRetrieval_QTSPR(method,TMatrixFile,alpha,indri_dir,doc_topic_file,query_topic_file):
    print >> sys.stderr, "Reading Transition Matrix file:", TMatrixFile
    TransitionMatrix,doclist = ReadTransitionMatrix(TMatrixFile)
    N_docs = int(TransitionMatrix.get_shape()[0])
    print >> sys.stderr,"Read ", N_docs," documents"

    print >> sys.stderr, "Create Topic-wise Teleportation matrix"
    TopicTeleportationList = GetTopicTeleportationList(doc_topic_file, N_docs,N_docs,N_docs,alpha)

    print >> sys.stderr, "Creating page rank vector"
    rList = GetPageRankList(TransitionMatrix,TopicTeleportationList,alpha,"iterate","query")
    
    #r = r/float(sum(r))

    PrintRankList(rList,indri_dir,query_topic_file,"qtspr")
    


if __name__ == '__main__':
    if len(sys.argv)<6:
        print >> sys.stderr, " usage : python main.py <method> <TransitionMatrix-File> <damping-factor> <indri-files-dir> <doc-topic-distribution> <query-topic-dist>"
        print >> sys.stderr, "<method> : gpr, qtspr, ptspr "
        sys.exit(0)
    method = sys.argv[1]
    TMatrixFile = sys.argv[2]
    alpha = 1 - float(sys.argv[3])
    indri_dir = sys.argv[4]
    doc_topic_file = sys.argv[5]
    query_topic_file = sys.argv[6]

    if method=="gpr":
        DoRetrieval_GPR(method,TMatrixFile,alpha,indri_dir)
    elif method=="qtspr":
        DoRetrieval_QTSPR(method,TMatrixFile,alpha,indri_dir,doc_topic_file,query_topic_file)
