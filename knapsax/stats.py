import time
from tqdm import tqdm
import tracemalloc

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Stats:
    def __init__(self, n_runs: int, algorithm_instance: object):
        self.n_runs = n_runs
        self.algorithm_instance = algorithm_instance
        self.data = {
            "iteration": [],
            "best_solution": [],
            "best_value": [],
            "best_weight": [],
            "history_value": [],
            "history_weight": [],
            "execution_time": [],
            "memory_peak": [],
            "memory_peak_mb": [],
        }

    def run(self):

        for i in tqdm(range(self.n_runs), desc=f"Running {self.algorithm_instance.__class__}", unit="run"):
            start_time = time.time()
            tracemalloc.start()
            best_solution, best_value, best_weight = self.algorithm_instance.run()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            end_time = time.time()

            self.data["iteration"].append(i)
            self.data["best_solution"].append(best_solution)
            self.data["best_value"].append(best_value)
            self.data["best_weight"].append(best_weight)
            self.data["history_value"].append(self.algorithm_instance.history_value)
            self.data["history_weight"].append(self.algorithm_instance.history_weight)
            self.data["execution_time"].append(end_time - start_time)
            self.data["memory_peak"].append(peak)
            self.data["memory_peak_mb"].append(peak / 10**6)

    def frame(self):
        return pd.DataFrame(self.data)
    
    def plot_convergence(self, title: str, savefig: str = None):
        df = self.frame()

        value_by_run = np.array(df["history_value"].tolist())
        value_by_iteration = value_by_run.T

        means_by_iteration = np.mean(value_by_iteration, axis=1)
        std_by_iteration = np.std(value_by_iteration, axis=1)
        max_value = np.nanmax(value_by_iteration)

        fig, ax = plt.subplots(figsize=(10, 6))

        sns.lineplot(
            x=np.arange(len(means_by_iteration)),
            y=means_by_iteration,
            ax=ax,
            label="Média do valor",
            color="royalblue",
            linewidth=2.5
        )

        ax.fill_between(
            np.arange(len(means_by_iteration)),
            means_by_iteration - std_by_iteration,
            means_by_iteration + std_by_iteration,
            color="royalblue",
            alpha=0.2,
            label="Desvio padrão do valor"
        )

        ax.axhline(
            y=max_value,
            linestyle="--",
            color="forestgreen",
            linewidth=2,
            label=f"Valor máximo = {max_value}"
        )

        ax.set_title(title, fontsize=20)
        ax.set_xlabel("Iteração", fontsize=16)
        ax.set_ylabel("Valor", fontsize=16)
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.grid(True, which='both', linestyle='--', linewidth=0.7, alpha=0.7)
        ax.legend(fontsize=12, frameon=True)
        plt.tight_layout()

        if savefig:
            plt.savefig(savefig, dpi=600)
        
        return fig, ax
    