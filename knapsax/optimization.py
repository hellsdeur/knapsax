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
    def __init__(self, knapsack):
        self.knapsack = knapsack
        self.items = []
        self.total_weight = 0
        self.total_value = 0

    def add_item(self, item_index):
        item = self.knapsack.items[item_index]
        if self.total_weight + item.weight <= self.knapsack.capacity:
            self.items.append(item_index)
            self.total_weight += item.weight
            self.total_value += item.value
            return True
        return False

    def __repr__(self):
        return (f"Solution(value={self.total_value}, weight={self.total_weight}, items={self.items})")


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
