def input_matrix(N, name):
    while True:
        print(f"{name}을(를) 입력하세요. ({N}x{N}, 한 줄에 {N}개씩) : ")
        matrix = []

        for i in range(N):
            row = input()
            values = row.strip().split()

        # 열 수 검증
        if len(values) != N:
            print(f"입력 형식 오류: 각 줄에 {N}개의 숫자를 공백으로 구분해 입력하세요.")
            break

        # 숫자 파싱 검증
        try:
            row_values = [float(v) for v in values]
        except ValueError:
            print("입력 형식 오류: 숫자만 입력하세요.")
            break

        matrix.append(row_values)

    if len(matrix) == N:
        print(f"f{name} 저장 완료 : ")
        for row in matrix:
            print(" ".join(str(int(v))) for v in row)
        return matrix