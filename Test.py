import ClusterLib


#--------------- test of the dataloading funtions :
def testLoadingAtt(file, nbrPointsExpected, nbrDimensionExpected) :
    attr = ClusterLib.loadData_Att(file)
    nbrPoints = len(attr)
    nbrDim = len(attr[0])
    if(nbrPoints != nbrPointsExpected) :
        print("erreur dans la fonction de chargement attr: le nombre de points ne corresponds pas à ce qui est attendue dans la méthode avec le fichier "+file+"."+str(nbrPoints)+" au lieu de "+str(nbrPointsExpected))
    if (nbrDim != nbrDimensionExpected) :
        print("erreur dans la fonction de chargement attr: la taille des vecteurs ne corresponds pas à ce qui est attendue dans la méthode avec le fichier "+file+"."+str(nbrDim)+" au lieu de "+str(nbrDimensionExpected))


def testLoadingNet(file, nbrNodeExpected, nbrEdgeExpected) :
    net = ClusterLib.loadData_Net(file)
    nbrEdge = len(net)
    nbrNode = max([item for sublist in net for item in sublist])+1
    if(nbrNode != nbrNodeExpected) :
        print("erreur dans la fonction de chargement net: le nombre de noeuds ne corresponds pas à ce qui est attendue dans la méthode avec le fichier "+file+"."+str(nbrNode)+" au lieu de "+str(nbrNodeExpected))
    if (nbrEdge != nbrEdgeExpected) :
        print("erreur dans la fonction de chargement net: le nombre d'arc ne corresponds pas à ce qui est attendue dans la méthode avec le fichier " + file+"."+str(nbrEdge)+" au lieu de "+str(nbrEdgeExpected))


#--------------- test transformations :
def testAttToNet(attr, k, netExpected) :
    net = ClusterLib.Att2Net(attr,ClusterLib.netMethods.transform.naiveTransform,k=k)
    if(net != netExpected) :
        print("erreur, la transformation attToNet à un probléme. graphe obtenue :\n" + str(net) + "\n graphe attendue :\n" + str(netExpected))


def testNetToAtt(method, net, nbrPointsExpected, nbrDimensionExpected) :
    attr = ClusterLib.Net2Att(net, getattr(ClusterLib.attMethods.transform, method))
    nbrPoints = len(attr)   #nbr de vecteurs.
    nbrDim = len(attr[0])   #taille des vecteurs.
    if(nbrPoints != nbrPointsExpected) :
        print("erreur, le nombre de points ne corresponds pas à ce qui est attendue dans la méthode " + method + "." + str(nbrPoints) + " au lieu de " + str(nbrPointsExpected))
    if (nbrDim != nbrDimensionExpected) :
        print("erreur, la tailles des vecteurs ne corresponds pas à ce qui est attendue dans la méthode " + method + "." + str(nbrDim) + " au lieu de " + str(nbrDimensionExpected))



#--------------- test metrics :

def testAmi(list1, list2, resAttendue) :
    resObtained = ClusterLib.Metric.ami(list1,list2)
    if(resObtained != resAttendue) :
        print("error with ami. le résultat obtenue est " + str(resObtained) + " au lieu de " + str(resAttendue))


def testF1(list1, list2, resAttendue) :
    resObtained = ClusterLib.Metric.f1(list1,list2)
    if(resObtained != resAttendue) :
        print("error with ami. le résultat obtenue est " + str(resObtained) + " au lieu de " + str(resAttendue))








#data :
attr_file = ["data/att/birch1", "data/att/birch2", "data/att/dim032", "data/att/dim064", "data/att/dim128", "data/att/dim256", "data/att/s1", "data/att/s2", "data/att/s3" ,"data/att/s4"]
attr_nbr_points = [100000, 100000, 1024, 1024, 1024, 1024, 5000, 5000, 5000, 5000]
attr_nbr_dim = [2, 2, 32, 64, 128, 256, 2, 2, 2, 2]

netw_file = ["data/net/chaine", "data/net/dolphins", "data/net/football", "data/net/interconnexion_totale", "data/net/karate", "data/net/clique"]#, "data/net/amazon"]
netw_nbr_noeuds = [120, 62, 115, 120, 34, 64, 120, 0]
netw_nbr_edge = [119, 159, 613, 7140, 78, 208, 114, 0]


#testLoadingAtt :
for i in range(len(attr_file)) :
    testLoadingAtt(attr_file[i]+".csv", attr_nbr_points[i], attr_nbr_dim[i])


#testLoadingNet :
for i in range(len(netw_file)) : #on ne teste pas amazon pour le moment.
    testLoadingNet(netw_file[i]+".gml", netw_nbr_noeuds[i], netw_nbr_edge[i])


