import ClusterLib

# --- Creation d'un Net object
netObj = []
netObj.append((1,2))
netObj.append((1,3,2))
netObj.append((1,4))
netObj.append((2,4,7))
netObj.append((3,5))

# --- Transformation du Net vers Attr
attObj = ClusterLib.Net2Att(netObj, ClusterLib.attMethods.transform.naiveTransform)
print(netObj)
print(attObj)