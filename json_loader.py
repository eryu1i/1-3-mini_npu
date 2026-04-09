import json

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"오류: {path} 파일을 찾을 수 없습니다.")
        exit(1)


def normalize_label(raw):
    raw = raw.strip().lower()
    if raw in ("+", "cross"):
        return "Cross"
    elif raw == "x":
        return "X"
    else:
        raise ValueError(f"알 수 없는 라벨: {raw}")


def validate_and_load(path):
    data = load_json(path)

    # 필터 로드 + 라벨 정규화
    filters = {}
    for size_key, filter_dict in data["filters"].items():
        filters[size_key] = {}
        for label, matrix in filter_dict.items():
            normalized = normalize_label(label)
            filters[size_key][normalized] = matrix

    # 패턴 로드 + 스키마 검증
    patterns = {}
    for pattern_key, pattern_data in data["patterns"].items():
        # 키에서 N 추출 (size_5_0 -> 5)
        parts = pattern_key.split("_")
        N = int(parts[1])
        filter_key = f"size_{N}"

        entry = {
            "input":    None,
            "expected": None,
            "N":        N,
            "error":    None
        }

        # 필수 키 존재 여부 검증
        if "input" not in pattern_data or "expected" not in pattern_data:
            entry["error"] = "input 또는 expected 키 누락"
            patterns[pattern_key] = entry
            continue

        # 필터 존재 여부 검증
        if filter_key not in filters:
            entry["error"] = f"{filter_key} 필터 없음"
            patterns[pattern_key] = entry
            continue

        # 크기 검증
        pattern_input = pattern_data["input"]
        pattern_rows = len(pattern_input)
        pattern_cols = len(pattern_input[0])
        filter_rows = len(filters[filter_key]["Cross"])
        filter_cols = len(filters[filter_key]["Cross"][0])

        if pattern_rows != N or pattern_cols != N:
            entry["error"] = f"패턴 크기 불일치: {pattern_rows}x{pattern_cols} (기대: {N}x{N})"
            patterns[pattern_key] = entry
            continue

        if filter_rows != N or filters_cols != N:
            entry["error"] = f"필터 크기 불일치: {filter_rows}x{filter_cols} (기대: {N}x{N})"
            patterns[pattern_key] = entry
            continue

        # 검증 통과
        entry["input"]    = pattern_input
        entry["expected"] = normalize_label(pattern_data["expected"])
        patterns[pattern_key] = entry

    return filters, patterns