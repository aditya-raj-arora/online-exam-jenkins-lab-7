"""
Project 4 - Extra Check stage (runs only when RUN_EXTRA_CHECK is ticked)
A small test suite for the evaluation engine.
"""
import sys
from evaluator import ExamEvaluator, SAMPLE_QUESTIONS

ev = ExamEvaluator(SAMPLE_QUESTIONS, negative_ratio=0.25, pass_percentage=40)


def test_correct_single_choice():
    assert ev.score_question("Q1", "B") == 4.0


def test_wrong_single_choice_is_negative():
    assert ev.score_question("Q1", "C") == -1.0


def test_unattempted_scores_zero():
    assert ev.score_question("Q2", None) == 0.0


def test_multi_select_full_marks():
    assert ev.score_question("Q3", ["A", "C"]) == 4.0


def test_multi_select_partial_marks():
    assert ev.score_question("Q5", ["B", "C"]) == 2.67


def test_multi_select_wrong_option_is_negative():
    assert ev.score_question("Q3", ["A", "B"]) == -1.0


def test_full_paper_topper():
    r = ev.evaluate({"Q1": "B", "Q2": "D", "Q3": ["A", "C"], "Q4": "A", "Q5": ["B", "C", "D"]})
    assert r["total"] == 20.0 and r["grade"] == "S" and r["status"] == "PASS"


def test_blank_paper_fails():
    r = ev.evaluate({})
    assert r["total"] == 0.0 and r["grade"] == "F" and r["status"] == "FAIL"


def test_total_never_negative():
    r = ev.evaluate({"Q1": "A", "Q2": "A", "Q4": "B"})
    assert r["total"] == 0.0


def test_grade_boundaries():
    assert ExamEvaluator.grade(90) == "S"
    assert ExamEvaluator.grade(79.99) == "B"
    assert ExamEvaluator.grade(40) == "E"
    assert ExamEvaluator.grade(39.9) == "F"


TESTS = [obj for name, obj in list(globals().items()) if name.startswith("test_")]


def main():
    print(f"Running {len(TESTS)} evaluator tests")
    print("-" * 55)
    failed = 0
    for test in TESTS:
        try:
            test()
            print(f"  PASS  {test.__name__}")
        except AssertionError:
            failed += 1
            print(f"  FAIL  {test.__name__}")
    print("-" * 55)
    print(f"Result: {len(TESTS) - failed} passed, {failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
