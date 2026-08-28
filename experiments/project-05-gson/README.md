# Project 05: Gson (Java) — Size-Axis Observation

## What This Is

[Gson](https://github.com/google/gson) (24k+ stars, Apache-2.0) is the size-axis project (Section 3.2.2): a larger, differently-scoped Maven multi-module project (JSON serialization, not an HTTP client), analysed separately from the cross-language arm to test whether strategy effects hold as project size and build complexity increase. Checked out externally at `gson-parent-2.14.0`; no fork.

## The Four Configurations

Workflow files: `.github/workflows/p05-gson-c{1,2,3,4}-*.yml` (repo root).

Gson's own CI runs a Java-version matrix (11/17/21/25) plus native-image and reproducible-build jobs; only the core test path on a single JDK (21) is reproduced. The measured command is scoped to `mvn test --projects gson` rather than the root aggregator's `mvn test`, which otherwise attempts to build every submodule (`metrics`, `test-graal-native-image`, `test-jpms`, `test-shrinker`), several of which need toolchains beyond this setup. Nothing to consolidate, so C1 and C3 are structurally identical.

| Config | File | What changes |
|---|---|---|
| C1 — Baseline | `p05-gson-c1-tests.yml` | No caching |
| C2 — Caching | `p05-gson-c2-tests.yml` | + `cache: maven` on setup-java |
| C3 — Consolidation | `p05-gson-c3-consolidated.yml` | Structurally identical to C1 |
| C4 — Combined | `p05-gson-c4-combined.yml` | Same caching as C2 |

## Status

All four configurations validated before the full protocol; C3's first validation attempt hit a transient Maven Central registry resolution error (unrelated to the workflow itself — the identical C1 YAML passed), and the retry succeeded. Full n = 30 protocol complete for all four configurations. See `dissertation/DISSERTATION.md`, Chapter 5, for results.

## Reproducing

```bash
set -a && source ../.env && set +a
python3 ../project-01-httpie-cli/scripts/trigger_runs.py --branch main --workflow p05-gson-c1-tests.yml --runs 30
python3 ../project-01-httpie-cli/scripts/collect_results.py
```

`collect_results.py` queries the whole repository in one pass and writes every project's rows to `../project-01-httpie-cli/results/raw_data.csv` (see `experiments/README.md`); this project has no separate `results/` folder of its own.
