__author__ = 'Zhongpeng Lin'
"""
Graph algorithms implemented with networkx
"""
from networkx import Graph, DiGraph
import sys,re


def read_graph(file):
    g = Graph()
    with open(file, 'r') as graph_file:
        for line in graph_file:
            if not line.startswith('#'):
                nodes = line.split('\t')
                g.add_edge(int(nodes[0]), int(nodes[1]))
    return g


def read_dag(file):
    g = DiGraph()
    with open(file, 'r') as graph_file:
        for line in graph_file:
            if not line.startswith('#'):
                nodes = re.split('\s+', line.strip(), 1)
                from_node = int(nodes[0])
                to_node = int(nodes[1])
                if to_node > from_node:
                    g.add_edge(from_node, to_node)
    return g


def create_dag_from(graph):
    dag = DiGraph()
    for edge in graph.edges_iter():
        if edge[1] > edge[0]:
            dag.add_edge(edge[0], edge[1])
    return dag


def get_least_degree_node(graph):
    """
    :param graph:
    :return: the node with least degree. If there are multiple, return one of them
    """
    least_degree_node = None
    least_degree = graph.number_of_nodes()
    for node, degree in graph.degree_iter():
        if degree == 1:
            return node
        elif degree < least_degree:
            least_degree = degree
            least_degree_node = node
    return least_degree_node

if __name__ == '__main__':
    g = read_dag(sys.argv[1])
    print('Number of directed edges:', g.number_of_edges())
    print('Least degree:', g.degree(get_least_degree_node(g)))