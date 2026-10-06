import pandas as pd
from cafe import Cafe
import os
from parameters import N_STEPS, STEP
import plotter


def run_single_simulation(enable_logging=False):
    cafe = Cafe()
    log_data = []

    for step_num in range(N_STEPS):
        cafe.arrive()
        cafe.serve()
        cafe.stats.record_queue(len(cafe.queue))

        if enable_logging:
            hours = int(cafe.current_time)
            minutes = int((cafe.current_time * 60) % 60)
            time_str = f"{hours:02d}:{minutes:02d}"

            if cafe.current_order is not None:
                status = f"Обслуговує (ціна: {cafe.current_order.price} грн)"
            else:
                status = "Вільний"

            log_data.append({
                "Час": time_str,
                "Черга": len(cafe.queue),
                "Стан": status,
                "Залишок (хв)": round(cafe.remaining_time, 1)
            })

        cafe.current_time += STEP / 60.0

    df_log = None
    if enable_logging:
        df_log = pd.DataFrame(log_data)
        df_log.set_index("Час", inplace=True)

    # Повертаємо загальну статистику, таблицю логу та масив довжин черги для графіка
    return cafe.stats.summary(), df_log, cafe.stats.queue_lengths


def main():
    # 1. ЕКСПЕРИМЕНТ: 1 ПРОГОН (для діаграм, гістограм і логу)
    summary_1, df_log, queue_lengths = run_single_simulation(enable_logging=True)

    # Зберігаємо лог одного дня у файл CSV (можна відкрити в Excel)
    df_log.to_csv(os.path.join("results","single_run_log.csv"), encoding="utf-8-sig")

    # Викликаємо функції для збереження графіків (1 прогон)
    plotter.plot_single_run(queue_lengths)

    # 2. ЕКСПЕРИМЕНТ: 100 ПРОГОНІВ
    num_runs = 100
    all_results = []

    for _ in range(num_runs):
        res, _, _ = run_single_simulation(enable_logging=False)
        all_results.append(res)

    # Створюємо DataFrame з результатами 100 прогонів
    df_results = pd.DataFrame(all_results)
    df_results.index = [f"День {i + 1}" for i in range(num_runs)]

    # Зберігаємо повну таблицю 100 днів у файл CSV
    df_results.to_csv(os.path.join("results","100_runs_results_table.csv"), encoding="utf-8-sig")

    # Розраховуємо середні показники та зберігаємо їх у текстовий файл
    avg_results = df_results.mean()
    with open(os.path.join("results", "100_runs_averages.txt"), "w", encoding="utf-8") as file:
        file.write("--- Середні результати за 100 прогонів ---\n")
        for key, value in avg_results.items():
            file.write(f"{key}: {value:.2f}\n")

    # Викликаємо функції для збереження графіків (100 прогонів)
    plotter.plot_100_runs(df_results)


if __name__ == "__main__":
    main()