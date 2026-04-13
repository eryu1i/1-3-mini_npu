def generate_cross(N):
    mid = N // 2
    matrix = []

    for row in range(N):
        cols = []
        for col in range(N):
            if row == mid or col == mid:
                cols.append(1.0)
            else:
                cols.append(0.0)
        matrix.append(cols)

    return matrix


def generate_x(N):
    matrix = []

    for row in range(N):
        cols = []
        for col in range(N):
            if row == col or row + col == N - 1:
                cols.append(1.0)
            else:
                cols.append(0.0)
        matrix.append(cols)

    return matrix