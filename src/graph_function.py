"""This module convert dataframe into JSON graph."""
import json
from os.path import exists
from pathlib import Path
import collections
from operator import itemgetter
import networkx as nx #package pour les graphes
import pandas as pd
from networkx.readwrite import json_graph
from matplotlib import pyplot as plt


# init default export path
export_path =Path(Path(__file__).parents[1],'json_export')

def create_graph(drugs, publications, show = True) :
    """Create a graph from two dataframe

    Parameters
    ----------
    drugs : dataframe
    publications : dataframe

    Returns
    -------
    Graph object
        a graph with drug linked to publication

    Raises
    ------
    ValueError
        Error drugs header.
        Error publications header.
    """

    if isinstance(drugs, pd.core.frame.DataFrame) is False :
        raise TypeError("Drugs not a dataframe")
    if isinstance(publications, pd.core.frame.DataFrame) is False :
        raise TypeError("Publication not a dataframe")

    check_drugs = ['atccode', 'drug']
    check_publications = ['id', 'title', 'date', 'journal', 'source', 'id_source', 'id_journal']
    # check dataframe column
    if collections.Counter(list(drugs.columns)) == collections.Counter(check_drugs):
        print ('Drugs header OK')
    else:
        raise ValueError("Error drugs header")
    if collections.Counter(list(publications.columns)) == collections.Counter(check_publications):
        print ('Publication header OK')
    else:
        raise ValueError("Error publication header")

    # I chose to draw a directional graph between drugs and newspapers
    graph = nx.DiGraph()
    for row in drugs.itertuples():
        # initialize first node with drug name
        graph.add_node(row.drug)
        for publication in publications.itertuples() :
            # uppercase title for comparison
            title = publication.title.upper()
            # verification of the mention of the drug in the title
            if title.find(row.drug)!=-1 :
                # creating an id from the source name and index to name the node
                pub_node_name = publication.source + '_' + str(int(publication.id_source))
                graph.add_nodes_from([(pub_node_name,
                                       {'id' : publication.id,
                                        'title' : publication.title,
                                        'journal' : publication.journal,
                                        'date' : publication.date.strftime('%Y-%m-%d')})])
                # creation of the relationship between the drug and the diary
                graph.add_edge(row.drug, pub_node_name)
                if publication.journal != 'Empty' :
                    # creating an id for the journal to name the node
                    jour_node_name = 'journal' + '_' + str(int(publication.id_journal))
                    graph.add_nodes_from([(jour_node_name, {'journal' : publication.journal})])
                    graph.nodes[jour_node_name][row.atccode]={ 'drug' : row.drug,
                                                              'date' :
                                                                  publication.date.strftime('%Y-%m-%d')}
                    graph.add_edge(row.drug, jour_node_name)
    print('==> Graph completed')
    if show is True :
        # graph preview
        nx.draw(graph,pos= nx.spring_layout(graph), with_labels=True, font_weight='bold')
        plt.show()
    return graph


def export_json_graph(graph, directory = export_path, filename = 'drug_graph.json'):
    """Export graph at json format to the parameters directory

    Parameters
    ----------
    graph : graph object
    directory : path
    filename : str
    """

    path = Path(directory, filename)
    # write json to file
    with open(path, 'w') as file:
        json.dump(json_graph.node_link_data(graph), file)
        print('==> export file done :\n', path.resolve())


def read_json_file(directory = export_path, filename = 'drug_graph.json'):
    """Read a graph from json

    Parameters
    ----------
    directory : path
    filename : str

    Returns
    -------
    Graph object
        a graph with drug linked to publication

    Raises
    ------
    ValueError
        File not found.
    """

    path = Path(directory, filename)
    # checking that json exists
    if exists(path) is False:
        raise ValueError("File {} not found".format(path))
    # read json
    with open(path) as file:
        js_graph = json.load(file)
    return json_graph.node_link_graph(js_graph)


def max_mention(directory = export_path, filename = 'drug_graph.json'):
    """Read a graph from json

    Parameters
    ----------
    directory : path
    filename : str

    Returns
    -------
    list
        list of string with journal name
    """

    # load the graph file
    graph = read_json_file(directory, filename)
    # retrieval of the number of incoming links by nodes
    degree = list(graph.in_degree())
    # recovery of the max value
    nb_liasion_max= max(degree,key=itemgetter(1))[1]
    # identification of the newspapers having mentioned this number of drugs
    journaux = [item for item in degree if item[1] == nb_liasion_max]
    result = []
    for journal in journaux:
        # the nodes have the same structure as the dicts
        result.append(graph.nodes[journal[0]]['journal'])
    result = [*set(result)]
    if len(result) == 1:
        print('The journal citing the most drug :\n\t{}\n'
              'Number of different drugs cited : {}'.format(result[0],nb_liasion_max))
    else :
        print('The journals that cited the most drugs are :\n'
              '\t{}\nNumber of different drugs cited : {}'.format(result,nb_liasion_max))
    return result
