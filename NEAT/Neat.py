from NEAT.ConnectionGene import InnovationGenerator
from NEAT.Genome import Genome
from NEAT.NodeGene import NodeGeneType, NodeGene
from NEAT.ConnectionGene import ConnectionGene
from NEAT.Specie import Specie
from NEAT.NeuralNet import NeuralNet
import numpy as np
from math import inf
from random import Random

innovation_counter = InnovationGenerator()

C1 = 1.0
C2 = 1.0
C3 = 0.3

DT = 0.8

MUTATION_RATE = 0.3
NODE_RATE = 0.1
CONNECTION_RATE = 0.3


def evolution(input_set, output_set, epochs=1000):
    generation = creat_genesis(input_set.shape[1], output_set.shape[1])
    species_map = {}
    score_map = {}
    species = []
    epoch = 0
    while epoch < epochs:
        print('epoch {}'.format(epoch))
        # place genomes into species
        # species_map = {}
        score_map = {}
        # species = []
        species, species_map = classify(generation, species, species_map)
        # remove empty species
        for specie in species:
            if len(specie.members) == 0:
                species.remove(specie)
        # evaluate genomes and assign fitness
        for genome in generation:
            specie = species_map[genome]
            # mayyyyybe this is wrong
            score = evaluate(genome, input_set, output_set)
            print('score {}'.format(score))
            adjusted_score = score / len(specie.members)
            specie.add_adjusted_fitness(adjusted_score)
            specie.set_fitness(genome, adjusted_score)
            score_map[genome] = {'genome': genome, 'fitness': adjusted_score}

        # put best genomes from each species into next generation
        next_gen = []
        for specie in species:
            best = specie.get_best_member()
            next_gen.append(best)

        # breed the rest of the generation
        while len(next_gen) < len(generation):
            specie = select_specie_roulette(species)
            genome_1 = select_genome_roulette(specie)
            genome_2 = select_genome_roulette(specie)
            if evaluate(genome_1, input_set, output_set) < evaluate(genome_2, input_set, output_set):
                child = Genome.crossover(genome_2, genome_1)
            else:
                child = Genome.crossover(genome_1, genome_2)
            if Random().random() < MUTATION_RATE:
                child.mutation(Random())
            if Random().random() < NODE_RATE:
                child.add_node_mutation(Random())
            if Random().random() < CONNECTION_RATE:
                child.add_connection_mutation(Random())

            next_gen.append(child)
        epoch += 1
        generation = next_gen

    return generation


def creat_genesis(inputs, outputs, size=10):
    """
    creates the initial population
    :return: a list of genomes
    """
    nodes = {}
    connections = {}
    nodes_input = {}
    nodes_output = {}
    global innovation_counter

    for i in range(inputs):
        counter = innovation_counter.get_innovation()
        node = NodeGene(NodeGeneType.INPUT, counter, counter)
        nodes_input[counter] = node

    for i in range(outputs):
        counter = innovation_counter.get_innovation()
        node = NodeGene(NodeGeneType.OUTPUT, counter, counter)
        nodes_output[counter] = node

    # connections
    # initially it is a feed forward fully connect no hidden layers network
    rand = Random()
    for input_node in nodes_input.values():
        for output_node in nodes_output.values():
            counter = innovation_counter.get_innovation()
            conn = ConnectionGene(input_node.get_id(), output_node.get_id(), rand.random(), innovation_number=counter)
            connections[counter] = conn

    population = []
    nodes = nodes_input
    nodes.update(nodes_output)
    for i in range(size):
        gene = Genome(connections, nodes, innovation_counter)
        population.append(gene)
    return population


def evaluate(genome, input_set, output_set):
    phenotype = generate_phenotype(genome)
    gene_fitness = get_fitness_mse(phenotype, input_set, output_set) #get_fitness_mse(phenotype, input_set, output_set)
    return gene_fitness


def classify(generation, species, species_map):
    for genome in generation:
        found = False
        for specie in species:
            if Genome.compute_distance(genome, specie.get_representative(), C1, C2, C3) < DT:
                specie.add_member(genome, 0)
                species_map[genome] = specie
                found = True
                break
        if not found:
            new_specie = Specie(genome, 0)
            species_map[genome] = new_specie
            species.append(new_specie)

    return species, species_map


def select_specie_roulette(species):
    total = 0
    for specie in species:
        total += specie.adjusted_fitness
    r = Random().random() * total
    accumulated_weight = 0
    for specie in species:
        accumulated_weight += specie.adjusted_fitness
        if accumulated_weight >= r:
            return specie
    raise ArithmeticError()


def select_genome_roulette(specie):
    total = 0
    for member in specie.members:
        total += member['fitness']
    r = Random().random() * total
    accumulated_weight = 0
    for member in specie.members:
        accumulated_weight += member['fitness']
        if accumulated_weight >= r:
            return member['genome']
    raise ArithmeticError()


def generate_phenotype(gene):

    return NeuralNet(gene)


def get_fitness(phenotype, input_set, output_set):
    """ for testing purposes we try to make topolgies gain 100 neurons"""
    return len(phenotype.predict(input_set))


def get_fitness_mse(phenotype, input_set, output_set):
    """
    calculate MSE for batch
    :param phenotype: neural net
    :param input_set: matrix containing inputs
    :param output_set: matrix containing outputs, rows are considered as different patterns
    :return: a float representing the inverse of MSE
    """
    predictions = phenotype.predict(input_set)
    error = (output_set - predictions) ** 2
    error = np.sum(error) / len(output_set)
    return 1 / error if error != 0 else inf


if __name__ == '__main__':
    input_set = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
    output_set = np.array([[0], [1], [1], [1]])
    generation = evolution(input_set, output_set, 200)
    for gene in generation:
        phenotype = NeuralNet(gene)
        print(phenotype.predict(input_set))
        print(len(gene.connections))
        print('--------')