from mac import mac_2d, flatten
from input_handler import input_matrix
from json_loader import validate_and_load
from pattern_generator import generate_cross
from performance import measure_2d, measure_1d, print_performance_table
from reporter import print_case_result, print_summary


def judge(score_cross, score_x):
    if abs(score_cross - score_x) < 1e-9:
        return "UNDECIDED"
    elif score_cross > score_x:
        return "Cross"
    else:
        return "X"


def mode_1():
    # 3 x 3 필터 A, B, 패턴 입력
    filter_a = input_matrix(3, "필터 A")
    filter_b = input_matrix(3, "필터 B")
    pattern  = input_matrix(3, "패턴")

    # MAC 연산
    score_a = mac_2d(pattern, filter_a, 3)
    score_b = mac_2d(pattern, filter_b, 3)

    # 판정 출력
    print(f"\nA 점수: {score_a:.1f} | B 점수: {score_b:.1f}")
    if abs(score_a - score_b) < 1e-9:
        print("판정: 판정 불가")
    elif score_a > score_b:
        print("판정: A")
    else:
        print("판정: B")

    # 성능 분석
    cross_pattern = generate_cross(3)
    avg_2d = measure_2d(cross_pattern, filter_a, 3)
    avg_1d = measure_1d(flatten(cross_pattern), flatten(filter_a), 3)
    print_performance_table([(3, avg_2d, avg_1d)])


def mode_2():
    # 필터, 패턴 로드
    filters, patterns = validate_and_load("data.json")

    results = []

    for pattern_key, pattern_data in patterns.items():
        # 스키마 오류 케이스
        if pattern_data["error"] is not None:
            print(f"[{pattern_key}] FAIL | 사유: {pattern_data['error']}")
            results.append({
                "key": pattern_key,
                "judgment": "FAIL",
                "expected": "-",
                "pass_fail": "FAIL",
                "reason":    pattern_data["error"]
            })
            continue

        N             = pattern_data["N"]
        pattern_input = pattern_data["input"]
        expected      = pattern_data["expected"]
        filter_key    = f"size_{N}"

        # MAC 연산
        score_cross = mac_2d(pattern_input, filters[filter_key]["Cross"], N)
        score_x     = mac_2d(pattern_input, filters[filter_key]["X"],     N)

        # 판정
        judgment  = judge(score_cross, score_x)
        pass_fail = "PASS" if judgment == expected else "FAIL"
        if pass_fail == "PASS":
            reason = ""
        elif judgment == "UNDECIDED":
            reason = "동점 처리 규칙에 따라 FAIL"
        else:
            reason = "판정 불일치"

        # 케이스별 출력
        print_case_result(pattern_key, score_cross, score_x, judgment, expected, pass_fail)

        results.append({
            "key":       pattern_key,
            "judgment":  judgment,
            "expected":  expected,
            "pass_fail": pass_fail,
            "reason":    reason
        })

    # 성능 분석
    perf_results = []
    for N in [5, 13, 25]:
        filter_key = f"size_{N}"
        if filter_key not in filters:
            continue
        # 임의의 필터 Cross로 측정
        pattern = generate_cross(N)
        cross_filter = filters[filter_key]["Cross"]
        avg_2d = measure_2d(pattern, cross_filter, N)
        avg_1d = measure_1d(flatten(pattern), flatten(cross_filter), N)
        perf_results.append((N, avg_2d, avg_1d))

    print_performance_table(perf_results)

    # 결과 요약
    print_summary(results)


def main():
    print("모드를 선택하세요")
    print("1: 사용자 입력 (3x3)")
    print("2: data.json 분석")
    mode = input("선택: ").strip()

    if mode == "1":
        mode_1()
    elif mode == "2":
        mode_2()
    else:
        print("잘못된 입력입니다. 1 또는 2를 입력하세요.")


if __name__ == "__main__":
    main()