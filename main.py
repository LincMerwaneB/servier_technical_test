""" script to generate a graph from csv_json file """
from src import import_data as imp
from src import graph_function as gr

# Function that allows the loading of files in 2 dataframes
df_drugs, df = imp.import_dir_to_dataframe()

# Function that takes as input the 2 previous dataframes and generates the associated graph
graph = gr.create_graph(df_drugs, df)

# Export function of the previously generated graph
gr.export_json_graph(graph, filename = 'drug_graph.json')

#Fonction qui permet de récupérer le journal qui mentionne le plus de médicaments différents
gr.max_mention(filename = 'drug_graph.json')
