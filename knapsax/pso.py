from knapsax.populational import Populational
import numpy as np


class PSO(Populational):
    def __init__(self, population_size: int, knapsack, weights, values, capacity):
        super().__init__(population_size, knapsack)

        self.weights = weights
        self.values = values
        self.capacity = capacity
        self.num_items = len(weights)

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


class PSO_knapsack:
    def __init__(self, weights, values, capacity, num_particles=100, max_evals=20000,
                 inertia=1.0, c1=0.5, c2=0.5, min_velocity=4, max_velocity=4):

        self.weights = weights
        self.values = values
        self.capacity = capacity
        num_itens = len(weights)

        self.num_particles = num_particles
        self.max_evals = max_evals
        self.inertia = inertia
        self.c1 = c1
        self.c2 = c2
        self.min_velocity = min_velocity
        self.max_velocity = max_velocity

        self.history = []

    def run(self):
        swarm = [PSO(self.weights, self.values, self.capacity) for _ in range(self.num_particles)]
        global_best = swarm[0].best_position.copy()
        global_best_fitness = swarm[0].best_fitness

        evals = self.num_particles
        self.history.append(global_best_fitness)

        while evals < self.max_evals:
            for particle in swarm:
                particle.update_velocity(global_best, self.inertia, self.c1, self.c2, self.min_velocity,
                                         self.max_velocity)
                particle.update_position()
                fitness = particle.evaluate()
                evals += 1

                if fitness > particle.best_fitness:
                    particle.best_fitness = fitness
                    particle.best_position = particle.position.copy()

                if fitness > global_best_fitness:
                    global_best_fitness = fitness
                    global_best = particle.position.copy()

                if evals >= self.max_evals:
                    break
            self.history.append(global_best_fitness)
        return global_best, global_best_fitness, self.history