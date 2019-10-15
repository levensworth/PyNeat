from NEAT.Genome import Genome
from NEAT.NodeGene import NodeGene, NodeGeneType
from NEAT.ConnectionGene import ConnectionGene, InnovationGenerator
from random import Random as Rand


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


def given_another_genome():

    node1 = NodeGene(NodeGeneType.INPUT, 1, 1)
    node2 = NodeGene(NodeGeneType.INPUT, 2, 2)
    node3 = NodeGene(NodeGeneType.INPUT, 3, 3)
    node4 = NodeGene(NodeGeneType.OUTPUT, 4, 4)
    node5 = NodeGene(NodeGeneType.HIDDEN, 5, 5)
    node6 = NodeGene(NodeGeneType.HIDDEN, 6, 6)

    nodes = {node1.get_id(): node1, node2.get_id(): node2, node3.get_id(): node3, node4.get_id(): node4,
             node5.get_id(): node5, node6.get_id(): node6}

    conn1 = ConnectionGene(node1.get_id(), node4.get_id(), 0.8, innovation_number=1)
    conn2 = ConnectionGene(node2.get_id(), node4.get_id(), -0.4, False, 2)
    conn3 = ConnectionGene(node3.get_id(), node4.get_id(), 0.5, innovation_number=3)
    conn4 = ConnectionGene(node2.get_id(), node5.get_id(), 0.2, innovation_number=4)
    conn5 = ConnectionGene(node5.get_id(), node6.get_id(), 0.4, innovation_number=5)
    conn6 = ConnectionGene(node3.get_id(), node5.get_id(), 0.6, innovation_number=6)
    conn7 = ConnectionGene(node1.get_id(), node6.get_id(), 0.6, innovation_number=7)
    conn8 = ConnectionGene(node6.get_id(), node4.get_id(), 0.6, innovation_number=8)

    connections = {conn1.get_innovation_number(): conn1, conn2.get_innovation_number(): conn2,
                   conn3.get_innovation_number(): conn3, conn4.get_innovation_number(): conn4,
                   conn5.get_innovation_number(): conn5, conn6.get_innovation_number(): conn6,
                   conn7.get_innovation_number(): conn7, conn8.get_innovation_number(): conn8}
    genome = Genome(connections, nodes, InnovationGenerator())
    return genome


def test_representation_genome():
    genome = given_a_genome()
    print(genome)


def test_crossover():
    genome1 = given_a_genome()
    genome2 = given_another_genome()
    new_genome = Genome.crossover(genome2, genome1)

    print(new_genome)


def test_add_node():
    genome = given_a_genome()
    true_result = given_a_genome()
    node6 = NodeGene(NodeGeneType.HIDDEN, 5, 5)
    true_result.nodes[5] = node6
    conn1 = ConnectionGene(1, 5, 1, innovation_number=13)
    conn2 = ConnectionGene(5, 3, 0.3, innovation_number=14)
    true_result.connections[13] = conn1
    true_result.connections[14] = conn2
    rand = TestRandom()
    genome.add_node_mutation(rand)
    print(genome == true_result)


def test_add_connection():
    genome = given_a_genome()
    true_result = given_a_genome()
    conn7 = ConnectionGene(2, 4, 0.3, innovation_number=12)
    true_result.connections[12] = conn7
    rand = TestRandom()
    genome.add_connection_mutation(rand)
    print(true_result == genome)


def test_distance():
    genome_less_fitted = given_a_genome()
    genome_more_ftted = given_another_genome()

    distance = Genome.compute_distance(genome_less_fitted, genome_more_ftted, 1, 1, 1)
    print(distance)

class TestRandom(object):
    def __init__(self):
        self.index = 0

    def randint(self, min_int, max_int):
        self.index += 2
        return self.index

    def random(self):
        return 0.3


if __name__ == '__main__':
    # test_representation_genome()
    test_add_connection()
    test_add_node()
    #test_crossover()
    test_distance()
