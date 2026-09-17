# Online Examination and Evaluation System - Jenkins CI/CD Pipelines

ISWE406P - Agile Development Process and DevOps, Assessment VII

Five Jenkins pipeline projects. Each one lives in its own folder with its own Jenkinsfile.
The code uses only the Python standard library (no pip installs needed).

| Folder | Jenkins concept | What the code does |
|---|---|---|
| project1-parameterized | `parameters` (choice + string) | Builds and validates dev/staging/prod configs; prod has stricter rules |
| project2-artifacts | `archiveArtifacts` | Evaluates 6 candidates with negative marking; creates TXT, CSV and JSON result reports |
| project3-parallel | `parallel` | Three ~3 s checks (question bank, evaluation engine, concurrent exam sessions) |
| project4-conditional | `when` | Evaluation engine (single/multi-select, partial marks); optional test suite and grade sheet |
| project5-envvars | `environment` | Exam rules (pass mark, negative marking, attempts) read from custom env variables |

## Jenkins job setup (for each project)
1. New Item -> Pipeline.
2. Pipeline -> Definition: **Pipeline script from SCM** -> Git -> this repo URL, branch `*/main`.
3. Script Path: `<folder>/Jenkinsfile`, e.g. `project3-parallel/Jenkinsfile`.
4. Replace `<your-username>` in every Jenkinsfile with your GitHub username.

## Demo changes to show during evaluation
- **P1:** build with `staging`, then `prod`; the config, validation and build_info.json change.
- **P2:** edit an answer in `exam_data.json`, push, rebuild; older builds keep their old reports.
- **P3:** total stage time is ~3 s instead of ~9 s; console lines from all three checks interleave.
- **P4:** toggle `RUN_EXTRA_CHECK` / `GENERATE_GRADE_SHEET`; unticked stages show as skipped.
- **P5:** change `PASS_MARK` to `'60'` or `MAX_ATTEMPTS` to `'2'`; results change without touching app.py.

## Run locally (optional)
```
cd project2-artifacts
python app.py
```
