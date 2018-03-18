# Clustering VS Community Detection

## Description

A l'heure actuelle, le clustering est divisé en deux grands domaines qui se sont développés indépendemment

* Le Clustering classique travaille sur des données ayant un ensemble de propriétés (ex: pour une personne : âge, genre, revenu, lieu de résidence, ...), mais chaque donnée peut être considéré indépendemment
* La détection de communautés (ou clustering de graphe) travaille sur des données relationnelles, c'est à dire n'ayant pas de propriétés associées aux données, mais seulement des relations entre elles (les relations peuvent avoir des propriétés, typiquement des types ou des poids différents). Ces données sont typiquement représentées par des graphes, ou réseaux.

Cette librairie permet de facilement comparer les méthodes classiques des deux approches sur des problèmes commun.

## Contenu
#### Librairie
* **ClusterLib.py**
fonctions de chargement, transformation, clustering et valuation des des données
 * **AttClustering.py**
 fonctions spécifiques aux données attribuées
 * **NetClustering.py**
 fonctions spécifiques aux graphes
 
#### Exécution
Le fichier _Main.py est ouvert à la modification dans l'optique de jouer avec la librairie
> $ python3 _Main.py

## Membres

Encadrant

 * **Cazabet Rémy**, Associate Professor, Univ. Lyon, UCBL, LIRIS, Lyon, France

Etudiants

* **Castaneda Hugo**, Master 1 Informatique, Univ. Lyon, UCBL, Lyon, France
* **Jourdan Luca**, Master 1 Informatique, Univ. Lyon, UCBL, Lyon, France
