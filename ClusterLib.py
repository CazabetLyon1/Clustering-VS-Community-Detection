from AttClustering import attMethods
from NetClustering import netMethods
import Metric

# -----------------------------------------------------------
# --------------------------------------------------- LOAD --
def loadData_Att(filename):
	return attMethods.loadData(filename)

def loadData_Net(filename):
	return netMethods.loadData(filename)

# -----------------------------------------------------------
# ---------------------------------------------- TRANSFORM --
def Att2Net(AttObj,method,**kwargs):
	return method(AttObj,**kwargs)

def Net2Att(NetObj,method,**kwargs):
	return method(NetObj)

# -----------------------------------------------------------
# --------------------------------------------- CLUSTERING --
def cluster_Att(attObject,method,clusterCount=None,**kwargs):
	return method(attObject,clusterCount,**kwargs)

def cluster_Net(netObject,method,clusterCount=None,**kwargs):
	return method(netObject,clusterCount,**kwargs)

# -----------------------------------------------------------
# --------------------------------------------- EVALUATION --
def evaluateClustering(trueClusters,predClusters,method,**kwargs):
	return method(trueClusters,predClusters,**kwargs)
