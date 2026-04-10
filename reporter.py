def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(int(v)) for v in row))


def print_case_result(key, score_cross, score_x, judgment, expected, pass_fail):
    print(f"[{key}] Cross: {score_cross:.1f} | X: {score_x:.1f} | 판정: {judgment} | expected: {expected} | {pass_fail}")


def print_summary(results):
    total = len(results)
    passed = sum(1 for r in results if r["pass_fail"] == "PASS")
    failed = total - passed

    print(f"\n전체: {total} | 통과 {passed} | 실패: {failed}")

    # 실패 케이스 목록 출력
    if failed > 0:
        print("\n[실패 케이스]")
        for r in results:
            if r["pass_fail"] == "FAIL":
                print(f" [{r['key']}] 판정: {r['judgment']} | expected: {r['expected']} | 사유: {r['reason']}")