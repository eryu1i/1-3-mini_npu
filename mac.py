def mac_2d(pattern, filter_2d, N):
    score = 0.0

    for row in range(N):
        for col in range(N):
            score += pattern[row][col] * filter_2d[row][col]

    return score