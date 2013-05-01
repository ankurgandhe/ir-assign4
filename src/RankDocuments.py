import sys
import math

def RankIndriFile(FileName,PageRank):
    #print >> sys.stderr, "Reading file:",FileName
    try:
        Name=FileName.strip().split('/')[-1]
        uid=int(Name.split('-')[0])
        qid = int(Name.split('-')[1].split('.')[0])
        RankList = []
        for l in open(FileName):
            l=l.strip().split()
            docid = int(l[2])
            score = float(l[4])
            NewScore = ScorePageRank(uid,docid,score,PageRank,1)
            RankList.append((NewScore,docid))
        
        return (uid,qid,sorted(RankList,reverse=True))
            
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)

def ScorePageRank(uid,docid,qscore,PageRank,algo):
    FinalScore =0
    if algo==1:
        lambda1=0.2
        prscore = PageRank[docid-1]#math.log10(PageRank[docid-1])
        FinalScore = (1-lambda1)*qscore + lambda1*prscore 
    return FinalScore
    
