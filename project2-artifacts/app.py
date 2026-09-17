"""
Project 2 - Archive Build Artifacts Pipeline
Online Examination and Evaluation System

Evaluates all candidate responses in exam_data.json and generates three
report files in reports/, which Jenkins archives as build artifacts:
  - result_report.txt  (human-readable result sheet)
  - results.csv        (spreadsheet-friendly marks list)
  - summary.json       (machine-readable statistics)
"""
import csv
import json
import os
import statistics
from datetime import datetime

DATA_FILE = "exam_data.json"
OUT_DIR = "reports"

GRADE_BANDS = [(90, "S"), (80, "A"), (70, "B"), (60, "C"), (50, "D"), (40, "E")]


def get_grade(percentage):
    for cutoff, grade in GRADE_BANDS:
        if percentage >= cutoff:
            return grade
    return "F"


def evaluate_candidate(questions, answers, negative_mark):
    correct = wrong = unattempted = 0
    score = 0.0
    section_scores = {}

    for q in questions:
        section = q["section"]
        section_scores.setdefault(section, 0.0)
        response = answers.get(q["id"])

        if response is None:
            unattempted += 1
        elif response == q["answer"]:
            correct += 1
            score += q["marks"]
            section_scores[section] += q["marks"]
        else:
            wrong += 1
            score -= negative_mark
            section_scores[section] -= negative_mark

    return {
        "correct": correct,
        "wrong": wrong,
        "unattempted": unattempted,
        "score": round(max(score, 0), 2),
        "sections": {k: round(v, 2) for k, v in section_scores.items()},
    }


def main():
    with open(DATA_FILE) as f:
        data = json.load(f)

    exam = data["exam"]
    questions = data["questions"]
    max_marks = sum(q["marks"] for q in questions)
    sections = sorted({q["section"] for q in questions})

    print(f"Evaluating '{exam['title']}' ({exam['code']})")
    print(f"Questions: {len(questions)} | Max marks: {max_marks} | "
          f"Negative marking: -{exam['negative_mark']} per wrong answer\n")

    results = []
    for reg_no, entry in data["responses"].items():
        r = evaluate_candidate(questions, entry["answers"], exam["negative_mark"])
        r["reg_no"] = reg_no
        r["name"] = entry["name"]
        r["percentage"] = round(r["score"] / max_marks * 100, 2)
        r["grade"] = get_grade(r["percentage"])
        r["status"] = "PASS" if r["percentage"] >= exam["pass_percentage"] else "FAIL"
        results.append(r)
        print(f"  Evaluated {reg_no} ({entry['name']}): {r['score']}/{max_marks}")

    # Rank candidates (ties share a rank)
    results.sort(key=lambda x: x["score"], reverse=True)
    prev_score, rank = None, 0
    for i, r in enumerate(results, 1):
        if r["score"] != prev_score:
            rank, prev_score = i, r["score"]
        r["rank"] = rank

    scores = [r["score"] for r in results]
    passed = sum(1 for r in results if r["status"] == "PASS")
    stats = {
        "candidates": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "pass_rate": round(passed / len(results) * 100, 2),
        "highest": max(scores),
        "lowest": min(scores),
        "average": round(statistics.mean(scores), 2),
        "median": round(statistics.median(scores), 2),
        "topper": results[0]["name"],
    }

    os.makedirs(OUT_DIR, exist_ok=True)
    generated = f"{datetime.now():%Y-%m-%d %H:%M:%S}"

    # 1. Text report
    with open(os.path.join(OUT_DIR, "result_report.txt"), "w") as f:
        f.write("ONLINE EXAMINATION AND EVALUATION SYSTEM\n")
        f.write("=" * 90 + "\n")
        f.write(f"Exam      : {exam['title']}\n")
        f.write(f"Exam Code : {exam['code']}\n")
        f.write(f"Max Marks : {max_marks}   Pass Mark: {exam['pass_percentage']}%   "
                f"Negative: -{exam['negative_mark']}\n")
        f.write(f"Generated : {generated}\n")
        f.write("=" * 90 + "\n\n")

        header = f"{'Rank':<5}{'Reg No':<11}{'Name':<9}{'C':>3}{'W':>3}{'U':>3}"
        header += "".join(f"{s:>9}" for s in sections)
        header += f"{'Score':>7}{'%':>8}{'Grade':>7}{'Result':>8}"
        f.write(header + "\n")
        f.write("-" * len(header) + "\n")
        for r in results:
            line = (f"{r['rank']:<5}{r['reg_no']:<11}{r['name']:<9}"
                    f"{r['correct']:>3}{r['wrong']:>3}{r['unattempted']:>3}")
            line += "".join(f"{r['sections'][s]:>9}" for s in sections)
            line += f"{r['score']:>7}{r['percentage']:>8}{r['grade']:>7}{r['status']:>8}"
            f.write(line + "\n")
        f.write("-" * len(header) + "\n")
        f.write("C = Correct, W = Wrong, U = Unattempted\n\n")

        f.write("CLASS STATISTICS\n")
        for key, value in stats.items():
            f.write(f"  {key.replace('_', ' ').title():<12}: {value}\n")

    # 2. CSV
    with open(os.path.join(OUT_DIR, "results.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "reg_no", "name", "correct", "wrong", "unattempted",
                         *sections, "score", "percentage", "grade", "status"])
        for r in results:
            writer.writerow([r["rank"], r["reg_no"], r["name"], r["correct"], r["wrong"],
                             r["unattempted"], *[r["sections"][s] for s in sections],
                             r["score"], r["percentage"], r["grade"], r["status"]])

    # 3. JSON summary
    with open(os.path.join(OUT_DIR, "summary.json"), "w") as f:
        json.dump({"exam": exam, "max_marks": max_marks,
                   "generated": generated, "statistics": stats}, f, indent=2)

    print("\nClass statistics:")
    for key, value in stats.items():
        print(f"  {key:<12}: {value}")
    print(f"\nReports generated in '{OUT_DIR}/': result_report.txt, results.csv, summary.json")


if __name__ == "__main__":
    main()
