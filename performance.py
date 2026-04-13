import time
from mac import mac_2d, mac_1d


def measure_2d(pattern, filter_2d, N, repeat=10):
    total = 0.0

    for _ in range(repeat):
        start = time.time()
        mac_2d(pattern, filter_2d, N)
        end = time.time()
        total += (end - start) * 1000

    return total / repeat


def measure_1d(pattern_flat, filter_flat, N, repeat=10):
    total = 0.0

    for _ in range(repeat):
        start = time.time()
        mac_1d(pattern_flat, filter_flat, N)
        end = time.time()
        total += (end - start) * 1000

    return total / repeat


def print_performance_table(results):
    print(f"{'크기':<5} {'2D 평균(ms)':<15} {'1D 평균(ms)':<15} {'차이(ms)':<10} {'연산 횟수(N²)'}")
    print("-" * 65)

    for N, avg_2d, avg_1d in results:
        diff = avg_2d - avg_1d
        print(f"{f'{N}x{N}':<10} {avg_2d:<15.4f} {avg_1d:<15.4f} {diff:<15.4f} {N * N}")