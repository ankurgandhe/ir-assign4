import sys
import math

def RankIndriFile(FileName,PageRank,UserQueryTopicProb,method):

    try:
        Name=FileName.strip().split('/')[-1]
        uid=int(Name.split('-')[0])
        qid = int(Name.split('-')[1].split('.')[0])
        RankList = []
        for l in open(FileName):
            l=l.strip().split()
            docid = int(l[2])
            score = float(l[4])
            
            if method=="gpr":
                PageRankScore = PageRank[docid-1]
                print >> sys.stderr, "PageRank for ",uid,qid,docid,":",PageRankScore
                NewScore = ScorePageRank(uid,docid,score,PageRankScore,1)
            elif method=="qtspr":
                PageRankScore = 0.0
                for t in range(len(PageRank)):
                    PageRankScore = PageRankScore + UserQueryTopicProb[(uid,qid)][t]*PageRank[t][docid-1]
                print >> sys.stderr, "PageRank for ",uid,qid,docid,":",PageRankScore
                NewScore = ScorePageRank(uid,docid,score,PageRankScore,1)
            RankList.append((NewScore,docid))
        
        return (uid,qid,sorted(RankList,reverse=True))
            
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)

def ScorePageRank(uid,docid,qscore,PageRankScore,algo):
    FinalScore =0
    if algo==1:
        lambda1=0.2
        prscore = float(math.log10(PageRankScore))
        FinalScore = (1-lambda1)*qscore + lambda1*prscore 
    
    return FinalScore
    
