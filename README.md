# servier_technical_test
Un data pipeline qui trace un graphe de liaison à partir de fichier plat

1 - Présentation
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
Le repo est organisé comme ci-dessous :

|── data
|── json_export
|── SQL
|── src
|───── graph_function.py
|───── import_data.py
|── tests
|── main.py
|── test_import_data.py

Ce repo définit un pipeline permettant de générer un graphe de liaison entre des médicaments et des publications à partir des fichiers CSV et JSON présent dans le répertoire data.
Le lancement du pipeline se fait en exécutant le fichier "main.py".
Ce fichier va exécuter les traitements suivants :
  * import_data : ce traitement va récupèrer les chemins des fichiers json/csv à traiter dans le repertoire data pour les charger dans un dataframe puis il va les préparer pour etre exploitable (suppression de charactère en trop, ajout d'id, etc...)
  * graph_function : ce traitement va tracer le graphe de liaison entre les médicaments et les publications à partir des dataframes fournies (et des règle de gestion) puis l'enregistrer dans un fichier au format json dans le repertoire json_export
  
  ![image](https://user-images.githubusercontent.com/79836255/188482557-d7a4726b-30a6-4cb2-8049-3f436aef3020.png)

Ce graphe réalisé grace au package networkx permet d'illustrer les liens entre les médicaments, les articles et les journaux. Chaque noeud correspond a une entitée (médicament, journaux, article) et les flèches répresentent l'action "mentionnée par".

2 - Comment exécuter le script
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Pour exécuter le pipeline il faut :
  * installer les packages du fichier "requirements.txt"
  * exécuter le fichier main.py
L'exécution du fichier main crééra le fichier json du graphe et affichera le ou les journaux mentionnant le plus de médicaments.

3 - Question

Pour traiter plus de volume il faudra surement modifier la fonctions pandas.read() avec les attributs chunksize et low_memory ou bien passer sur des solutions plus adaptées a des volumes massive de données.
On peut par exemple imaginer une architecture cloud dans GCP avec le chargement des fichiers via dataflow et des traitements dans bigquery et le tracé du graphe via dataproc ou cloud run.

4 SQL
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Les requêtes SQL sont dans le repertoire SQL.
