# Project 01: HTTPie CLI (Python) — CI/CD Carbon Emissions Study

> **Dissertation artefact** for the MSc DevOps dissertation:
> *"Greening the Pipeline: An Empirical Comparison of CI/CD Refinement Strategies and Their Carbon Impact Across Open-Source Projects"*
> **Student:** Umer Karachiwala (L00196895), ATU Donegal, Ireland

## What This Is

HTTPie CLI ([httpie/cli](https://github.com/httpie/cli), 34,000+ stars, BSD-3) is the anchor project (Section 3.2.4). No fork is used: every configuration checks out `httpie/cli@3.2.4` externally, at the fixed tag, from a workflow file living in this repository's own `.github/workflows/`. The subject code never changes; only the pipeline configuration around it does.

## The Four Configurations

Workflow files: `.github/workflows/p01-httpie-c{1,2,3,4}-*.yml` (root of this repo, not in this folder).

| Config | Files | What changes |
|---|---|---|
| C1 — Baseline | `p01-httpie-c1-tests.yml`, `-c1-code-style.yml`, `-c1-coverage.yml` | 3 separate workflows, no caching |
| C2 — Caching | `p01-httpie-c2-*.yml` (same 3 files) | + `cache: pip`, `cache-dependency-path: setup.cfg` |
| C3 — Consolidation | `p01-httpie-c3-consolidated.yml` | 3 stages merged into 1 workflow, no caching |
| C4 — Combined | `p01-httpie-c4-combined.yml` | C3's structure + caching |

## Status

All four configurations are validated (one clean run each, real Eco-CI data confirmed) as of 23 August 2026. Two environment-drift bugs were found and fixed during validation — see [`RESEARCH_LOG.md`](RESEARCH_LOG.md) for the full audit trail (issues C1-05, C1-06). The full n=30 protocol has not yet been run; `results/raw_data.csv` is populated once it has.

## Reproducing

```bash
set -a && source ../.env && set +a   # GITHUB_TOKEN, GITHUB_REPO
python3 scripts/trigger_runs.py --branch main --workflow p01-httpie-c1-tests.yml --runs 30
python3 scripts/collect_results.py    # writes results/raw_data.csv
```

Run once per workflow file (8 total for this project). See `scripts/run_experiment.sh` for the full sequence.

## Files

| File | Purpose |
|---|---|
| `RESEARCH_LOG.md` | Full audit trail: bugs found, fixes applied, validation runs |
| `scripts/trigger_runs.py` | Fires repeated `workflow_dispatch` runs, waits, enforces the 5-minute interval |
| `scripts/collect_results.py` | Downloads Eco-CI artifacts, writes `results/raw_data.csv` |
| `scripts/run_experiment.sh` | Runs the full 30×8 protocol for this project |
| `results/raw_data.csv` | Consolidated dataset (empty until the 30-run protocol completes) |
| `analysis/energy_analysis.ipynb` | Statistical analysis: Shapiro-Wilk, Wilcoxon, Bonferroni, Cliff's delta, SCI |
