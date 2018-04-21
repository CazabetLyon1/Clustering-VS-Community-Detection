import ClusterLib

# --- Load Data
print('loading...')
attr = ClusterLib.loadData_Att('data.csv')

# --- Clustering
print('Clustering...')
method = ClusterLib.attMethods.clustering.birch
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
