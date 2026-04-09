import time
from mac import mac_2d


def measure(pattern, filter_2d, N, repeat=10):
    total = 0.0

    for _ in range(repeat):
        start = time.time()
        mac_2d(pattern, filter_2d, N)
        end = time.time()
        total += (end - start) * 1000

    return total / repeat


def print_performance_table(results):
    print(f"{'크기':<10} {'평균 시간(ms)':<15} {'연산 횟수(N²)'}")
    print("-" * 40)

    for N, avg_ms in results:
        print(f"{f'{N}x{N}':<10} {avg_ms:<15.4f} {N * N}")