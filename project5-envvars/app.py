"""
Project 5 - Custom Environment Variables
Online Examination and Evaluation System

All exam rules come from environment variables defined once in the
Jenkinsfile's environment block. Change them there and every stage
(and this script) picks up the new values.
"""
import os
import sys

# (name, correct answers, wrong answers, attempts used)
CANDIDATES = [
    ("Ananya",  18, 2, 1),
    ("Rahul",   12, 6, 1),
    ("Sneha",    9, 8, 1),
    ("Karthik",  8, 4, 2),
    ("Priya",   15, 5, 1),
]
TOTAL_QUESTIONS = 20
MARKS_PER_QUESTION = 4


def read_config():
    try:
        return {
            "app_name": os.environ.get("APP_NAME", "UnknownApp"),
            "app_version": os.environ.get("APP_VERSION", "0.0.0"),
            "institution": os.environ.get("INSTITUTION", "Unknown Institution"),
            "exam_duration": int(os.environ.get("EXAM_DURATION", "60")),
            "pass_mark": float(os.environ.get("PASS_MARK", "40")),
            "negative_marking": os.environ.get("NEGATIVE_MARKING", "false").lower() == "true",
            "negative_ratio": float(os.environ.get("NEGATIVE_RATIO", "0.25")),
            "max_attempts": int(os.environ.get("MAX_ATTEMPTS", "1")),
        }
    except ValueError as err:
        print(f"ERROR: invalid environment variable value - {err}")
        sys.exit(1)


def main():
    cfg = read_config()

    print("=" * 62)
    print(f"{cfg['app_name']} v{cfg['app_version']}".center(62))
    print(cfg["institution"].center(62))
    print("=" * 62)

    print("\nCustom variables (defined by us in the Jenkinsfile):")
    for key, value in cfg.items():
        print(f"  {key:<17}: {value}")

    print("\nBuilt-in variables (set automatically by Jenkins):")
    for var in ("BUILD_NUMBER", "JOB_NAME", "WORKSPACE"):
        print(f"  {var:<17}: {os.environ.get(var, 'not running in Jenkins')}")

    max_marks = TOTAL_QUESTIONS * MARKS_PER_QUESTION
    penalty = MARKS_PER_QUESTION * cfg["negative_ratio"] if cfg["negative_marking"] else 0

    print(f"\nExam rules: {TOTAL_QUESTIONS} questions x {MARKS_PER_QUESTION} marks = {max_marks}, "
          f"{cfg['exam_duration']} min,")
    print(f"            pass at {cfg['pass_mark']}%, penalty per wrong answer = {penalty}")
    print(f"\n{'Candidate':<10}{'Correct':>9}{'Wrong':>7}{'Marks':>8}{'%':>8}  Result")
    print("-" * 62)
    passed = 0
    for name, correct, wrong, attempts in CANDIDATES:
        if attempts > cfg["max_attempts"]:
            print(f"{name:<10}{'-':>9}{'-':>7}{'-':>8}{'-':>8}  DISQUALIFIED "
                  f"(attempts {attempts} > {cfg['max_attempts']})")
            continue
        marks = max(correct * MARKS_PER_QUESTION - wrong * penalty, 0)
        pct = marks / max_marks * 100
        result = "PASS" if pct >= cfg["pass_mark"] else "FAIL"
        passed += result == "PASS"
        print(f"{name:<10}{correct:>9}{wrong:>7}{marks:>8.1f}{pct:>8.1f}  {result}")
    print("-" * 62)
    print(f"Passed: {passed}/{len(CANDIDATES)}")


if __name__ == "__main__":
    main()
