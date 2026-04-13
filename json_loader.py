import json


def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"오류: {path} 파일을 찾을 수 없습니다.")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"오류: {path} 파일 형식이 잘못됐습니다. ({e})")
        exit(1)


def normalize_label(raw):
    raw = raw.strip().lower()
    if raw in ("+", "cross"):
        return "Cross"
    elif raw == "x":
        return "X"
    else:
        raise ValueError


def validate_and_load(path):
    data = load_json(path)

    # filters / patterns 키 존재 여부 검증
    if "filters" not in data:
        print("오류: JSON에 'filters' 키가 없습니다.")
        exit(1)
    if "patterns" not in data:
        print("오류: JSON에 'patterns' 키가 없습니다.")
        exit(1)

    # 필터 로드 + 라벨 정규화
    filters = {}
    for size_key, filter_dict in data["filters"].items():
        filters[size_key] = {}
        for label, matrix in filter_dict.items():
            try:
                normalized = normalize_label(label)
            except ValueError:
                print(f"오류: {size_key} 필터 라벨 오류: {label}")
                exit(1)
            filters[size_key][normalized] = [[float(v) for v in row] for row in matrix]

    # 패턴 로드 + 스키마 검증
    patterns = {}
    for pattern_key, pattern_data in data["patterns"].items():
        parts = pattern_key.split("_")

        entry = {
            "input":    None,
            "expected": None,
            "N":        None,
            "error":    None
            }

        try:
            N = int(parts[1])
        except (ValueError, IndexError):
            entry["error"] = f"패턴 키 형식 오류: {pattern_key}"
            patterns[pattern_key] = entry
            continue

        entry["N"] = N
        filter_key = f"size_{N}"

        # input / expected 키 존재 여부 검증
        if "input" not in pattern_data or "expected" not in pattern_data:
            entry["error"] = "input 또는 expected 키 누락"
            patterns[pattern_key] = entry
            continue

        # 필터 존재 여부 검증
        if filter_key not in filters:
            entry["error"] = f"{filter_key} 필터 없음"
            patterns[pattern_key] = entry
            continue

        # 크기 검증 - 패턴
        pattern_input = pattern_data["input"]

        if len(pattern_input) != N:
            entry["error"] = f"패턴 행 수 불일치: {len(pattern_input)} (기대: {N})"
            patterns[pattern_key] = entry
            continue

        pattern_error = None
        for i, row in enumerate(pattern_input):
            if len(row) != N:
                pattern_error = f"패턴 {i}번째 행 열 수 불일치: {len(row)} (기대: {N})"
                break

        if pattern_error:
            entry["error"] = pattern_error
            patterns[pattern_key] = entry
            continue

        # 크기 검증 - 필터
        filter_error = None
        
        for label in ["Cross", "X"]:
            f = filters[filter_key][label]

            if len(f) != N:
                filter_error = f"필터 {label} 행 수 불일치: {len(f)} (기대: {N})"
                break

            for i, row in enumerate(f):
                if len(row) != N:
                    filter_error = f"필터 {label} {i}번째 행 열 수 불일치: {len(row)} (기대: {N})"
                    break

        if filter_error:
            entry["error"] = filter_error
            patterns[pattern_key] = entry
            continue

        # 검증 통과
        entry["input"] = [[float(v) for v in row] for row in pattern_data["input"]]
        try:
            entry["expected"] = normalize_label(pattern_data["expected"])
        except ValueError:
            entry["error"] = f"알 수 없는 expected 라벨: {pattern_data['expected']}"
            patterns[pattern_key] = entry
            continue
        patterns[pattern_key] = entry

    return filters, patterns