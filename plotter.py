# plotter.py
import matplotlib.pyplot as plt
import pandas as pd
import os

# Створюємо папку results, якщо вона ще не існує
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def plot_single_run(queue_lengths):
    """
    Будує діаграму та гістограму для одного прогону моделі.
    Зберігає їх у папку results.
    """
    # 1. Діаграма (лінійний графік): Зміна довжини черги в часі
    plt.figure(figsize=(10, 5))
    plt.plot(queue_lengths, label="Довжина черги", color="blue", marker='o', markersize=3)
    plt.title("Діаграма зміни довжини черги протягом дня (1 прогон)")
    plt.xlabel("Крок моделювання (період)")
    plt.ylabel("Кількість клієнтів у черзі")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "single_run_diagram.png"))
    plt.close()

    # 2. Гістограма: Розподіл значень довжини черги
    plt.figure(figsize=(10, 5))
    max_q = max(queue_lengths) if queue_lengths else 0
    plt.hist(queue_lengths, bins=range(max_q + 2), align='left', color="orange", edgecolor='black')
    plt.title("Гістограма довжини черги (1 прогон)")
    plt.xlabel("Кількість клієнтів у черзі")
    plt.ylabel("Частота (кількість кроків)")
    plt.xticks(range(max_q + 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "single_run_histogram.png"))
    plt.close()


def plot_100_runs(df_results):
    """
    Будує діаграму середніх показників та гістограму для 100 прогонів.
    Зберігає їх у папку results.
    """
    # 1. Діаграма (стовпчаста): Середні фінансові показники
    avg_metrics = df_results[['revenue', 'cost', 'profit']].mean()

    plt.figure(figsize=(8, 6))
    avg_metrics.plot(kind='bar', color=['green', 'red', 'blue'], edgecolor='black')
    plt.title("Діаграма середніх фінансових показників (100 прогонів)")
    plt.ylabel("Грошові одиниці (грн)")
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "100_runs_averages_diagram.png"))
    plt.close()

    # 2. Гістограма: Розподіл прибутку (profit) за 100 днів
    plt.figure(figsize=(10, 5))
    plt.hist(df_results['profit'], bins=15, color="purple", edgecolor='black')
    plt.title("Гістограма розподілу денного прибутку (за 100 прогонів)")
    plt.xlabel("Прибуток (грн)")
    plt.ylabel("Частота (кількість днів)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "100_runs_profit_histogram.png"))
    plt.close()