"""
Лабораторная работа № 7. Вариант 5.
Задача А: числа Фибоначчи (наивная рекурсия, мемоизация, итерация).
Задача Б: рюкзак 0/1 при N = 22, W = 120.
Доп. задание Г5 — восстановление решения двумя способами
и сравнение расхода памяти.
"""
import random
import sys
import time
from itertools import combinations


# ==================== Задача А: числа Фибоначчи ====================

def fib_naive(n, counter):
    """Наивная рекурсия: Θ(φⁿ)."""
    counter[0] += 1
    if n < 2:
        return n
    return fib_naive(n - 1, counter) + fib_naive(n - 2, counter)


def fib_memo(n, cache, counter):
    """Нисходящее ДП (мемоизация): Θ(n)."""
    counter[0] += 1
    if n < 2:
        return n
    if n in cache:
        return cache[n]
    cache[n] = fib_memo(n - 1, cache, counter) + fib_memo(n - 2, cache, counter)
    return cache[n]


def fib_iter(n):
    """Восходящее ДП: Θ(n) времени, O(1) памяти."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# ==================== Задача Б: рюкзак 0/1 ====================

def knapsack_dp_table(weights, values, capacity):
    """Задача о рюкзаке 0/1. Возвращает таблицу D и состав (обратным проходом)."""
    n = len(weights)
    D = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wi, vi = weights[i - 1], values[i - 1]
        for w in range(capacity + 1):
            D[i][w] = D[i - 1][w]
            if wi <= w and D[i - 1][w - wi] + vi > D[i][w]:
                D[i][w] = D[i - 1][w - wi] + vi

    # восстановление обратным проходом
    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if D[i][w] != D[i - 1][w]:
            chosen.append(i - 1)
            w -= weights[i - 1]
    return D[n][capacity], sorted(chosen), D


def knapsack_dp_take(weights, values, capacity):
    """Задача о рюкзаке 0/1 с таблицей take."""
    n = len(weights)
    D = [[0] * (capacity + 1) for _ in range(n + 1)]
    take = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wi, vi = weights[i - 1], values[i - 1]
        for w in range(capacity + 1):
            D[i][w] = D[i - 1][w]
            if wi <= w and D[i - 1][w - wi] + vi > D[i][w]:
                D[i][w] = D[i - 1][w - wi] + vi
                take[i][w] = 1

    # восстановление по take
    chosen, w = [], capacity
    for i in range(n, 0, -1):
        if take[i][w] == 1:
            chosen.append(i - 1)
            w -= weights[i - 1]
    return D[n][capacity], sorted(chosen), take


def knapsack_brute(weights, values, capacity):
    """Полный перебор: 2^N подмножеств. Только для проверки при малых N."""
    n = len(weights)
    best, best_set = 0, ()
    for size in range(n + 1):
        for subset in combinations(range(n), size):
            w = sum(weights[i] for i in subset)
            if w <= capacity:
                v = sum(values[i] for i in subset)
                if v > best:
                    best, best_set = v, subset
    return best, list(best_set)


# ==================== Эксперимент ====================

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # ---------- Задача А: числа Фибоначчи ----------
    N_LIST = [10, 15, 20, 25, 30, 33]
    print("--- Задача А: числа Фибоначчи ---")
    print(f"{'n':>4} {'наивная, с':>12} {'вызовов':>12} {'мемо, с':>10}"
          f" {'вызовов':>9} {'итер., с':>10} {'F(n)':>14}")

    naive_calls, memo_calls = [], []
    for n in N_LIST:
        c = [0]
        t0 = time.perf_counter(); r1 = fib_naive(n, c); t_naive = time.perf_counter() - t0
        c_naive = c[0]

        c = [0]
        t0 = time.perf_counter(); r2 = fib_memo(n, {}, c); t_memo = time.perf_counter() - t0
        c_memo = c[0]

        t0 = time.perf_counter(); r3 = fib_iter(n); t_iter = time.perf_counter() - t0
        assert r1 == r2 == r3

        naive_calls.append(c_naive)
        memo_calls.append(c_memo)
        print(f"{n:>4} {t_naive:>12.6f} {c_naive:>12} {t_memo:>10.6f}"
              f" {c_memo:>9} {t_iter:>10.6f} {r1:>14}")

    # ---------- Задача Б: рюкзак 0/1 ----------
    N, W = 22, 120
    rng = random.Random(7)
    weights = [rng.randint(5, 40) for _ in range(N)]
    values = [rng.randint(10, 100) for _ in range(N)]
    print(f"\n--- Задача Б: рюкзак 0/1, N = {N}, W = {W} ---")

    t0 = time.perf_counter()
    v1, items1, D = knapsack_dp_table(weights, values, W)
    t1 = time.perf_counter() - t0

    t0 = time.perf_counter()
    v2, items2, take = knapsack_dp_take(weights, values, W)
    t2 = time.perf_counter() - t0

    t0 = time.perf_counter()
    v_bf, items_bf = knapsack_brute(weights, values, W)
    t_bf = time.perf_counter() - t0

    print(f"  ДП (обратный проход):  ценность {v1}, время {t1:.4f} с")
    print(f"  ДП (таблица take):     ценность {v2}, время {t2:.4f} с")
    print(f"  Полный перебор:        ценность {v_bf}, время {t_bf:.4f} с")
    print(f"  Ускорение ДП:          ≈ {t_bf / t1:.0f}× (обратный проход)")
    assert v1 == v2 == v_bf, "Результаты не совпадают"
    assert items1 == items2

    print(f"  Состав рюкзака: предметы {items1}")
    print(f"  Суммарный вес: {sum(weights[i] for i in items1)} из {W}")

    # ---------- Г5: сравнение расхода памяти ----------
    print("\n--- Г5: расход памяти ---")
    size_D = sys.getsizeof(D) + sum(sys.getsizeof(row) for row in D) \
             + sum(sys.getsizeof(x) for row in D for x in row)
    size_take = sys.getsizeof(take) + sum(sys.getsizeof(row) for row in take) \
                + sum(sys.getsizeof(x) for row in take for x in row)
    print(f"  Таблица D:            ~{size_D:>8} байт")
    print(f"  Таблица take:         ~{size_take:>8} байт")
    print(f"  D + take (способ 2):  ~{size_D + size_take:>8} байт")
    print(f"  Отношение:            {(size_D + size_take) / size_D:.2f}×")

    # ---------- Графики ----------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].semilogy(N_LIST, naive_calls, "o-", label="Наивная")
    axes[0].semilogy(N_LIST, memo_calls, "s-", label="Мемоизация")
    axes[0].set_xlabel("n")
    axes[0].set_ylabel("Число вызовов (лог. шкала)")
    axes[0].set_title("Задача А: число вызовов")
    axes[0].grid(True, which="both", alpha=0.3)
    axes[0].legend()

    W_LIST = [30, 60, 90, 120, 150, 180, 210, 240]
    dp_times = []
    for w_cap in W_LIST:
        t0 = time.perf_counter()
        knapsack_dp_table(weights, values, w_cap)
        dp_times.append(time.perf_counter() - t0)
    axes[1].plot(W_LIST, dp_times, "o-", color="darkorange")
    axes[1].set_xlabel("Вместимость W")
    axes[1].set_ylabel("Время ДП, с")
    axes[1].set_title("Задача Б: время ДП от W при N = 22")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("lr7_plot.png", dpi=150)
    plt.show()