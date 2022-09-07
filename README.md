# servier_technical_test

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

|───── test_graph_function.py

|───── test_import_data.py

|── main.py

|── requirements.txt

|── setup.py


Ce repo définit un pipeline permettant de générer un graphe de liaison entre des médicaments et leurs mentions dans des articles/journaux.
Pour ce faire, j'ai choisi d'utiliser le package pandas pour la manipulation des données en raison de sa simplicité et j'ai choisi le package networkx pour tracer le graphe.
En effet, après quelques recherches, networkx semblait convenir pour la représentation d'un tel graphe tout en ayant des fonctionnalitées intéressantes (par exemple le support des graphes directionnels).

Les données concernant les médicaments et les journaux sont stockées dans des fichiers CSV et JSON dans le répertoire "data".

Le lancement du pipeline se fait en exécutant le fichier "main.py".
Ce fichier va exécuter les traitements suivants :
  * import_data : ce traitement va récupèrer les chemins des fichiers json/csv à traiter dans le repertoire data pour les charger dans un dataframe puis il va les préparer pour être exploitable (suppression de charactère en trop, ajout d'id, etc...).
  * graph_function : ce traitement va tracer le graphe de liaison entre les médicaments et les journaux à partir des dataframes fournies (et des règles de gestion) puis l'enregistrer dans un fichier au format json dans le repertoire "json_export"
  
  ![image](https://user-images.githubusercontent.com/79836255/188482557-d7a4726b-30a6-4cb2-8049-3f436aef3020.png)

Ce graphe permet d'illustrer simplement les liens entre les médicaments, les articles et les journaux :
 * Chaque noeud correspond à une entitée (médicament, journaux, article) 
 * Chaque flèche répresente l'action "mentionné par".

2 - Comment exécuter le script
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Pour exécuter le pipeline il faut :
  * télécharger le repo
  * exécuter la commande "pip install -e ." depuis le répertoire racine du package
  * exécuter le fichier "main.py"

L'exécution du fichier "main.py" crééra le fichier json du graphe dans le repertoire "json_export" et affichera le ou les journaux mentionnant le plus de médicaments.

3 - Question

Pour traiter un volume plus important de fichier il faudra surement modifier la fonction pandas.read() avec les attributs chunksize et low_memory ou bien passer sur des solutions plus adaptées à des volumes massifs de données.
On peut par exemple imaginer une architecture cloud dans GCP avec le chargement des fichiers via dataflow, des traitements dans bigquery et le tracé du graphe via dataproc ou cloud run.

3 - SQL
---------------------------------------------------------------------------------------------------------------------------------------------------------------------
Les requêtes SQL sont dans le repertoire SQL.
