"""
Project 3 - Parallel Stages (Branch 1)
Validates the question bank of the Online Examination System.
"""
import sys
import time
from datetime import datetime

QUESTIONS = [
    {"id": "Q1", "section": "Agile", "difficulty": "easy", "marks": 2,
     "text": "Which ceremony reviews the sprint increment?",
     "options": {"A": "Planning", "B": "Review", "C": "Retro", "D": "Stand-up"}, "answer": "B"},
    {"id": "Q2", "section": "Agile", "difficulty": "medium", "marks": 2,
     "text": "Who owns the product backlog?",
     "options": {"A": "Product Owner", "B": "Scrum Master", "C": "Dev Team", "D": "Tester"}, "answer": "A"},
    {"id": "Q3", "section": "DevOps", "difficulty": "easy", "marks": 2,
     "text": "What does CI stand for?",
     "options": {"A": "Code Inspection", "B": "Continuous Improvement",
                 "C": "Continuous Integration", "D": "Central Integration"}, "answer": "C"},
    {"id": "Q4", "section": "DevOps", "difficulty": "hard", "marks": 4,
     "text": "Which tool is primarily used for containerisation?",
     "options": {"A": "Maven", "B": "Docker", "C": "Selenium", "D": "Nagios"}, "answer": "B"},
    {"id": "Q5", "section": "Jenkins", "difficulty": "medium", "marks": 2,
     "text": "Which directive makes a stage conditional?",
     "options": {"A": "when", "B": "if", "C": "input", "D": "post"}, "answer": "A"},
    {"id": "Q6", "section": "Jenkins", "difficulty": "hard", "marks": 4,
     "text": "Which step saves build output files?",
     "options": {"A": "stash", "B": "echo", "C": "bat", "D": "archiveArtifacts"}, "answer": "D"},
]

ALLOWED_DIFFICULTY = {"easy", "medium", "hard"}
REQUIRED_SECTIONS = {"Agile", "DevOps", "Jenkins"}


def log(msg):
    print(f"[QUESTION-BANK {datetime.now():%H:%M:%S}] {msg}", flush=True)


def check_unique_ids():
    ids = [q["id"] for q in QUESTIONS]
    return len(ids) == len(set(ids)), "Question IDs are unique"


def check_options():
    bad = [q["id"] for q in QUESTIONS if len(q["options"]) != 4]
    return not bad, f"Every question has 4 options {bad or ''}"


def check_answers():
    bad = [q["id"] for q in QUESTIONS if q["answer"] not in q["options"]]
    return not bad, f"Every answer key matches an option {bad or ''}"


def check_marks_and_text():
    bad = [q["id"] for q in QUESTIONS if q["marks"] <= 0 or not q["text"].strip()]
    return not bad, f"Marks are positive and question text is present {bad or ''}"


def check_difficulty():
    bad = [q["id"] for q in QUESTIONS if q["difficulty"] not in ALLOWED_DIFFICULTY]
    return not bad, f"Difficulty levels are valid {bad or ''}"


def check_section_coverage():
    missing = REQUIRED_SECTIONS - {q["section"] for q in QUESTIONS}
    return not missing, f"All syllabus sections are covered {sorted(missing) or ''}"


def main():
    log(f"Running question bank checks on {len(QUESTIONS)} questions...")
    checks = [check_unique_ids, check_options, check_answers,
              check_marks_and_text, check_difficulty, check_section_coverage]
    failures = 0
    for check in checks:
        time.sleep(0.5)  # simulate work
        ok, message = check()
        log(f"{'PASS' if ok else 'FAIL'} - {message}")
        failures += not ok

    log(f"Total marks in bank: {sum(q['marks'] for q in QUESTIONS)}")
    if failures:
        log(f"{failures} check(s) failed.")
        sys.exit(1)
    log("Question bank checks passed.")


if __name__ == "__main__":
    main()
