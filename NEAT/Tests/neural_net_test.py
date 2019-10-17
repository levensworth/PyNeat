from NEAT import NeuralNet
from NEAT.Genome import Genome
from NEAT.NodeGene import NodeGene, NodeGeneType
from NEAT.ConnectionGene import ConnectionGene, InnovationGenerator
import numpy as np

def given_a_genome():
    node1 = NodeGene(NodeGeneType.INPUT, 0, 0)
    node2 = NodeGene(NodeGeneType.INPUT, 1, 1)
    node3 = NodeGene(NodeGeneType.INPUT, 2, 2)
    node4 = NodeGene(NodeGeneType.OUTPUT, 3, 3)
    node5 = NodeGene(NodeGeneType.HIDDEN, 4, 4)

    nodes = {node1.get_id(): node1, node2.get_id(): node2, node3.get_id(): node3, node4.get_id(): node4,
             node5.get_id(): node5}
    conn1 = ConnectionGene(node1.get_id(), node4.get_id(), 0.7, innovation_number=1)
    conn2 = ConnectionGene(node2.get_id(), node4.get_id(), -0.5, False, 2)
    conn3 = ConnectionGene(node3.get_id(), node4.get_id(), 0.5, innovation_number=3)
    conn4 = ConnectionGene(node2.get_id(), node5.get_id(), 0.2, innovation_number=4)
    conn5 = ConnectionGene(node5.get_id(), node4.get_id(), 0.4, innovation_number=5)
    conn6 = ConnectionGene(node1.get_id(), node5.get_id(), 0.6, innovation_number=6)
    conn7 = ConnectionGene(node4.get_id(), node5.get_id(), 0.6, False, innovation_number=11)

    connections = {conn1.get_innovation_number(): conn1, conn2.get_innovation_number(): conn2,
                   conn3.get_innovation_number(): conn3, conn4.get_innovation_number(): conn4,
                   conn5.get_innovation_number(): conn5, conn6.get_innovation_number(): conn6,
                   conn7.get_innovation_number(): conn7}
    inno = InnovationGenerator()
    inno.counter = 11
    genome = Genome(connections, nodes, inno)
    return genome


def given_an_input_out_set():
    x = [1,1,1]
    y = [0.7706068548532662]

    return np.array(x), np.array(y)

def test_net_formation():
    genome = given_a_genome()
    net = NeuralNet.NeuralNet(genome)
    print(net)


def test_input():
    genome = given_a_genome()
    net = NeuralNet.NeuralNet(genome)
    x, y = given_an_input_out_set()
    result = net.predict(x)
    print( result == y)


if __name__ == '__main__':
    test_net_formation()
    test_input()
