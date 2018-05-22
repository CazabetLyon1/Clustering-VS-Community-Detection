import ClusterLib
import csv



#----------------------- exemple from data to graph : ---------------------------------------------

#load the data :
attr = ClusterLib.loadData_Att("data/att/dim128.csv")

#load the ground truth :
temp = csv.reader(open("data/att/dim128.csv","r"))
groundTruth = []
for row in temp: groundTruth.append(int(row[0]))

#transform the data into graph with a link to the 3-nearest neightboors and using 6 core of the CPU :
net = ClusterLib.Att2Net(attr, ClusterLib.netMethods.transform.naiveTransform,k=3, Core=6)

#get the cluster of the graph using infomap :
cluster = ClusterLib.cluster_Net(net, ClusterLib.netMethods.clustering.louvain)

#get the f1 score of the clustering :
f1 = ClusterLib.Metric.f1(groundTruth,cluster)
print(f1)

#get the AMI score of the clustering :
ami = ClusterLib.Metric.ami(groundTruth,cluster)
print(ami)




#----------------------- exemple from graph to data : ---------------------------------------------

#load the graph :
net = ClusterLib.loadData_Net("data/net/karate.gml")

#load the ground truth :
labels = open("data/net/karate_labels", "r")
groundTruth = []
for val in labels.read().split():
    groundTruth.append(int(val))
labels.close()

#transform the graph into data using laplacianEigenmaps method :
attr = ClusterLib.Net2Att(net, ClusterLib.attMethods.transform.laplacianEigenmaps)

#get the cluster of the graph using kMeans with 3 cluster :
cluster = ClusterLib.cluster_Att(attr, ClusterLib.attMethods.clustering.kMeans, 3)

#get the f1 score of the clustering :
f1 = ClusterLib.Metric.f1(groundTruth,cluster)
print(f1)

#get the AMI score of the clustering :
ami = ClusterLib.Metric.ami(groundTruth,cluster)
print(ami)
