# MSc DevOps Dissertation

**Title:** Greening the Pipeline: An Empirical Comparison of CI/CD Refinement Strategies and Their Carbon Impact Across Open-Source Projects

**Student:** Umer Karachiwala · L00196895 · ATU Donegal, Ireland
**GitHub:** https://github.com/Umer-2612/msc-devops-dissertation

---

## What This Is

This repository contains all written and practical work for the dissertation. Writing and experimental work are kept separate so the structure stays clean as more projects are added.

```
msc-devops-dissertation/
├── dissertation/        ← all writing (chapters, bibliography, appendices)
├── experiments/         ← one folder per project experiment
│   └── project-01-httpie-cli/   ← first project (HTTPie CLI, Python)
├── literature/          ← paper summaries and newly found papers
├── notes/               ← supervisor meetings, weekly log, professor Q&A
└── README.md            ← this file
```

---

## Research Questions

**RQ1:** How much carbon does each strategy (caching, consolidation, path filtering) save compared to an unrefined baseline?

**RQ2:** Is the saving consistent across projects of different languages and sizes, or does it vary?

**RQ3:** Which strategy saves the most carbon per hour of implementation effort?

---

## Current Status (August 2026)

| Area | Progress |
|---|---|
| Literature review | 9 papers reviewed + 3 new 2026 papers found; expanded per-paper depth and gap analysis (Chapter 2) |
| Chapter 1: Introduction | Expanded: problem statement, objectives, contributions preview |
| Chapter 2: Literature Review | Sections 2.1–2.7 written |
| Chapter 3: Methodology | Trimmed to research rationale and design; implementation detail moved to Chapter 4 |
| Chapter 4: Design | New chapter: pipeline architecture, instrumentation pipeline, worked example, diagrams |
| First project (HTTPie CLI) | Workflows instrumented; pilot instrumentation data collected during testing |
| Full 30-run data collection | Not yet started — see `experiments/project-01-httpie-cli/RESEARCH_LOG.md` |

**Pilot finding (illustrative, from early instrumentation testing, not the validated 30-run protocol):** Caching + consolidation reduces test matrix energy by 7.1% (1,484 J → 1,378 J). Dependency installation stage alone: −16.8%.

---

## Experiment Branches (GitHub Actions)

The GitHub Actions CI/CD experiments run on a fork of HTTPie CLI:
https://github.com/Umer-2612/httpie-cli-carbon-study

| Branch | Config | Strategy |
|---|---|---|
| `experiment/c1-baseline` | C1 | Baseline, no optimisation |
| `experiment/c2-pip-cache` | C2 | Dependency caching |
| `experiment/c3-consolidation` | C3 | Workflow consolidation |
| `experiment/c4-combined` | C4 | Caching + consolidation + path filters |

---

## Key Files

| File | What it contains |
|---|---|
| `dissertation/chapters/01_introduction.md` | Introduction: purpose, background, problem statement, research questions, objectives, contributions preview |
| `dissertation/chapters/02_literature_review.md` | Literature review (sections 2.1–2.7), expanded per-paper depth and gap analysis |
| `dissertation/chapters/03_methodology.md` | Methodology: research rationale, project selection, configurations, SCI framework |
| `dissertation/chapters/04_design.md` | Design: pipeline architecture, instrumentation pipeline, measurement stages, worked example, diagrams |
| `dissertation/chapters/05_results.md` | Results chapter with statistical approach and pilot data |
| `dissertation/references/bibliography.md` | All references in Harvard format, including subject-project citations |
| `experiments/project-01-httpie-cli/README.md` | Project summary, pilot results, how to run |
| `experiments/project-01-httpie-cli/RESEARCH_LOG.md` | Audit log: decisions and findings |
| `notes/weekly_log.md` | Week-by-week progress log |
