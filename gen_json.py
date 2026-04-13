from pattern_generator import generate_cross, generate_x
import json

# pattern_generator.py 이용해 data.json 생성

data = {
    "filters": {
        "size_5": {
            "cross": generate_cross(5),
            "x": generate_x(5)
        },
        "size_13": {
            "cross": generate_cross(13),
            "x": generate_x(13)
        },
        "size_25": {
            "cross": generate_cross(25),
            "x": generate_x(25)
        }
    },
    "patterns": {
        "size_5_0": {"input": generate_cross(5), "expected": "+"},   # PASS
        "size_5_1": {"input": generate_x(5), "expected": "x"},       # PASS
        "size_5_2": {"input": generate_cross(5), "expected": "x"},   # FAIL - 판정 불일치
        "size_5_3": {"input": [[0]*5 for _ in range(5)], "expected": "+"}, # FAIL - UNDECIDED
        "size_5_4": {"input": generate_cross(4), "expected": "+"},   # FAIL - 크기 불일치
        "size_13_0": {"input": generate_cross(13), "expected": "+"},
        "size_13_1": {"input": generate_x(13), "expected": "x"},
        "size_25_0": {"input": generate_cross(25), "expected": "+"},
        "size_25_1": {"input": generate_x(25), "expected": "x"}
    }
}

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

print("data.json 생성 완료")