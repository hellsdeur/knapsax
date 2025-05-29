import numpy as np


class ACOSolution:
    def __init__(self, knapsack, pheromone_vector, alpha=1, beta=1):
        self.knapsack = knapsack
        self.pheromone_vector = pheromone_vector
        self.alpha = alpha
        self.beta = beta
        self.items = np.zeros(knapsack.n_items, dtype=int)
        self.total_weight = 0
        self.total_value = 0

    def generate_solution(self):
        for index in range(self.knapsack.n_items):
            if np.random.rand() < 0.5:
                self.items[index] = 1

        self._update_value_and_weight()

    def _update_value_and_weight(self):
        self.total_weight = 0
        self.total_value = 0
        for idx, included in enumerate(self.items):
            if included:
                item = self.knapsack.items[idx]
                self.total_weight += item.weight
                self.total_value += item.value

    def evaluate(self):
        return self.total_weight <= self.knapsack.capacity

    def __repr__(self):
        included_items = [idx for idx, val in enumerate(self.items) if val == 1]
        return (f"Solution(value={self.total_value}, weight={self.total_weight}, items={included_items})")


class ACO:
    def __init__(self, knapsack, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        self.knapsack = knapsack
        self.n_items = knapsack.n_items
        self.pheromone_vector = np.ones(self.n_items) / self.n_items
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

        self.history_value = []
        self.history_weight = []

    def reset(self):
        self.pheromone = np.ones(self.n_items) / self.n_items
        self.history_value = []
        self.history_weight = []

    def run(self):
        self.reset()
        best_solution = None

        for _ in range(self.n_iterations):
            all_solutions = self.generate_all_solutions()
            self.spread_pheromone(all_solutions)

            for solution in all_solutions:
                if solution.evaluate():
                    if best_solution is None or solution.total_value > best_solution.total_value:
                        best_solution = solution

            self.history_value.append(best_solution.total_value if best_solution else 0)
            self.history_weight.append(best_solution.total_weight if best_solution else 0)

            self.pheromone_vector *= self.decay

        if best_solution:
            return best_solution.items, best_solution.total_value, best_solution.total_weight
        else:
            return np.zeros(self.n_items, dtype=int), 0, 0

    def spread_pheromone(self, all_solutions):
        sorted_solutions = sorted([s for s in all_solutions if s.evaluate()], key=lambda s: s.total_value, reverse=True)
        for solution in sorted_solutions[:self.n_best]:
            for item_index, included in enumerate(solution.items):
                if included:
                    self.pheromone_vector[item_index] += solution.total_value / sum(item.value for item in self.knapsack.items)

    def generate_all_solutions(self):
        return [self.generate_single_solution() for _ in range(self.n_ants)]

    def generate_single_solution(self):
        solution = ACOSolution(self.knapsack, self.pheromone_vector, self.alpha, self.beta)
        solution.generate_solution()
        return solution
    