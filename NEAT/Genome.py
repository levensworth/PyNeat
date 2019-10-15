from NEAT.NodeGene import NodeGeneType, NodeGene
from NEAT.ConnectionGene import ConnectionGene
import random

PROBABILITY_PERTURBING = 0.1


class Genome(object):
    """
    Linear representation of network connectivity
    it contains the list of nodes and connections between them
    connections: a map of connection genes whose key is their innovation number
    nodes: a map of node gene whose key is their id
    """
    def __init__(self, connections, nodes, innovation_generator):
        self.connections = connections
        self.nodes = nodes
        self.innvation_generator = innovation_generator

    def get_connections(self):
        return self.connections

    def get_nodes(self):
        self.nodes

    def add_node_gene(self, node_gene):
        self.nodes[node_gene.get_id()] = node_gene

    def add_connection_gene(self, connection_gene):
        self.connections.append(connection_gene)

    def add_connection_mutation(self, rand):
        node_1_index = rand.choice([*self.nodes])
        node_2_index = rand.choice([*self.nodes])
        node_1 = self.nodes[node_1_index]
        node_2 = self.nodes[node_2_index]

        weight = rand.random()

        if node_1.get_type() is NodeGeneType.HIDDEN and node_2.get_type() is NodeGeneType.INPUT:
            flip = True
        elif node_1.get_type() is NodeGeneType.OUTPUT and node_2.get_type() is NodeGeneType.HIDDEN:
            flip = True
        elif node_1.get_type() is NodeGeneType.OUTPUT and node_2.get_type() is NodeGeneType.INPUT:
            flip = True
        else:
            flip = False

        connection_exist = False
        for conn in self.connections:
            conn = self.connections[conn]
            # Check if connection already exists
            if conn.get_in_node() is node_1.get_id() and conn.get_out_node() is node_2.get_id():
                connection_exist = True
                break
            elif conn.get_in_node() is node_2.get_id() and conn.get_out_node() is node_1.get_id():
                connection_exist = True
                break

        if connection_exist:
            return

        if flip:
            # swap nodes order
            aux = node_1
            node_1 = node_2
            node_2 = aux

        new_connection = ConnectionGene(node_1.get_id(), node_2.get_id(), weight, True, self.innvation_generator.get_innovation())
        self.connections[new_connection.get_innovation_number()] = new_connection

    def add_node_mutation(self, rand):
        conn_index = rand.choice([*self.connections])
        connection = self.connections.get(conn_index)
        in_node = self.nodes.get(connection.get_in_node())
        out_node = self.nodes.get(connection.get_out_node())
        connection.disable()
        new_node = NodeGene(NodeGeneType.HIDDEN, len(self.nodes)+1, self.innvation_generator.get_innovation())
        in_to_new = ConnectionGene(in_node.get_id(), new_node.get_id(), 1.0, True,
                                   self.innvation_generator.get_innovation())
        new_to_out = ConnectionGene(new_node.get_id(), out_node.get_id(), connection.get_weight(), True,
                                    self.innvation_generator.get_innovation())
        self.nodes[new_node.get_id()] = new_node
        self.connections[in_to_new.get_innovation_number()] = in_to_new
        self.connections[new_to_out.get_innovation_number()] = new_to_out

    def mutation(self, rand):
        connections = self.connections.values()
        for conn in connections:
            if rand.random() < PROBABILITY_PERTURBING:
                new_weight = conn.get_weight()
                new_weight = new_weight * ((rand.random() * 4.0) - 2.0)
                conn.set_weight(new_weight)
            else:
                new_weight = ((rand.random() * 4.0) - 2.0)
                conn.set_weight(new_weight)

    @classmethod
    def crossover(cls, parent1, parent2):
        """

        :param parent_node1: the more fit parent
        :param parent_node2: the less fit parent
        :return: a new genome
        """

        new_nodes = {}
        new_connections = {}
        # first copy most fitted parent nodes
        for fitted_node in parent1.nodes:
            fitted_node = parent1.nodes[fitted_node]
            new_nodes[fitted_node.get_id()] = fitted_node

        for connection in parent1.connections:
            connection = parent1.connections[connection]
            if connection.get_innovation_number() in parent2.connections:
                if random.random() <= 0.5:
                    child_gene = connection.__copy__()
                else:
                    child_gene = parent2.connections[connection.get_innovation_number()].__copy__()
                new_connections[child_gene.get_innovation_number()] = child_gene
            else:
                # disjoint or excess genes
                child_gene = connection.__copy__()
                new_connections[child_gene.get_innovation_number()] = child_gene

        return Genome(new_connections, new_nodes, parent1.innvation_generator)

    @classmethod
    def count_disjoint(cls, genome_1, genome_2):
        """
        By definitino a disjoint node would be that who has an innovation number lower than the max and
        does not have a counter part in the other genome
        :param  genome_1: a Genome
        :param  genome_2: a Genome
        :return: the total amount of disjoints
        """
        max_innovation_1 = 0
        for node in genome_1.nodes.values():
            if max_innovation_1 < node.innovation_number:
                max_innovation_1 = node.innovation_number

        max_innovation_2 = 0
        for node in genome_2.nodes.values():
            if max_innovation_2 < node.innovation_number:
                max_innovation_2 = node.innovation_number

        max_innovation_total = min(max_innovation_1, max_innovation_2)
        # now count disjoints
        disjoints = 0
        for i in range(max_innovation_total):
            node_1 = genome_1.nodes[i] if i in genome_1.nodes else None
            node_2 = genome_2.nodes[i] if i in genome_2.nodes else None

            if node_1 is None and node_2 is not None:
                disjoints += 1
            elif node_2 is None and node_1 is not None:
                disjoints += 1

        # now we do the same for connections
        max_innovation_1 = 0
        for node in genome_1.connections.values():
            if max_innovation_1 < node.innovation_number:
                max_innovation_1 = node.innovation_number

        max_innovation_2 = 0
        for node in genome_2.connections.values():
            if max_innovation_2 < node.innovation_number:
                max_innovation_2 = node.innovation_number

        max_innovation_total = min(max_innovation_1, max_innovation_2)
        # now count disjoints
        for i in range(max_innovation_total):
            node_1 = genome_1.connections[i] if i in genome_1.connections else None
            node_2 = genome_2.connections[i] if i in genome_2.connections else None

            if node_1 is None and node_2 is not None:
                disjoints += 1
            elif node_2 is None and node_1 is not None:
                disjoints += 1
        return disjoints

    @classmethod
    def count_matching_genes(cls, genome_1, genome_2):
        max_innovation_1 = 0
        for node in genome_1.nodes.values():
            if max_innovation_1 < node.innovation_number:
                max_innovation_1 = node.innovation_number

        max_innovation_2 = 0
        for node in genome_2.nodes.values():
            if max_innovation_2 < node.innovation_number:
                max_innovation_2 = node.innovation_number

        max_innovation_total = min(max_innovation_1, max_innovation_2)
        # now count matching
        matching = 0
        for i in range(max_innovation_total):
            node_1 = genome_1.nodes[i] if i in genome_1.nodes else None
            node_2 = genome_2.nodes[i] if i in genome_2.nodes else None

            if node_1 is not None and node_2 is not None:
                matching += 1
            elif node_2 is not None and node_1 is not None:
                matching += 1

        # now we do the same for connections
        max_innovation_1 = 0
        for node in genome_1.connections.values():
            if max_innovation_1 < node.innovation_number:
                max_innovation_1 = node.innovation_number

        max_innovation_2 = 0
        for node in genome_2.connections.values():
            if max_innovation_2 < node.innovation_number:
                max_innovation_2 = node.innovation_number

        max_innovation_total = min(max_innovation_1, max_innovation_2)
        # now count matching
        for i in range(max_innovation_total):
            node_1 = genome_1.connections[i] if i in genome_1.connections else None
            node_2 = genome_2.connections[i] if i in genome_2.connections else None

            if node_1 is not None and node_2 is not None:
                matching += 1
            elif node_2 is not None and node_1 is not None:
                matching += 1
        return matching

    @classmethod
    def count_excess_genes(cls, genome_1, genome_2):
        max_innovation_1 = 0
        for node in genome_1.nodes.values():
            if max_innovation_1 < node.innovation_number:
                max_innovation_1 = node.innovation_number

        max_innovation_2 = 0
        for node in genome_2.nodes.values():
            if max_innovation_2 < node.innovation_number:
                max_innovation_2 = node.innovation_number

        max_innovation_total = max(max_innovation_1, max_innovation_2)
        min_innovation_total = min(max_innovation_1, max_innovation_2)
        # now count excess
        excess = 0
        for i in range(min_innovation_total, max_innovation_total):
            node_1 = genome_1.nodes[i] if i in genome_1.nodes else None
            node_2 = genome_2.nodes[i] if i in genome_2.nodes else None

            if node_1 is None and node_2 is not None:
                excess += 1
            elif node_2 is None and node_1 is not None:
                excess += 1

        # now we do the same for connections
        max_innovation_1 = 0
        for node in genome_1.connections.values():
            if max_innovation_1 < node.innovation_number:
                max_innovation_1 = node.innovation_number

        max_innovation_2 = 0
        for node in genome_2.connections.values():
            if max_innovation_2 < node.innovation_number:
                max_innovation_2 = node.innovation_number

        max_innovation_total = max(max_innovation_1, max_innovation_2)
        min_innovation_total = min(max_innovation_1, max_innovation_2)
        # now count excess
        for i in range(min_innovation_total, max_innovation_total):
            node_1 = genome_1.connections[i] if i in genome_1.connections else None
            node_2 = genome_2.connections[i] if i in genome_2.connections else None

            if node_1 is None and node_2 is not None:
                excess += 1
            elif node_2 is None and node_1 is not None:
                excess += 1
        return excess

    @classmethod
    def calculate_weight_difference(cls, genome_1, genome_2):
        matching = 0
        weight_diff = 0
        # now we do the same for connections
        max_innovation_1 = 0
        for node in genome_1.connections.values():
            if max_innovation_1 < node.innovation_number:
                max_innovation_1 = node.innovation_number

        max_innovation_2 = 0
        for node in genome_2.connections.values():
            if max_innovation_2 < node.innovation_number:
                max_innovation_2 = node.innovation_number

        max_innovation_total = min(max_innovation_1, max_innovation_2)
        # now count matching
        for i in range(max_innovation_total):
            node_1 = genome_1.connections[i] if i in genome_1.connections else None
            node_2 = genome_2.connections[i] if i in genome_2.connections else None

            if node_1 is not None and node_2 is not None:
                matching += 1
                weight_diff += abs(node_1.get_weight() - node_2.get_weight())
        return weight_diff / matching

    @classmethod
    def compute_distance(cls, genome_1, genome_2, c1, c2, c3):
        """
        computes the δ = c1*(E/N) + c2*(D/N) + c3 * W
        :param genome_1: genome to compare
        :param genome_2: genome to compare
        :param c1: double
        :param c2: double
        :param c3: double
        :return: double representing how similar are genome_1 and genome_2
        """
        N = max(len(genome_1.nodes), len(genome_2.nodes))
        return c1 * (Genome.count_excess_genes(genome_1, genome_2) / N) +\
               c2 * (Genome.count_disjoint(genome_1, genome_2) / N) + c3 * \
               Genome.calculate_weight_difference(genome_1, genome_2)

    def __str__(self):
        string = 'nodes: \n'
        nodes = self.nodes.values()
        # nodes.sort()
        for node in nodes:
            string += node.__str__()
            string += '\n'

        string += '\n'

        connections = self.connections.values()
        # connections.sort()
        for conn in connections:
            string += conn.__str__()
        string += '\n'
        return string

    def __eq__(self, other) -> bool:
        if other is None or other.__class__ is not self.__class__:
            return False
        connections = other.connections == self.connections
        nodes = other.nodes == self.nodes
        return connections and nodes

    def __hash__(self):
        return 2 * hash(frozenset(self.nodes.items())) + 3 * hash(frozenset(self.connections.items())) + 7 * hash(self.innvation_generator)