#test transformation netToAtt :
#methodes = ["naiveTransform", "graphFactorization", "HOPE", "laplacianEigenmaps", "locallyLinearEmbedding", "node2vec", "SDNE"]
for i in range(len(netw_file)) :
    net = ClusterLib.loadData_Net(netw_file[i] + ".gml")
#    for methode in methodes :
#        testNetToAtt(methode, net, netw_nbr_noeuds[i], netw_nbr_noeuds[i])
    testNetToAtt("naiveTransform", net, netw_nbr_noeuds[i], netw_nbr_noeuds[i])


#test transformation attToNet :
att = [[0,1,0], [0,0,0], [0,7,9], [9,1,1], [8,8,8], [0,0,1]]
res_k1 = [[0,1],[1,0],[2,4],[3,0],[4,2],[5,1]]
res_k2 = [[0,1],[0,5],[1,0],[1,5],[2,4],[2,5],[3,0],[3,5],[4,2],[4,3],[5,1],[5,0]]
res_k3 = [[0,1],[0,5],[0,3],[1,0],[1,5],[1,3],[2,4],[2,5],[2,0],[3,0],[3,5],[3,1],[4,2],[4,3],[4,0],[5,1],[5,0],[5,3]]
testAttToNet(att, 1, res_k1)
testAttToNet(att, 2, res_k2)
testAttToNet(att, 3, res_k3)

att = [[0,0],[0,0],[1,1],[1,1],[9,9]]
res_k1 = [[0,1],[1,0],[2,3],[3,2],[4,2]]
res_k2 = [[0, 1], [0, 2], [1, 0], [1, 3], [2, 3], [2, 0], [3, 2], [3, 1], [4, 2], [4, 3]]
res_k3 = [[0, 1], [0, 2],[0,3], [1, 0],[1,2], [1, 3], [2, 3], [2, 0],[2,1], [3, 2],[3,0], [3, 1], [4, 2], [4, 3], [4,0]]
testAttToNet(att, 1, res_k1)
testAttToNet(att, 2, res_k2)
testAttToNet(att, 3, res_k3)

attr = ClusterLib.loadData_Att(attr_file[3] + ".csv")
net1 = ClusterLib.Att2Net(attr,ClusterLib.netMethods.transform.naiveTransform,k=1)
net2 = ClusterLib.Att2Net(attr,ClusterLib.netMethods.transform.naiveTransform,k=2)
net3 = ClusterLib.Att2Net(attr,ClusterLib.netMethods.transform.naiveTransform,k=3)
net4 = ClusterLib.Att2Net(attr,ClusterLib.netMethods.transform.naiveTransform,k=4)
net5 = ClusterLib.Att2Net(attr,ClusterLib.netMethods.transform.naiveTransform,k=5)
net6 = ClusterLib.Att2Net(attr,ClusterLib.netMethods.transform.naiveTransform,k=6)

if(len(net1) != 1024) :
    print("le nombre d'arrete ne correspond pas à ce qui est attendue(6144). obetnue " + str(len(net1)))
if(1023 != max([item for sublist in net1 for item in sublist])) :
    print("le nombre de noeuds ne correspond pas à ce qui est attendue.")

if(len(net2) != 2048) :
    print("le nombre d'arrete ne correspond pas à ce qui est attendue(6144). obetnue " + str(len(net2)))
if(1023 != max([item for sublist in net1 for item in sublist])) :
    print("le nombre de noeuds ne correspond pas à ce qui est attendue.")

if(len(net3) != 3072) :
    print("le nombre d'arrete ne correspond pas à ce qui est attendue(6144). obetnue " + str(len(net3)))
if(1023 != max([item for sublist in net1 for item in sublist])) :
    print("le nombre de noeuds ne correspond pas à ce qui est attendue.")

if(len(net4) != 4096) :
    print("le nombre d'arrete ne correspond pas à ce qui est attendue(6144). obetnue " + str(len(net4)))
if(1023 != max([item for sublist in net1 for item in sublist])) :
    print("le nombre de noeuds ne correspond pas à ce qui est attendue.")

if(len(net5) != 5120) :
    print("le nombre d'arrete ne correspond pas à ce qui est attendue(6144). obetnue " + str(len(net5)))
if(1023 != max([item for sublist in net1 for item in sublist])) :
    print("le nombre de noeuds ne correspond pas à ce qui est attendue.")

if(len(net6) != 6144) :
    print("le nombre d'arrete ne correspond pas à ce qui est attendue(6144). obetnue " + str(len(net6)))
if(1023 != max([item for sublist in net1 for item in sublist])) :
    print("le nombre de noeuds ne correspond pas à ce qui est attendue.")
