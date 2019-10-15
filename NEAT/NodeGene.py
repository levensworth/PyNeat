from enum import Enum


class NodeGeneType(Enum):
    INPUT = 0
    OUTPUT = 1
    HIDDEN = 2


class NodeGene(object):
    def __init__(self, neuron_type, neuron_id, innovation_number):
        self.neuron_type = neuron_type
        self.neuron_id = neuron_id
        self.innovation_number = innovation_number

    def get_type(self):
        return self.neuron_type

    def get_id(self):
        return self.neuron_id

    def get_innovation_number(self):
        return self.innovation_number

    def __copy__(self):
        return NodeGene(self.neuron_type, self.neuron_id, self.innovation_number)

    def __str__(self):
        return '|  Node: {}    |' \
               '|  Inno: {}    |' \
               '|  Type: {}    |'.format(self.neuron_id, self.innovation_number, self.neuron_type)

    def __eq__(self, other):
        if other is None or other.__class__ != self.__class__:
            return False

        return self.neuron_id == other.neuron_id

    def __hash__(self):
        return 17 * hash(self.neuron_id) + 19 * hash(self.neuron_type)
