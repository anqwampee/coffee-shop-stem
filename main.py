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
            total_min = 450 + step_num * STEP
            time_str = f"{total_min // 60:02d}:{total_min % 60:02d}"

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

        cafe.current_time = 7.5 + (step_num + 1) * STEP / 60

    while cafe.current_order is not None or cafe.queue:
        cafe.serve()

    df_log = None
    if enable_logging:
        df_log = pd.DataFrame(log_data)
        df_log.set_index("Час", inplace=True)

    # Перевірка балансу прийшли = обслужено + втрачено
    clients_rest = len(cafe.queue) + (1 if cafe.current_order is not None else 0)
    c = cafe.stats.clients

    summary = cafe.stats.summary()
    summary.update({
        "came": c["came"],
        "served": c["served"],
        "lost": c["lost"],
        "rest": clients_rest,
        "balance_ok": c["came"] == c["served"] + c["lost"] + clients_rest,
    })

    return summary, df_log, cafe.stats.queue_lengths


def main():
    summary_1, df_log, queue_lengths = run_single_simulation(enable_logging=True)

    df_log.to_csv(os.path.join("results","single_run_log.csv"), encoding="utf-8-sig")

    plotter.plot_single_run(queue_lengths)

    num_runs = 100
    all_results = []

    for _ in range(num_runs):
        res, _, _ = run_single_simulation(enable_logging=False)
        all_results.append(res)

    df_results = pd.DataFrame(all_results)
    df_results.index = [f"День {i + 1}" for i in range(num_runs)]

    df_results.to_csv(os.path.join("results","100_runs_results_table.csv"), encoding="utf-8-sig")

    avg_results = df_results.mean()
    with open(os.path.join("results", "100_runs_averages.txt"), "w", encoding="utf-8") as file:
        file.write("--- Середні результати за 100 прогонів ---\n")
        for key, value in avg_results.items():
            file.write(f"{key}: {value:.2f}\n")

    plotter.plot_100_runs(df_results)

    print("Прийшло за добу (середнє):", df_results["came"].mean())
    print("Баланс виконано в усіх прогонах:", df_results["balance_ok"].all())
    print("Обслужено: середнє / мін / макс:",
          df_results["served"].mean(), df_results["served"].min(), df_results["served"].max())


if __name__ == "__main__":
    main()