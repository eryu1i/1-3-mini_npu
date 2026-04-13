from pattern_generator import generate_cross, generate_x
import json

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
        "size_5_0": {"input": generate_cross(5), "expected": "+"},
        "size_5_1": {"input": generate_x(5), "expected": "x"},
        "size_13_0": {"input": generate_cross(13), "expected": "+"},
        "size_13_1": {"input": generate_x(13), "expected": "x"},
        "size_25_0": {"input": generate_cross(25), "expected": "+"},
        "size_25_1": {"input": generate_x(25), "expected": "x"}
    }
}

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

print("data.json 생성 완료")