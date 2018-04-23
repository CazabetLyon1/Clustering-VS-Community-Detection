from sklearn.metrics import f1_score, adjusted_mutual_info_score as AMI
from sklearn.preprocessing import MultiLabelBinarizer


def f1(trueClusters, predClusters, **kwargs) :
    avg = kwargs.get('average', None)   # accept this values : None, ‘binary’ (default), ‘micro’, ‘macro’, ‘samples’, ‘weighted’
    score = f1_score(trueClusters, predClusters, average=avg)
    return score


def ami(true, predict, **kwargs) :
    score = AMI(true, predict)
    return score
