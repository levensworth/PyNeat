#PyNeat
###Python implementation for NEAT algorithm

##Technologies used:
- Python 3.7
- numpy 1.17.2

##Code structure:
- Genome: contains the structure which represents a Genome, the same has a map of connection genes and Node genes.
- NodeGene: a gene structure representing a graph node with has an innovation number.
- ConnectionGene: a gene structure representing a connection between two nodes, it has an innovation number and a weight.
- Neat: it contains the evaluation method.

*Observations*:
- The evolutionary algorithm uses roulette to select species for the crossover
- A percentage (g) of the next generation will always be the best fitted current generation's genes.
  this is  to preserve good structures.
- Add connection mutation will create a random connection between nodes.
- Add Node mutation will create a node and disable a connection but create two new connections.
- The innovation number generator is global and the same for connection and node Genes.
- The Distance equation to measure distance between Genomes needs three Constants:
        <br>->C1
        <br>->C2
        <br>->C3

## TODO:
- this project needs to be optimized, packaged, distributed and used in further projects.
