"""
Project 3 - Parallel Stages (Branch 2)
Verifies the scoring logic of the evaluation engine.
"""
import sys
import time
from datetime import datetime

NEGATIVE_MARK = 0.5
KEY = ["A", "B", "C", "D"]
MARKS = [2, 2, 2, 4]

TEST_CASES = [
    ("All answers correct",         ["A", "B", "C", "D"],     10.0),
    ("All answers wrong",           ["B", "C", "D", "A"],      0.0),
    ("All unattempted",             [None, None, None, None],  0.0),
    ("Mixed with negative marking", ["A", "B", "D", None],     3.5),
    ("Only high-mark question",     [None, None, None, "D"],   4.0),
    ("Score never goes negative",   ["B", None, None, None],   0.0),
]


def score(answer_key, responses, marks):
    total = 0.0
    for key, resp, m in zip(answer_key, responses, marks):
        if resp is None:
            continue
        total += m if resp == key else -NEGATIVE_MARK
    return max(total, 0.0)


def log(msg):
    print(f"[EVALUATION    {datetime.now():%H:%M:%S}] {msg}", flush=True)


def main():
    log(f"Running {len(TEST_CASES)} evaluation test cases...")
    failures = 0
    for name, responses, expected in TEST_CASES:
        time.sleep(0.5)  # simulate work
        actual = score(KEY, responses, MARKS)
        ok = actual == expected
        failures += not ok
        log(f"{'PASS' if ok else 'FAIL'} - {name}: expected {expected}, got {actual}")

    if failures:
        log(f"{failures} test case(s) failed.")
        sys.exit(1)
    log("Evaluation engine checks passed.")


if __name__ == "__main__":
    main()
