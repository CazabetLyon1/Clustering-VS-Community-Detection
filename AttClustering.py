class attMethods:
	# ------------------------ loading
	# -- Type de données:
	# --
	# -- [
	# -- ...
	# -- (attr1,attr2,attr3,attr4,...)
	# -- (attr1,attr2,attr3,attr4,...)
	# -- ...
	# -- ]
	# --
	# --------------------------------
	def loadData(filename):
		pass

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
				ret.append(tuple(liens))

			return ret

		def learningTransform(netData,**kwargs):
			pass
		
	# ------------------------ clustering
	class clustering:
		def kMeans(clusterCount=None,**kwargs):
			pass

		def affinityPropagation(clusterCount=None,**kwargs):
			pass

		def meanShift(clusterCount=None,**kwargs):
			pass

		def spectralClustering(clusterCount=None,**kwargs):
			pass

		def WHC(clusterCount=None,**kwargs):
			pass

		def agglomerative(clusterCount=None,**kwargs):
			pass

		def DBSCAN(clusterCount=None,**kwargs):
			pass

		def gaussianMixture(clusterCount=None,**kwargs):
			pass

		def birch(clusterCount=None,**kwargs):
			pass