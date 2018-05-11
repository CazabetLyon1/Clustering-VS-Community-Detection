import ClusterLib
import csv

nbrCore = 6

# --- Load Data :
#data :
attrFile = ["data/att/s2", "data/att/birch1", "data/att/birch2", "data/att/dim032", "data/att/dim064", "data/att/dim128", "data/att/dim256", "data/att/s1", "data/att/s3" ,"data/att/s4"]
netwFile = ["data/net/chaine", "data/net/dolphins", "data/net/football", "data/net/interconnexion_totale", "data/net/karate", "data/net/clique"]

print("loading ....")
for i in range(len(attrFile)) :
	#load data.
	attr = ClusterLib.loadData_Att(attrFile[i]+".csv")
	#load ground truth.
	temp = csv.reader(open(attrFile[i] + "_labels.csv","r"))
	groundTruth = []
	for row in temp: groundTruth.append(int(row[0]))

	#on teste pour différents k.
	for k in range(1,11) :
		methodNet = ["infomap", "louvain", "labelPropagation", "nestedBlockmodel"]
		print('att -> net ' + str(k))
		#transformation.
		net = ClusterLib.Att2Net(attr,ClusterLib.netMethods.transform.naiveTransform,k=k, Core=nbrCore)
		#calcule f1score et AMI pour chaque méthode.
		for m in methodNet :
			print(m)
			method = getattr(ClusterLib.netMethods.clustering, m)
			cluster = ClusterLib.cluster_Net(net, method)
			f1 = ClusterLib.Metric.f1(groundTruth,cluster)
			ami = ClusterLib.Metric.ami(groundTruth,cluster)
			print("avec le fichier " + attrFile[i] + " et pour k = " + str(k) + " : \nami = " + str(ami) + "\nf1score = " + str(f1))
			mon_fichier = open("resultat/fichier=" + str(i) + "_k=" + str(k) + "_method=" + m + ".txt", "w")
			mon_fichier.write("f1 = " + str(f1) + "\n")
			mon_fichier.write("ami = " + str(ami) + "\n")
			mon_fichier.write("\n network :\n\n")
			mon_fichier.write(str(net))
			mon_fichier.write("\n \n \n \n cluster :\n\n")
			mon_fichier.write(str(cluster))
			mon_fichier.close()
