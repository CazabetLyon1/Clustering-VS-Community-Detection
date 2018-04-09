import ClusterLib

# --- Creation d'un Net object
netObj = []
netObj.append((1,2))
netObj.append((1,3,2))
netObj.append((1,4))
netObj.append((2,4,7))
netObj.append((3,5))

test_att = []
#test_att.append((1,2,3,4,5,6,7,8,9))
#test_att.append((1,1,1,1,1,1,1,1,5))
#test_att.append((1,1,1,1,4,4,8,5,5))
#test_att.append((1,7,7,8,4,1,2,3,5))
#test_att.append((1,1,7,1,3,2,0,8,6))
test_att.append((1,5))
test_att.append((1,4))
test_att.append((1,3))
test_att.append((1,2))

# --- Transformation du Net vers Attr
attObj = ClusterLib.Net2Att(netObj, ClusterLib.attMethods.transform.naiveTransform)
print(netObj)
print(attObj)

# --- Transformation du Net vers Attr
#t = ClusterLib.loadData_Net("./dataset/graph/karate.gml")
#print(t)
test_netw = ClusterLib.Att2Net(test_att, ClusterLib.netMethods.transform.naiveTransform, k=1)
print(test_att)
print(test_netw)

clust = ClusterLib.cluster_Net(t, ClusterLib.netMethods.clustering.labelPropagation)
print(clust)
