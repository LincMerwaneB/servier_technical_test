""" script to generate a graph from csv_json file """
import logging
from pathlib import Path
from src import import_data as imp
from src import graph_function as gr

logging.basicConfig(filename=Path(Path(__file__).parents[0],'logs','log.txt'),
                    level=logging.ERROR)

if __name__ == "__main__":

    logging.info("----- STEP 1 - Importing files -----")
    # Function that allows the loading of files in 2 dataframes
    df_drugs, df_journal = imp.import_dir_to_dataframe()

    logging.info("----- STEP 2 - Creating graph -----")
    # Function that takes as input the 2 previous dataframes and generates the associated graph
    graph = gr.create_graph(df_drugs, df_journal)

    logging.info("----- STEP 3 - Creating graph -----")
    # Export function of the previously generated graph
    gr.export_json_graph(graph, filename = 'drug_graph.json')

    logging.info("----- STEP 4 - Creating graph -----")
    #Fonction qui permet de récupérer le journal qui mentionne le plus de médicaments différents
    gr.max_mention(filename = 'drug_graph.json')
    logging.info("----- Processing completed -----")
