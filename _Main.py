import ClusterLib

# --- Load Data
print('loading...')
attr = ClusterLib.loadData_Att('data.csv')

# --- Clustering
print('Clustering...')
method = ClusterLib.attMethods.clustering.birch
cluster = ClusterLib.cluster_Att(attr,method,3)

# --- Plotting
print('Plotting...')
import matplotlib.pyplot as plt
plt.ion()
colors = ['green','red','blue','magenta','yellow']
colId = 0
for sett in cluster:
	x = [elm[0] for elm in sett]
	y = [elm[1] for elm in sett]
	plt.scatter(x,y,color=colors[colId])
	colId += 1
plt.pause(100)
