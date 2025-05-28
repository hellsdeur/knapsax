import numpy as np


class Particula:
    def __init__(self, knapsack):
        self.knapsack = knapsack
        self.weights = [item.weight for item in knapsack.items]
        self.values = [item.value for item in knapsack.items]
        self.capacity = knapsack.capacity
        self.num_items = len(self.weights)
        
        self.position = self.generate_feasible_position()
        self.velocity = np.random.uniform(-1, 1, size=self.num_items)

        self.best_position = self.position.copy()
        self.best_fitness = self.evaluate()

    def generate_feasible_position(self):
        position = np.zeros(self.num_items, dtype=int)
        total_weight = 0
        indices = np.random.permutation(self.num_items)
        for i in indices:
            if total_weight + self.weights[i] <= self.capacity:
                position[i] = 1
                total_weight += self.weights[i]
        return position

    def evaluate(self):
        total_weight = np.sum(self.position * self.weights)
        if total_weight > self.capacity:
            return 0
        return np.sum(self.position * self.values)

    def update_velocity(self, global_best, inertia, c1, c2, min_v, max_v):
        r1 = np.random.rand(self.num_items)
        r2 = np.random.rand(self.num_items)
        cognitive = c1 * r1 * (self.best_position - self.position)
        social = c2 * r2 * (global_best - self.position)
        self.velocity = inertia * self.velocity + cognitive + social
        self.velocity = np.clip(self.velocity, -min_v, max_v)

    def update_position(self):
        prob = 1 / (1 + np.exp(-self.velocity))
        self.position = np.where(np.random.rand(self.num_items) < prob, 1, 0)


class PSO:
    def __init__(self, knapsack, num_particles=100, max_evals=20000,
                 inertia=0.7, c1=0.5, c2=0.3, min_velocity=4, max_velocity=4, n_iterations=100):
        
        self.knapsack = knapsack
        self.n_iterations = n_iterations

        self.weights = [item.weight for item in knapsack.items]
        self.values = [item.value for item in knapsack.items]
        self.capacity = knapsack.capacity
        self.num_items = len(self.weights)

        self.num_particles = num_particles
        self.max_evals = max_evals
        self.inertia = inertia
        self.c1 = c1
        self.c2 = c2
        self.min_velocity = min_velocity
        self.max_velocity = max_velocity

        self.history_value = []
        self.history_weight = []
    
    def run(self):
        swarm = [Particula(self.knapsack) for _ in range(self.num_particles)]
        global_best = swarm[0].best_position.copy()
        global_best_fitness = swarm[0].best_fitness

        self.history_value = [global_best_fitness]
        self.history_weight = [np.sum(global_best * self.weights)]

        for _ in range(self.n_iterations):
            for particle in swarm:
                particle.update_velocity(global_best, self.inertia, self.c1, self.c2,
                                        self.min_velocity, self.max_velocity)
                particle.update_position()
                fitness = particle.evaluate()

                if fitness > particle.best_fitness:
                    particle.best_fitness = fitness
                    particle.best_position = particle.position.copy()

                if fitness > global_best_fitness:
                    global_best_fitness = fitness
                    global_best = particle.position.copy()

            self.history_value.append(global_best_fitness)
            self.history_weight.append(np.sum(global_best * self.weights))

        selected_items = [self.knapsack.items[i] for i in range(self.num_items) if global_best[i] == 1]
        total_value = sum(item.value for item in selected_items)
        total_weight = sum(item.weight for item in selected_items)

        return selected_items, total_value, total_weight


    #     # >>> AQUI: converte a solução final no mesmo formato do ACO <<<
    #     return self._format_solution(global_best)

    # def _format_solution(self, solution):
    #     selected_items = []
    #     for i in range(self.num_items):
    #         if solution[i] == 1:
    #             selected_items.append(self.knapsack.items[i])

    #     total_value = sum(item.value for item in selected_items)
    #     total_weight = sum(item.weight for item in selected_items)

    #     return selected_items, total_value, total_weight