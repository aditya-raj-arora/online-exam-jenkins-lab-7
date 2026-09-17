"""
Project 4 - Grade Sheet stage (runs only when GENERATE_GRADE_SHEET is ticked)
Evaluates a batch of candidates and prints a grade sheet.
"""
from evaluator import ExamEvaluator, SAMPLE_QUESTIONS

CANDIDATES = {
    "24MIS0101 Ananya":  {"Q1": "B", "Q2": "D", "Q3": ["A", "C"], "Q4": "A", "Q5": ["B", "C", "D"]},
    "24MIS0102 Rahul":   {"Q1": "B", "Q2": "A", "Q3": ["A"], "Q4": "A", "Q5": ["B", "C"]},
    "24MIS0103 Sneha":   {"Q1": "C", "Q2": "D", "Q3": ["A", "B"], "Q4": None, "Q5": ["C"]},
    "24MIS0104 Karthik": {"Q1": "A", "Q2": "B", "Q3": None, "Q4": "C", "Q5": None},
}

ev = ExamEvaluator(SAMPLE_QUESTIONS)
print("GRADE SHEET - Sample Batch")
print(f"{'Candidate':<20}{'Q1':>7}{'Q2':>7}{'Q3':>7}{'Q4':>7}{'Q5':>7}"
      f"{'Total':>8}{'%':>8}{'Grade':>7}{'Result':>8}")
print("-" * 86)
for name, responses in CANDIDATES.items():
    r = ev.evaluate(responses)
    marks = "".join(f"{m:>7.2f}" for m in r["breakdown"].values())
    print(f"{name:<20}{marks}{r['total']:>8}{r['percentage']:>8}{r['grade']:>7}{r['status']:>8}")
print("-" * 86)
