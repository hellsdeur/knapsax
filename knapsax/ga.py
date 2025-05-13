from knapsax.populational import Populational

class GeneticAlgorithm(Populational):
    def __init__(self, population_size, knapsack):
        super().__init__(population_size, knapsack)
