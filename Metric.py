from sklearn.metrics import f1_score, adjusted_mutual_info_score as AMI
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np


def f1(trueClusters, predClusters, **kwargs) :
    avg = kwargs.get('average', "macro")   # accept this values : None, ‘binary’ (default), ‘micro’, ‘macro’, ‘samples’, ‘weighted’
    nbrClusterPredicted = max(predClusters)
    maxScore = 0
    pred = np.array(predClusters)

    for i in range(0, (nbrClusterPredicted+1)) :  #f1_score() preserve the order of the cluster but it's not what we want here.
        cluster = pred
        cluster = cluster + i
        cluster = cluster % (nbrClusterPredicted+1)
        score = f1_score(trueClusters, cluster, average=avg)
        if score > maxScore :
            maxScore = score
    return maxScore


def ami(true, predict, **kwargs) :
    score = AMI(true, predict)
    return score
