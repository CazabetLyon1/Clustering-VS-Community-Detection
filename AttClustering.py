import numpy as np
from sklearn.cluster import KMeans,MeanShift,AgglomerativeClustering,AffinityPropagation,DBSCAN,Birch,estimate_bandwidth
from sklearn import mixture
import networkx as nx
from gem.utils import graph_util

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
	def graphToDiGraph(net):
		di_graph = nx.DiGraph()
		di_graph.add_nodes_from(range(max([item for sublist in net for item in sublist])+1))
		for node in net:
			n1 = node[0]
			n2 = node[1]
			if len(node)==3:
				di_graph.add_edge(n1, n2, weight=node[2])
			else:
				di_graph.add_edge(n1, n2)
		return di_graph

	def GEMexport(netData,emb):
		G = attMethods.graphToDiGraph(netData)
		Y, t = emb.learn_embedding(graph=G, edge_f=None, is_weighted=True, no_python=True)
		return Y

	class transform:
		# ---
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

		# ---
		def graphFactorization(netData,**kwargs):
			d = kwargs.get('d',2)
			max_iter = kwargs.get('max_iter',100000)
			eta = kwargs.get('eta',1*10**-4)
			regu = kwargs.get('regu',1.0)
			from gem.embedding.gf import GraphFactorization
			emb = GraphFactorization(d=d, max_iter=max_iter, eta=eta, regu=regu)
			return attMethods.GEMexport(netData,emb)

		# ---
		def HOPE(netData,**kwargs):
			d = kwargs.get('d',4)
			beta = kwargs.get('beta',0.01)
			from gem.embedding.hope import HOPE
			emb = HOPE(d=d, beta=beta)
			return attMethods.GEMexport(netData,emb)

		# ---
		def laplacianEigenmaps(netData,**kwargs):
			d = kwargs.get('d',2)
			from gem.embedding.lap import LaplacianEigenmaps
			emb = LaplacianEigenmaps(d=d)
			return attMethods.GEMexport(netData,emb)

		# ---
		def locallyLinearEmbedding(netData,**kwargs):
			d = kwargs.get('d',2)
			from gem.embedding.lle import LocallyLinearEmbedding
			emb = LocallyLinearEmbedding(d=d)
			return attMethods.GEMexport(netData,emb)

		# ---
		def node2vec(netData,**kwargs):
			d = kwargs.get('d',2)
			max_iter = kwargs.get('max_iter',1)
			walk_len = kwargs.get('walk_len',80)
			num_walks = kwargs.get('num_walks',10)
			con_size = kwargs.get('con_size',10)
			ret_p = kwargs.get('ret_p',1)
			inout_p = kwargs.get('inout_p',1)
			from gem.embedding.node2vec import node2vec
			emb = node2vec(d=d, max_iter=max_iter, walk_len=walk_len,
				num_walks=num_walks, con_size=con_size, ret_p=ret_p, inout_p=1)
			return attMethods.GEMexport(netData,emb)

		# ---
		def SDNE(netData,**kwargs):
			d = kwargs.get('d',2)
			beta = kwargs.get('beta',5)
			alpha = kwargs.get('alpha',1e-5)
			nu1 = kwargs.get('nu1',1e-6)
			nu2 = kwargs.get('nu2',1e-6)
			K = kwargs.get('K',3)
			n_units = kwargs.get('n_units',[50, 15,])
			rho = kwargs.get('rho',0.3)
			n_iter = kwargs.get('n_iter',50)
			xeta = kwargs.get('xeta',0.01)
			n_batch = kwargs.get('n_batch',500)
			modelfile = kwargs.get('modelfile',['./intermediate/enc_model.json', './intermediate/dec_model.json'])
			weightfile = kwargs.get('weightfile',['./intermediate/enc_weights.hdf5', './intermediate/dec_weights.hdf5'])
			from gem.embedding.sdne import SDNE
			emb = SDNE(d=d, beta=beta, alpha=alpha, nu1=nu1, nu2=nu2,
				K=K,n_units=n_units, rho=rho, n_iter=n_iter, xeta=xeta,
				n_batch=n_batch,modelfile=modelfile,weightfile=weightfile)
			return attMethods.GEMexport(netData,emb)

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
		'''
		if nbLabels is None:
			nbLabels = np.unique(labels).size
		cluster = []
		for _ in range(nbLabels):
			cluster.append([])
		for i in range(len(labels)):
			label = labels[i]
			cluster[label].append(i)
		'''
		return labels
