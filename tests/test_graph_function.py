""" Unit test for graph_function module """
import networkx as nx
import pytest
from src import import_data as imp
from src import graph_function as gr


def test_graph_function():
    """ test the function test_graph_function graph type"""
    df_drugs, df_journal = imp.import_dir_to_dataframe()
    graph = gr.create_graph(df_drugs, df_journal, show = False)
    assert isinstance(graph, nx.classes.digraph.DiGraph) is True

def test_graph_function_entry():
    """ test the function test_graph_function entry var """
    with pytest.raises(TypeError, match='Drugs not a dataframe'):
        gr.create_graph('df', 'df_journal')
