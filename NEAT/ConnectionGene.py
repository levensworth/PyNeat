class ConnectionGene(object):
    """
    A representation of network connection.
    contains:   - input node (by reference to the genome)
                - output node (by reference to the genome)
                - weight of the connection (double value)
                - the innovation number (for evolution purposes)
                - enable flag (for innovation purposes)
    """
    def __init__(self, in_node, out_node, weight, enable=True, innovation_number=0):
        self.in_node = in_node
        self.out_node = out_node
        self.enable = enable
        self.weight = weight
        self.innovation_number = innovation_number

    def get_in_node(self):
        return self.in_node

    def get_out_node(self):
        return self.out_node

    def get_weight(self):
        return self.weight

    def is_enable(self):
        return self.enable

    def get_innovation_number(self):
        return self.innovation_number

    def set_weight(self, weight):
        self.weight = weight

    def disable(self):
        self.enable = False

    def __copy__(self):
        return ConnectionGene(self.in_node, self.out_node, self.weight, self.enable,
                              self.innovation_number)

    def __eq__(self, o: object) -> bool:
        if o is None or o.__class__ is not self.__class__:
            return False

        return o.get_in_node() is self.get_in_node() and o.get_out_node() is self.get_out_node() \
               and o.get_innovation_number() is self.get_innovation_number() and o.is_enable() is self.is_enable()

    def __hash__(self):
        return 17 * hash(self.innovation_number) + 19 * hash(self.in_node) + 23 * hash(self.out_node)

    def __str__(self):
        return '--------------\n' \
               '| In: {}      |\n' \
               '| Out: {}     |\n' \
               '| Weight: {}  |\n' \
               '| Enable: {}  |\n' \
               '| Innov: {}   |\n' \
               '--------------\n'.format(self.in_node, self.out_node, self.weight, self.enable, self.innovation_number)


class InnovationGenerator(object):
    def __init__(self):
        self.counter = 0

    def get_innovation(self):
        self.counter += 1
        return self.counter
