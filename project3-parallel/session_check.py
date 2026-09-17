"""
Project 3 - Parallel Stages (Branch 3)
Simulates several candidates taking the exam at the same time and
verifies that every session is started, auto-saved and submitted.
"""
import sys
import threading
import time
from datetime import datetime

CANDIDATES = ["24MIS0101", "24MIS0102", "24MIS0103", "24MIS0104", "24MIS0105"]
EXAM_DURATION_SEC = 2.0   # compressed exam duration for the demo

lock = threading.Lock()
submitted = {}


def log(msg):
    with lock:
        print(f"[SESSION       {datetime.now():%H:%M:%S}] {msg}", flush=True)


def run_session(reg_no, time_needed):
    log(f"{reg_no} logged in and started the exam")
    time_spent = min(time_needed, EXAM_DURATION_SEC)
    time.sleep(time_spent / 2)
    log(f"{reg_no} progress auto-saved")
    time.sleep(time_spent / 2)

    # Timer forces submission if the candidate needed more time than allowed
    mode = "auto-submitted (time up)" if time_needed > EXAM_DURATION_SEC else "submitted"
    with lock:
        submitted[reg_no] = mode
    log(f"{reg_no} {mode}")


def main():
    log(f"Simulating {len(CANDIDATES)} concurrent exam sessions...")
    start = time.time()
    threads = []
    for i, reg_no in enumerate(CANDIDATES):
        time_needed = 1.2 + i * 0.3   # last two candidates run out of time
        t = threading.Thread(target=run_session, args=(reg_no, time_needed))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    time.sleep(0.8)  # simulate final consistency check
    missing = [c for c in CANDIDATES if c not in submitted]
    auto = sum(1 for m in submitted.values() if m.startswith("auto"))
    log(f"Sessions completed: {len(submitted)}/{len(CANDIDATES)} "
        f"({auto} auto-submitted) in {time.time() - start:.1f}s")

    if missing:
        log(f"FAIL - sessions not submitted: {missing}")
        sys.exit(1)
    log("Exam session checks passed.")


if __name__ == "__main__":
    main()
