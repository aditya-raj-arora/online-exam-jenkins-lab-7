"""
Project 1 - Parameterized Build Pipeline
Online Examination and Evaluation System

Builds an environment-specific configuration for the exam system.
Usage: python config_builder.py <environment> <exam_code>
"""
import json
import sys
import time
from datetime import datetime

CONFIGS = {
    "dev": {
        "database_host": "localhost:5432",
        "database_name": "exam_dev_db",
        "exam_duration_min": 5,
        "max_concurrent_candidates": 20,
        "negative_marking": False,
        "proctoring_enabled": False,
        "result_publish_mode": "instant",
        "debug_mode": True,
        "log_level": "DEBUG",
    },
    "staging": {
        "database_host": "staging-db.exam.internal:5432",
        "database_name": "exam_staging_db",
        "exam_duration_min": 30,
        "max_concurrent_candidates": 200,
        "negative_marking": True,
        "proctoring_enabled": True,
        "result_publish_mode": "after_review",
        "debug_mode": True,
        "log_level": "INFO",
    },
    "prod": {
        "database_host": "prod-db.exam.internal:5432",
        "database_name": "exam_prod_db",
        "exam_duration_min": 90,
        "max_concurrent_candidates": 5000,
        "negative_marking": True,
        "proctoring_enabled": True,
        "result_publish_mode": "scheduled",
        "debug_mode": False,
        "log_level": "WARNING",
    },
}

REQUIRED_KEYS = [
    "database_host", "database_name", "exam_duration_min",
    "max_concurrent_candidates", "result_publish_mode", "log_level",
]


def banner(text):
    print("=" * 60)
    print(text.center(60))
    print("=" * 60, flush=True)


def print_config(cfg):
    print("\nConfiguration selected:")
    print("-" * 60)
    for key, value in cfg.items():
        print(f"  {key:<28}: {value}")
    print("-" * 60, flush=True)


def validate(env, cfg):
    errors = []
    for key in REQUIRED_KEYS:
        if key not in cfg or cfg[key] in ("", None):
            errors.append(f"Missing required setting: {key}")
    if cfg["exam_duration_min"] <= 0:
        errors.append("Exam duration must be positive")
    if cfg["max_concurrent_candidates"] <= 0:
        errors.append("Max concurrent candidates must be positive")

    # Stricter rules for production
    if env == "prod":
        if cfg["debug_mode"]:
            errors.append("Debug mode must be OFF in production")
        if not cfg["proctoring_enabled"]:
            errors.append("Proctoring must be ON in production")
        if cfg["log_level"] == "DEBUG":
            errors.append("DEBUG logging is not allowed in production")
    return errors


def simulate_build(env):
    steps = [
        "Loading question bank module",
        "Loading candidate authentication module",
        "Loading exam timer and auto-submit module",
        "Loading evaluation engine",
        f"Applying {env} database settings",
        "Packaging application",
    ]
    print("\nBuild steps:")
    for i, step in enumerate(steps, 1):
        time.sleep(0.4)
        print(f"  [{i}/{len(steps)}] {step} ... done", flush=True)


def main():
    env = sys.argv[1].lower() if len(sys.argv) > 1 else "dev"
    exam_code = sys.argv[2] if len(sys.argv) > 2 else "UNSPECIFIED"

    if env not in CONFIGS:
        print(f"ERROR: Unknown environment '{env}'. Choose from {list(CONFIGS)}")
        sys.exit(2)

    banner(f"ONLINE EXAM SYSTEM - {env.upper()} BUILD")
    print(f"Exam code : {exam_code}")
    print(f"Started at: {datetime.now():%Y-%m-%d %H:%M:%S}")

    cfg = CONFIGS[env]
    print_config(cfg)

    print("\nValidating configuration...")
    errors = validate(env, cfg)
    if errors:
        for e in errors:
            print(f"  [FAIL] {e}")
        print("Build aborted due to invalid configuration.")
        sys.exit(1)
    print("  [OK] All configuration checks passed", flush=True)

    simulate_build(env)

    build_info = {
        "environment": env,
        "exam_code": exam_code,
        "built_at": datetime.now().isoformat(timespec="seconds"),
        "config": cfg,
    }
    with open("build_info.json", "w") as f:
        json.dump(build_info, f, indent=2)

    banner(f"BUILD SUCCESSFUL FOR {env.upper()}")
    print("Build details written to build_info.json")


if __name__ == "__main__":
    main()
