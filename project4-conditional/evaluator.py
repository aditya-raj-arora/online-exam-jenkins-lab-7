"""
Project 4 - Conditional Stage Execution
Evaluation engine of the Online Examination System.

Supports:
  - single-choice questions (full marks, or negative marks if wrong)
  - multiple-select questions (partial marks; any wrong option = negative)
  - percentage, grade and pass/fail calculation
"""

GRADE_BANDS = [(90, "S"), (80, "A"), (70, "B"), (60, "C"), (50, "D"), (40, "E")]


class ExamEvaluator:
    def __init__(self, questions, negative_ratio=0.25, pass_percentage=40):
        self.questions = questions
        self.negative_ratio = negative_ratio
        self.pass_percentage = pass_percentage
        self.max_marks = sum(q["marks"] for q in questions.values())

    def score_question(self, qid, response):
        q = self.questions[qid]
        if response is None or response == []:
            return 0.0
        penalty = -q["marks"] * self.negative_ratio

        if q["type"] == "single":
            return float(q["marks"]) if response == q["answer"] else penalty

        # multiple-select question
        chosen, correct = set(response), set(q["answer"])
        if chosen - correct:
            return penalty
        return round(q["marks"] * len(chosen) / len(correct), 2)

    @staticmethod
    def grade(percentage):
        for cutoff, g in GRADE_BANDS:
            if percentage >= cutoff:
                return g
        return "F"

    def evaluate(self, responses):
        breakdown = {qid: self.score_question(qid, responses.get(qid))
                     for qid in self.questions}
        total = max(round(sum(breakdown.values()), 2), 0.0)
        percentage = round(total / self.max_marks * 100, 2)
        return {
            "total": total,
            "max_marks": self.max_marks,
            "percentage": percentage,
            "grade": self.grade(percentage),
            "status": "PASS" if percentage >= self.pass_percentage else "FAIL",
            "breakdown": breakdown,
        }


SAMPLE_QUESTIONS = {
    "Q1": {"type": "single", "answer": "B", "marks": 4},
    "Q2": {"type": "single", "answer": "D", "marks": 4},
    "Q3": {"type": "multi", "answer": ["A", "C"], "marks": 4},
    "Q4": {"type": "single", "answer": "A", "marks": 4},
    "Q5": {"type": "multi", "answer": ["B", "C", "D"], "marks": 4},
}


if __name__ == "__main__":
    ev = ExamEvaluator(SAMPLE_QUESTIONS)
    demo = {"Q1": "B", "Q2": "A", "Q3": ["A"], "Q4": "A", "Q5": ["B", "C", "D"]}
    result = ev.evaluate(demo)
    print("Smoke test - evaluating one sample candidate:")
    for qid, marks in result["breakdown"].items():
        print(f"  {qid}: {marks:+.2f}")
    print(f"  Total: {result['total']}/{result['max_marks']} "
          f"({result['percentage']}%) Grade {result['grade']} - {result['status']}")
