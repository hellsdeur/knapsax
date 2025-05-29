import numpy as np
from typing import List

from knapsax.optimization import Item, Knapsack


class ACOSolution:
    def __init__(self, path, items: List[Item]):
        self.path = path
        self.items = items
        self.total_weight = sum(items[i].weight for i in path)
        self.total_value = sum(items[i].value for i in path)

    def __repr__(self):
        included_items = [idx for idx, val in enumerate(self.items) if val == 1]
        return (f"Solution(value={self.total_value}, weight={self.total_weight}, items={included_items})")


class ACO:
    def __init__(self, n_ants, decay, pheromone_intensity, n_iterations, n_best, knapsack: Knapsack, alpha=1.0, beta=0.0):
        self.n_ants = n_ants
        self.decay = decay
        self.pheromone_intensity = pheromone_intensity
        self.n_iterations = n_iterations
        self.n_best = n_best
        self.alpha = alpha
        self.beta = beta
        self.knapsack = knapsack
        self.items = sorted(knapsack.items, key=lambda item: item.weight)
        self.nbr_items = len(self.items)
        self.pheromones = np.ones((self.nbr_items,), dtype=np.float32)
        self.heuristics = np.array([item.value / item.weight if item.weight > 0 else 0 for item in self.items], dtype=np.float32)
        self.global_best_values = np.zeros((self.n_iterations,), dtype=np.float32)
        self.global_best_solution = None
        self.history_value = []
        self.history_weight = []

    def reset(self):
        self.history_value = []
        self.history_weight = []

    def run(self):
        self.reset()
        for generation in range(self.n_iterations):
            solutions = []
            fitness = np.zeros((self.n_ants,), dtype=np.uint16)

            for ant in range(self.n_ants):
                path = self.construct_solution()
                solution = ACOSolution(path, self.items)
                solutions.append(solution)
                fitness[ant] = solution.total_value

            generation_max = np.max(fitness)
            index = np.argmax(fitness)

            if generation == 0 or generation_max >= self.global_best_values[generation - 1]:
                self.global_best_values[generation] = generation_max
                self.global_best_solution = solutions[index]
            else:
                self.global_best_values[generation] = self.global_best_values[generation - 1]

            self.history_value.append(self.global_best_solution.total_value)
            self.history_weight.append(self.global_best_solution.total_weight)

            self.update_pheromones(solutions, fitness)

        return self.global_best_values.astype(np.uint16), self.global_best_solution.total_value, self.global_best_solution.total_weight

    def construct_solution(self):
        available = np.ones((self.nbr_items,), dtype=bool)
        ant_path = np.zeros(self.nbr_items, dtype=np.uint8)
        path_node = 0
        sum_weight = 0.0

        while np.any(available):
            probabilities = np.zeros_like(self.pheromones)
            for i in range(self.nbr_items):
                if available[i]:
                    probabilities[i] = (self.pheromones[i] ** self.alpha) * (self.heuristics[i] ** self.beta)

            total = np.sum(probabilities)
            if total == 0:
                break

            probabilities /= total
            item_index = np.random.choice(self.nbr_items, p=probabilities)

            ant_path[path_node] = item_index
            path_node += 1
            sum_weight += self.items[item_index].weight

            available[item_index] = False
            for i in range(self.nbr_items):
                if self.items[i].weight > (self.knapsack.capacity - sum_weight):
                    available[i] = False

        return ant_path[:path_node]

    def update_pheromones(self, solutions, fitness):
        self.pheromones *= self.decay
        added_pheromones = lambda fit: self.pheromone_intensity * float(fit)
        sorted_indices = np.argsort(fitness)
        top_indexes = sorted_indices[-self.n_best:]
        for i in top_indexes:
            self.pheromones[solutions[i].path] += added_pheromones(fitness[i])
