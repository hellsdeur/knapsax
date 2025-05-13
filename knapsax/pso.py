from knapsax.populational import Populational


class PSO(Populational):
    def __init__(self, population_size: int, knapsack):
        super().__init__(population_size, knapsack)
        