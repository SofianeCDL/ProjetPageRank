# LLDM-gcp-project


Projet réalisé dans le cadre de l’UE de Gestion des données distribuées à large échelle.

**Enseignement** : Molli Pascal

**Diplome** : Master 2 Informatique, Université de Nantes

**Campus** : Michelet-Sciences

**Date** : 20/10/2023



## Authors

- Lou-Anne Sauvêtre [@LouAnneSVTR](https://www.github.com/LouAnneSVTR)
- Sofiane Couëdel [@SofianeCDL](https://www.github.com/LouAnneSVTR](https://github.com/SofianeCDL))
- Nicolas Bitaillou [@Stevehunn](https://www.github.com/Stevehunn)


## Introduction

L'algorithme PageRank est un algorithme clé pour le classement des pages web, inventé par les fondateurs de Google, Larry Page et Sergey Brin. Il évalue la pertinence des pages en fonction du nombre et de la qualité des liens pointant vers elles. PageRank a révolutionné les moteurs de recherche et est au cœur de l'analyse de réseaux.

Ce projet vise à  comparer les performances de deux cadres de traitement de données populaires, Pig et PySpark, dans le contexte de l'application de l'algorithme PageRank à des graphes massifs. Cette comparaison est inspirée d'une démonstration qui a eu lieu lors de la conférence NDSI 2012, où les Resilient Distributed Datasets (RDD) ont été présentés comme un outil révolutionnaire pour le traitement de données distribuées.
Nous effectuerons cette comparaison avec l'outil Google Cloud PLatform (GCP).


# Objectifs du Projet
Les objectifs de notre projet sont les suivants :

1. **Rédaction du Code Python pour PageRank** : Développement d'un code Python pour mettre en œuvre PageRank avec Pig et PySpark, en prenant en charge 2, 4 et 6 nœuds.

2. **Tests Initiaux** : Effectuer des tests préliminaires de PageRank avec 2 nœuds et un petit fichier de 20 mo pour évaluer les performances initiales.

3. **Tests Finaux** : Réaliser des tests finaux en utilisant un fichier de données de 800 mo pour évaluer les performances sur des graphes de plus grande envergure.

4. **Comparaison** : Annalyse comparative entre nos résultats pour Pig et PySpark.

Ces objectifs aideront à évaluer l'efficacité des implémentations PageRank sur GCP, en vue de futurs projets d'analyse de graphes à grande échelle.

Les fichiers sources : https://github.com/momo54/large_scale_data_management

# 1 - Configuration

Afin d'évaluer les performances entre les implémentations Pig et PySpark, nous avons utilisé le service d'exécution de tâches Dataproc de la suite Google Cloud. NOus avons décidé d'utiliser Python pour réaliser notre projet. Aussi nous avons comme fichiers : 

**Code sources Pig et PySpark** : *large_scale_data_management
/dataproc.py* et *large_scale_data_management/pyspark
/pagerank.py*.

**Configuration du Cluster** : Nous avons défini la région du cluster sur *"europe-central2"*, type de machine *"machine_type_uri: n1-standard-4"*.

**Nombre de Nœuds** : Selon la consigne, ous avons utilisé 2, 4 et 6 nœuds en fonction des restrictions de quota et des besoins en puissance de calcul pour exécuter les algorithmes.

**Données d'Entrée** : Nous avons préchargé le jeu de données *"lddm_data/small_page_links.nt 3*" dans le bucket public *"gs://public_lddm_data/small_page_links.nt 3"* au sein de l'impémentation Pig et dasn la commande de lancement de PySpark.
Les données d'entrées finales sont **A COMPLETER**

**Licences** : http://www.apache.org/licenses/LICENSE-2.0 pour PySpark.


# 2. Tests préliminaires
Execution des tests préliminaire avec les commandes :

```bash
  python3 lddm_svtr.py 'bucket_name' 'region' 'cluster_name'
```

```bash
  python3 lddm_svtr.py
```
Avec comme paramètres prédéfinis dans le code : 
- project_id   = "lsdm-40181"
- region       = "europe-central2"
- cluster_name = "clusterlsdm"

Résultats : 

Visible en brut sous format txt au lancement du programme dans le fichier *result_data.txt*. 
Les configurations de bases étant fixées à 2 noeuds avec *lddm_data/small_page_links.nt 3* comme jeu de données. 


Comparaison préliminaire : 

Les résultats préliminaires de ce benchmark indiquent que Spark, face à Pig, a montré des performances supérieures en termes de temps de calcul.
En effet, prenons par exemple deux noeuds, PySpark avec 38.01116800308227	et Pig avec 191.1238124370575s. PySpark est 80% fois plus rapide que Pig. 

On s'attend ainsi, pour le fichier de 800mo à constater une différence bien supérieurs entre PySpark et Pig.



# 3. Tests finaux

Nous avons testés avec le fichier de grande taille, 800mo. Cette fois-ci, on joute également la version de PySpark avec partitionnement.

| Pig | Nombre de noeuds |   
| :-------- | :------------------------- |
| `49 min 35 s` | 3 | 
| `40 min 54 s` | 4 | 
| `36 min 22 s` | 5 | 

| PySpark sans partitionnement| Nombre de noeuds      
| :------- | :------------------------- | 
| `46 min 18 s` |3 | 
| `40 min 32 s` |4 |
| `36 min 24 s` |5 |

| PySpark avec partitionnement| Nombre de noeuds      
| :------- | :------------------------- | 
| `33 min 39 s `  |3 |
| `31 min 55 s`   |4 |
| `31 min 03 s`   |5 |


# 4. Observation


Comparaison finale : 

On observe une légère différence de temps d'execution entre Pig et PySpark, le plus rapide étant PySpark avec partitionnement 

![alt text](https://github.com/SofianeCDL/ProjetPageRank/blob/main/Graph.png)

On observe alors que PySpark avec partitionnement affiche les meilleures performances parmi les trois configurations présentées. On peut ainsi penser que le partitionnement joue un rôle essentiel en permettant une répartition efficace des charges de travail. On voit cependant que l'ajoute de noeud ne réduit que de peu la vitesse d'execution.

PySpark sans partitionnement démontre des performances plus rapide que Pig mais de peu contrairement à nos essais préliminaires pour un nombre de nœuds équivalent.


# Conclusion finale 

Cette comparaison met en évidence la capacité de PySpark et Pig avec partitionnement à traiter rapidement des tâches. Globalement, l'ajout de nœuds (par exemple, en passant de 3 à 6 nœuds) améliore dans tous les cas les performances.
PySpark sans partitionnement est légèrement plus rapide que Pig qui lui est le moins performant en termes de vitesse d'exécution. Le choix entre les deux technologies doit être basé sur les besoins spécifiques de chaque projet et sur la balance entre la simplicité d'utilisation de Pig et la vitesse de PySpark. D'après nos tests et nos observations, Pig et PySpark se valent, on rapelle que pour 5 noeuds les temps d'executions étaint presque semblables.

En résumé, si les performances sont un critère essentiel, l'utilisation de PySpark avec partitionnement semble être la meilleure option parmi les trois, avec des temps d'exécution significativement plus courts. Cependant, le choix entre Pig et PySpark sans partitionnement dépendra des besoins spécifiques de votre cas d'utilisation.




## Documentation

[Gestion de cluster en Python](https://cloud.google.com/dataproc/docs/tutorials/python-library-example?hl=fr)

