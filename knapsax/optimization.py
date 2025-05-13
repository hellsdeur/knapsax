from typing import List, Protocol
import random


class Item:
    def __init__(self, value: int, weight: int):
        self.value: int = value
        self.weight: int = weight

    def __repr__(self):
        return f"Item(value={self.value}, weight={self.weight})"


class Knapsack:
    def __init__(self, instance_file: str):
        self.instance_file: str = instance_file
        self.n_items: int = 0
        self.capacity: int = 0
        self.items: List[Item] = []
        self.load_instance()

    def load_instance(self):
        with open(self.instance_file, 'r') as file:
            lines = file.readlines()

            self.n_items = int(lines[0].strip())

            self.capacity = int(lines[1].strip())

            for line in lines[2:]:
                value, weight = map(int, line.split())
                self.items.append(Item(value, weight))

    def __repr__(self):
        return f"Knapsack(file={self.instance_file}, n_items={self.n_items}, capacity={self.capacity})"


class Solution:
    def __init__(self, knapsack: Knapsack):
        self.knapsack: Knapsack = knapsack
        self.x: List[Item] = []
        self.n_items: int = 0
        self.total_value: int = 0
        self.total_weight: int = 0
        self.generate_solution()

    def generate_solution(self):

        shuffled_items = random.shuffle(self.knapsack.items, len(self.knapsack.items))

        while self.total_weight <= self.knapsack.capacity and len(shuffled_items) > 0:
            item = shuffled_items.pop(0)
            if self.total_weight + item.weight <= self.knapsack.capacity:
                self.x.append(item)
                self.total_value += item.value
                self.total_weight += item.weight
                self.n_items += 1
                shuffled_items = random.shuffle(self.knapsack.items, len(shuffled_items))
            else:
                break

    def __repr__(self):
        return f"Solution(value={self.total_value}, weight={self.total_weight}, n_items={self.n_items})"


class Problem(Protocol):
    def __call__(self, new_cost: float, best_cost: float) -> bool:
        pass
    

class Minimize(Problem):
    def __call__(self, new_cost: float, best_cost: float) -> bool:
        return new_cost < best_cost


class Maximize(Problem):
    def __call__(self, new_cost: float, best_cost: float) -> bool:
        return new_cost > best_cost
    

class ObjectiveFunction:
    def __call__(self, solution: Solution) -> float:
        return solution.total_value
