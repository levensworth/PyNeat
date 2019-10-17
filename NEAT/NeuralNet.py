import math
from NEAT.NodeGene import NodeGeneType
from collections import OrderedDict
def sigmoid(x, treshold):
    return math.exp(x) / (math.exp(x)+1)


class NeuralNet(object):
    def __init__(self, gene):
        self.nodes = self.create_graph(gene)

    def create_graph(self, gene):
        """
        this method should create a network based on the genetical encoding
        :param gene: a Genome
        :return: a graph strucure representing the network
        """
        nodes = {}
        for node in gene.nodes.values():
            nodes[node.get_id()] = Node(sigmoid, node.get_type(), node.get_id())

        for connection in gene.connections.values():
            if not connection.enable:
                break
            in_node = nodes[connection.get_in_node()]
            out_node = nodes[connection.get_out_node()]

            in_node.add_out_node_connection(Connection(in_node, out_node, connection.weight
                                                       , connection.innovation_number))
            out_node.add_in_node_connection(Connection(in_node, out_node, connection.weight
                                                       , connection.innovation_number))
        # we sort the keys to maintain the order between iterations
        # nodes = sorted(nodes, key=nodes.get)
        return nodes

        # now we sort the list by type and sub sort by innovation number

    def predict(self, input_values):
        """
        this method will try to redict an out given a numpy array input
        :param input_values: numpy vector where each row represents a single input
        :return:
        """
        in_nodes = []
        out_nodes = []
        for node in self.nodes.values():
            if node.neuron_type == NodeGeneType.INPUT:
                in_nodes.append(node)
            elif node.neuron_type == NodeGeneType.OUTPUT:
                out_nodes.append(node)

        if len(input_values) != len(in_nodes):
            raise AttributeError('input size is {} and should be {}'.format(input_values.shape[1], len(in_nodes)))

        # set the input vector
        index = 0
        for node in in_nodes:
            node.receive_input(input_values[index])

        conn_stack = []
        for node in out_nodes:
            for child_conn in node.in_nodes.values():
                conn_stack.append(child_conn)

        # now starts the fun part ;)
        while len(conn_stack) is not 0:
            current_conn = conn_stack.pop()

            if current_conn.visited:
                # we mark as visited the child node
                # because it's output has already being calculated
                current_conn.in_node.visited = True
                # send the output to the father
                result = current_conn.in_node.process()
                result = result * current_conn.weight
                current_conn.out_node.receive_input(result)
            else:
                # we visit the connection
                current_conn.visited = True
                conn_stack.append(current_conn)
                if current_conn.in_node.neuron_type == NodeGeneType.INPUT:
                    # it's an input so we only get the input passed
                    result = current_conn.in_node.input_val
                    result = result * current_conn.weight
                    current_conn.out_node.receive_input(result)
                # and we append it's children
                for conn in current_conn.in_node.in_nodes.values():
                    conn_stack.append(conn)

        # at this point all output nodes have their values
        result = []
        # we should always sort output nodes
        out_nodes.sort(key=lambda x: x.marker)
        for node in out_nodes:
            result.append(node.process())
        return result


class Node(object):
    """
    This class represents a node in a neural net graph,
    as the underlying structure is a graph, the output computation can be solved as a pre-order or post-order
    (for algorithmic reasons) search throw the graph. For that purpose, we start by visiting the output nodes.

    """
    def __init__(self, activation, neuron_type, marker, threshold=0.1):
        self.threshold = threshold
        self.activation = activation
        self.neuron_type = neuron_type
        self.marker = marker
        self.in_nodes = {}
        self.out_nodes = {}
        self.input_val = 0
        self.visited = False

    def process(self):
        return self.activation(self.input_val, self.threshold)

    def add_in_node_connection(self, connection):
        self.in_nodes[connection.innovation_number] = connection

    def add_out_node_connection(self, connection):
        self.out_nodes[connection.innovation_number] = connection

    def receive_input(self, value):
        self.input_val += value

    def __lt__(self, other):
        return self.marker < other.marker

class Connection(object):
    """
    Representation of a connection between nodes
    """
    def __init__(self, in_node, out_node, weight, innovation_number):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.visited = False
        self.innovation_number = innovation_number
