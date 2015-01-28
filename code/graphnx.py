__author__ = 'Zhongpeng Lin'
"""
Graph algorithms implemented with networkx
"""
from networkx import Graph, DiGraph
import sys
import re
import itertools
import time


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
        if degree <= 2:
            return node
        elif degree < least_degree:
            least_degree = degree
            least_degree_node = node
    return least_degree_node


def degeneracy_wedge_iterator(graph):
    """
    The graph will be destroyed while iteration
    :param graph:
    :yield: wedges
    """
    while graph.number_of_nodes() > 0:
        node = get_least_degree_node(graph)
        successors = graph.successors(node)
        for pair in itertools.combinations(successors, 2):
            yield (node, pair)
        graph.remove_node(node)


def count_triangle_degeneracy_wedge_iteration(graph):
    n = 0
    for wedge in degeneracy_wedge_iterator(graph):
        if graph.has_edge(wedge[1][0], wedge[1][1]):
            n += 1
    return n

if __name__ == '__main__':
    g = read_dag(sys.argv[1])
    print('Number of directed edges:', g.number_of_edges())
    n = 0
    start_time = time.time()
    n = count_triangle_degeneracy_wedge_iteration(g)
    print('Number of triangles:', n)
    print('Time used:', time.time() - start_time)