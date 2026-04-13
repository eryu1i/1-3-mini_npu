def mac_2d(pattern, filter_2d, N):
    score = 0.0

    for row in range(N):
        for col in range(N):
            score += pattern[row][col] * filter_2d[row][col]

    return score


def mac_1d(pattern_flat, filter_flat, N):
    score = 0.0

    for i in range(N * N):
        score += pattern_flat[i] * filter_flat[i]

    return score


def flatten(pattern_2d):
    flat = []
    for row in pattern_2d:
        for val in row:
            flat.append(val)
    return flat