import math
from igraph import Graph as ig
from graph_tool.all import minimize_nested_blockmodel_dl, Graph as gt


# ------------------------ distance
def euclidianDistance(coordinate1, coordinate2):
	# each coordinate should be of the same dimension
	if(len(coordinate1) != len(coordinate2)):
		raise ValueError('error : the coordinate of the two points should be of the same dimension')

	sumOfSquare = 0
	for i,j in zip(coordinate1,coordinate2):
		sumOfSquare = sumOfSquare + ((abs(i) - abs(j)) ** 2)

	distance = math.sqrt(sumOfSquare)
	return distance


#transform the partition to correspond to the format of the librairy
def transformPartition(clusters) :
	nbrElement = 0
	for i in range(0,len(clusters)) :
		nbrElement = nbrElement + len(clusters[i])

	partition = [-1]*nbrElement
	for i in range(0,len(clusters)) :			#gave for each vertex the number of the community which it belong to.
		for j in range(0,len(clusters[i])) :
			partition[clusters[i][j]] = i

	return partition



class netMethods:
	# ------------------------ loading
	# -- Type de données:
	# --
	# -- sommets demarre a 0
	# --
	# -- [
	# -- ...
	# -- (sommet1, sommet2[, poid])
	# -- (sommet2, sommet7[, poid])
	# -- ...
	# -- ]
	# --
	# --------------------------------
	def loadData(filename):
		graph = ig.Read_GML(filename)
		return graph.get_edgelist()


	# ------------------------ transfrom
	class transform:

		#k nearest neightboors
		def naiveTransform(netData,**kwargs):
			k = kwargs.get('k', None)	# valeur par défault à definir, None ne peut pas permettre de construire un graphe
			nbrPoint = len(netData)
			distance = [dict() for x in range(nbrPoint)]	#create one dictionary for each point.
			graph = []

			#calcul of all the distance
			for i, vector in enumerate(netData) :
				j = i + 1
				while j < nbrPoint :#if j < i the entry is already in the dictionnary so it's useless to calculate it again.
					distance[i][j] = euclidianDistance(netData[i], netData[j])
					distance[j][i] = distance[i][j]
					j += 1

				#construction of the graph.
				j = 0
				while j < k :
					nearest = min(distance[i], key=distance[i].get)
					del distance[i][nearest]
					if([nearest, i] not in graph) :	#as the graph is non-oriented we don't want to add 2 time the same edge.
						graph.append([i, nearest])
					j += 1

			return graph



	# ------------------------ clustering
	class clustering:
		def infomap(netObject, clusterCount=None,**kwargs):
			graph = ig(0, netObject)
			partition = graph.community_infomap()
			print(partition)
			return transformPartition(partition)


		def louvain(netObject, clusterCount=None,**kwargs):
			graph = ig(0, netObject)
			partition = graph.community_multilevel()
			return transformPartition(partition)


		def labelPropagation(netObject, clusterCount=None,**kwargs):
			graph = ig(0, netObject)
			partition = graph.community_label_propagation()
			return transformPartition(partition)


		def nestedBlockmodel(netObject, clusterCount=None,**kwargs):
			g = gt()
			g.set_directed(False)
			for i in range(len(netObject)) :	#create the vertexself.#incorect, len(netobject) est le nombre de lien pas de sommet !!!!
				g.add_vertex()
			g.add_edge_list(netObject)		#create the edges.
			print(len(netObject))

			block = minimize_nested_blockmodel_dl(g)
			nbrBlocks = block.levels[0].get_B()
			block = block.levels[0].get_blocks()
			partition = [[] for x in range(nbrBlocks)]	#one list for each community.

			for i in range (0, len(netObject)-1) :
				partition[block[i]].append(i)

			return transformPartition(partition)
