#!/usr/bin/python

import networkx as nx
import matplotlib.pyplot as plt

import sys
import StateMachine

def draw_graph(graph, node_labels, edge_labels,
                graph_layout='shell',
                node_size=12000, node_color='blue', node_alpha=0.3, node_text_size=10,
                edge_color='blue', edge_alpha=0.3, edge_tickness=1, edge_text_pos=0.3,
                text_font='sans-serif'):

    G = nx.MultiDiGraph()

    for edge in graph:
        G.add_edge(edge[0], edge[1])

    if graph_layout == 'spring':
        graph_pos = nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos = nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos = nx.random_layout(G)
    else:
        graph_pos = nx.shell_layout(G)

    # draw graph

    nx.draw_networkx_nodes(G, graph_pos, node_size=node_size, alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_labels(G, graph_pos, node_labels, nodefont_size=node_text_size, font_family=text_font)

    nx.draw_networkx_edges(G, graph_pos, width=edge_tickness, alpha=edge_alpha, edge_color=edge_color )

    edge_labels_dictionary = dict(zip(graph, edge_labels))
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels_dictionary, label_pos=edge_text_pos)

    plt.show()


def main():

    if not sys.argv[1]:
        print "usage: ", sys.argv[0], "transition table"
        exit(1)

    fsm = StateMachine.StateMachine(sys.argv[1]) #"test_table.txt")

    index = 0
    transition_to_index = {}
    node_labels = {}
    for trans in fsm.transitions:
        transition_to_index[trans] = index
        node_labels[index] = trans
        index = index + 1

    #transition_to_index['End'] = index
    #node_labels[index] = 'End'

    graph = []
    edge_labels = []
    for state in fsm.transitions:
        state_index = transition_to_index[state]
        for event in fsm.transitions[state]:
            new_state = fsm.transitions[state][event]
            new_state_index = transition_to_index[new_state]
            graph.append((state_index, new_state_index))
            edge_labels.append(event[:-5])

    draw_graph(graph, node_labels, edge_labels, graph_layout="shell") #, edge_labels)

if __name__ == '__main__':

    main()

