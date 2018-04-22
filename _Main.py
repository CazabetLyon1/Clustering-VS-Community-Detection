import ClusterLib

# --- Load Data
print('loading...')
attr1 = ClusterLib.loadData_Att('data/att/random.csv')
net = ClusterLib.loadData_Net('data/net/karate.gml')
print('net -> att')
attr = ClusterLib.Net2Att(net,ClusterLib.attMethods.transform.laplacianEigenmaps)
print(attr)

# --- Clusteringgit sta
print('Clustering...')
method = ClusterLib.attMethods.clustering.kMeans
cluster = ClusterLib.cluster_Att(attr,method,3)

print(cluster)
# --- Plotting
print('Plotting...')
import matplotlib.pyplot as plt
plt.ion()
colors = ['green','red','blue','magenta','yellow']
for i in range(len(cluster)):
	xData = attr[i][0]
	yData = attr[i][1]
	clusterId = cluster[i]
	col = colors[clusterId]
	plt.scatter(xData,yData,color=col)
plt.pause(100)
