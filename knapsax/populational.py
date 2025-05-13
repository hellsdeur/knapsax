from knapsax.optimization import Knapsack, Solution, Problem


class Populational:
    def __init__(self, population_size: int, knapsack: Knapsack):
        self.population_size = population_size
        self.knapsack = knapsack
        self.population = []
        self.fitness_scores = []
        self.best_individual = None
        self.best_fitness = float('-inf')

    def initialize_population(self):

        self.population = [Solution(self.knapsack) for _ in range(self.population_size)]

    