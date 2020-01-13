class Specie(object):
    def __init__(self, representative, fitness):
        self.representative = representative
        self.members = []
        self.add_member(representative, fitness)
        self.adjusted_fitness = 0

    def get_representative(self):
        return self.representative

    def add_member(self, member, fitness):
        self.members.append({'genome': member, 'fitness': fitness})

    def set_fitness(self, member, fitness):
        for i in range(len(self.members)):
            m = self.members[i]
            if m['genome'] == member:
                self.members[i] = {'genome': member, 'fitness': fitness}

    def add_adjusted_fitness(self, fitness):
        self.adjusted_fitness += fitness

    def get_best_member(self):
        best = None
        for member in self.members:
            if best is None or member['fitness'] > best['fitness']:
                best = member
        if best is None:
            raise ArithmeticError()
        return best['genome']

    def reset(self, rand):
        self.representative = self.members[rand.randint(0, len(self.members))]['genome']
        self.members = []
        self.adjusted_fitness = 0

