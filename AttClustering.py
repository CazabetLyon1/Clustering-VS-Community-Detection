import numpy as np
from sklearn.cluster import KMeans,MeanShift,AgglomerativeClustering,AffinityPropagation,DBSCAN,Birch,estimate_bandwidth
from sklearn import mixture

class attMethods:
	# ------------------------ loading
	# -- Type de données:
	# --
	# -- [
	# -- ...
	# -- [attr1,attr2,attr3,attr4,...]
	# -- [attr1,attr2,attr3,attr4,...]
	# -- ...
	# -- ]
	# --
	# --------------------------------
	def loadData(filename):
		attr = []
		f = open(filename,'r')
		lines = f.readlines()
		for line in lines:
			elm = line.strip().split(',')
			elm = [float(e) for e in elm]
			attr.append(elm)
		return attr;

	# ------------------------ transfrom
	class transform:
		def naiveTransform(netData,**kwargs):

			# --- Comptage des sommets
			length = 0
			for link in netData:
				s1 = list(link)[0]
				s2 = list(link)[1]
				theoLength = max(s1,s2)+1
				if theoLength > length:
					length = theoLength

			# --- Creation de la matrice
			dic = {}
			for i in range(length):
				dic[i] = []
				for _ in range(length):
					dic[i].append(0)

			for link in netData:
				s1 = None
				s2 = None
				p = 1
				if len(link) == 2:
					s1, s2 = link
				else:
					s1, s2, p = link

				# --- mise a jour de la matrice
				dic[s1][s2] = p

			# --- Normalisation
			ret = []
			for sommet,liens in dic.items():
				ret.append(liens)

			return ret

		def learningTransform(netData,**kwargs):
			pass
	# ------------------------ clustering
	class clustering:
		# ---
		def kMeans(obj,clusterCount=None,**kwargs):
			labels = KMeans(n_clusters=clusterCount, random_state=170).fit_predict(obj)
			return attMethods.labelsToCluster(obj,labels,clusterCount)

		# ---
		def affinityPropagation(obj,clusterCount=None,**kwargs):
			af = AffinityPropagation(preference=-50).fit(obj)
			cluster_centers_indices = af.cluster_centers_indices_
			labels = af.labels_
			return attMethods.labelsToCluster(obj,labels,len(cluster_centers_indices))

		# ---
		def meanShift(obj,clusterCount=None,**kwargs):
			quantile = attMethods.getDefaultValue('quantile',0.2,**kwargs)
			bandwidth = estimate_bandwidth(obj, quantile=quantile, n_samples=int(len(obj)/20))
			ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
			ms.fit(obj)
			labels = ms.labels_
			cluster_centers = ms.cluster_centers_
			return attMethods.labelsToCluster(obj,labels,len(cluster_centers))

		# ---
		def agglomerative(obj,clusterCount=None,**kwargs):
			model = AgglomerativeClustering(n_clusters=clusterCount)
			model.fit(obj)
			labels = model.labels_
			return attMethods.labelsToCluster(obj,labels,clusterCount)

		# ---
		def DBSCAN(obj,clusterCount=None,**kwargs):
			eps = attMethods.getDefaultValue('eps',0.3,**kwargs)
			min_samples = attMethods.getDefaultValue('min_samples',0.3,**kwargs)
			db = DBSCAN(eps=eps, min_samples=min_samples).fit(obj)
			core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
			core_samples_mask[db.core_sample_indices_] = True
			labels = db.labels_
			n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
			return attMethods.labelsToCluster(obj,labels,n_clusters_)

		# ---
		def gaussianMixture(obj,clusterCount=None,**kwargs):
			gmm = mixture.GaussianMixture(n_components=clusterCount, covariance_type='full').fit(obj)
			labels = gmm.predict(obj)
			return attMethods.labelsToCluster(obj,labels,clusterCount)

		# ---
		def birch(obj,clusterCount=None,**kwargs):
			threshold = attMethods.getDefaultValue('threshold',0.5,**kwargs)
			mdl = Birch(threshold=threshold, n_clusters=clusterCount)
			mdl.fit(obj)
			labels = mdl.labels_
			return attMethods.labelsToCluster(obj,labels)
		
	# ------------------------ common methods
	# ---
	def getDefaultValue(name,default,**kwargs):
			if name in kwargs:
				return  kwargs[name]
			else:
				return default
	# ---
	def labelsToCluster(obj,labels,nbLabels=None):
		if nbLabels is None:
			nbLabels = np.unique(labels).size
		cluster = []
		for _ in range(nbLabels):
			cluster.append([])
		for i in range(len(labels)):
			label = labels[i]
			cluster[label].append(obj[i])
		return cluster

