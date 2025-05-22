import numpy as np

from knapsax.optimization import Solution


class ACOSolution(Solution):
    def __init__(self, knapsack, pheromone_vector, alpha=1, beta=1):
        super().__init__(knapsack)
        self.pheromone_vector = pheromone_vector
        self.alpha = alpha
        self.beta = beta

    def generate_solution(self):
        available_items = set(range(self.knapsack.n_items))

        while available_items:
            probabilities = self._compute_probabilities(available_items)

            if probabilities.sum() == 0 or len(available_items) == 0:
                break

            item_index = np.random.choice(list(available_items), p=probabilities)

            self.add_item(item_index)
            available_items.remove(item_index)

    def _compute_probabilities(self, available_items):
        pheromone = np.array([self.pheromone_vector[i] for i in available_items])
        heuristic = np.array([self.knapsack.items[i].value / self.knapsack.items[i].weight for i in available_items])
        scores = (pheromone ** self.alpha) * (heuristic ** self.beta)
        total = scores.sum()
        if total == 0:
            return np.ones_like(scores) / len(scores)
        return scores / total


class ACO:
    def __init__(self, knapsack, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        self.knapsack = knapsack
        self.n_items = knapsack.n_items
        self.pheromone = np.ones(self.n_items) / self.n_items
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

        self.history_value = []
        self.history_weight = []

    def run(self):
        best_solution = None

        for _ in range(self.n_iterations):
            all_solutions = self.gen_all_solutions()
            self.spread_pheromone(all_solutions)

            local_best = max(all_solutions, key=lambda s: s.total_value)
            if best_solution is None or local_best.total_value > best_solution.total_value:
                best_solution = local_best
            self.history_value.append(best_solution.total_value)
            self.history_weight.append(best_solution.total_weight)

            self.pheromone *= self.decay

        return best_solution.items, best_solution.total_value, best_solution.total_weight

    def spread_pheromone(self, all_solutions):
        sorted_solutions = sorted(all_solutions, key=lambda s: s.total_value, reverse=True)
        for solution in sorted_solutions[:self.n_best]:
            for idx in solution.items:
                self.pheromone[idx] += solution.total_value / sum(item.value for item in self.knapsack.items)

    def gen_all_solutions(self):
        return [self.gen_solution() for _ in range(self.n_ants)]

    def gen_solution(self):
        solution = ACOSolution(self.knapsack, self.pheromone, self.alpha, self.beta)
        solution.generate_solution()
        return solution
