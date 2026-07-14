# Chapter 3: Methodology


## 3.1 Research Design

This dissertation adopts a **quantitative experimental research design**. The study is empirical: it collects measured data from real CI/CD pipeline executions rather than relying on simulation, estimation from existing datasets, or qualitative analysis. The design follows the controlled experiment approach described by Wohlin et al. (2012) for software engineering research: a baseline configuration is established, independent variables (pipeline refinement strategies) are applied one at a time, and the dependent variable (energy consumption / SCI carbon score) is measured under controlled conditions for each configuration.

The study uses a **within-subjects design**: each project is measured under all four configurations (C1–C4), enabling paired statistical comparisons that eliminate between-project variability as a confound.

---

## 3.2 Project Selection

### 3.2.1 Selection Criteria

Projects are selected from public GitHub repositories using the following inclusion criteria:

| Criterion | Requirement | Rationale |
|---|---|---|
| CI platform | GitHub Actions only | Eco-CI is trained for GitHub-hosted `ubuntu-latest` runners |
| Runner type | GitHub-hosted `ubuntu-latest` | Eco-CI's SPECpower model targets this hardware profile |
| Stars | > 500 | Indicates real-world active use |
| Last commit | Active within 3 months of study | Ensures maintained CI configuration |
| Test suite | Automated tests executing in CI | Testing is the dominant energy-consuming stage |
| Licence | MIT, Apache 2.0, or equivalent | Required for forking and YAML modification |
| Dependency manager | pip, npm, Maven, or Gradle | Enables `cache: pip/npm/maven` strategy |
| Workflow files | 2–10 `.github/workflows/*.yml` | Ensures non-trivial pipeline; not too complex to audit |
| No self-hosted runners | Confirmed `runs-on: ubuntu-latest` | Self-hosted runners differ in hardware profile |

**Exclusion criteria:** Projects using only scheduled (cron) triggers without push/PR triggers; projects with encrypted workflows or restricted Actions permissions; monorepos with more than 20 workflow files (complexity exceeds scope).

### 3.2.2 Language and Size Distribution

To address RQ2 (cross-project consistency), projects are selected to span at least:
- Two programming languages (minimum: Python + one of JavaScript/TypeScript/Java/Go)
- Two project size categories: small (<5,000 lines of source code) and medium/large (>5,000 lines)

The pilot study reported in this dissertation uses **HTTPie CLI** (Python, ~4,000 LOC, 34,000+ stars) as the first and anchor project. Additional projects are selected and forked in the weeks following the initial pilot.

### 3.2.3 HTTPie CLI: Pilot Project

**HTTPie CLI** (https://github.com/httpie/cli) is a production-grade Python HTTP client at version 3.2.4. Its pre-study GitHub Actions configuration consists of three independent workflow files (`tests.yml`, `code-style.yml`, `coverage.yml`) that each reinstall all project dependencies from scratch on every trigger, with no caching strategy. This is representative of how mature Python open-source projects accumulate CI configuration without revisiting default behaviours over time.

The repository is forked to `https://github.com/Umer-2612/httpie-cli-carbon-study` with `workflow_dispatch` triggers added to all workflows for controlled on-demand execution.

---

## 3.3 Experiment Configurations

Four configurations are evaluated per project. Each represents an independently applicable and incrementally additive refinement:

| Config | Branch | Structure | Pip Cache | Path Filters |
|---|---|---|---|---|
| **C1 — Baseline** | `experiment/c1-baseline` | 3 separate workflow files | No | File-specific per workflow |
| **C2 — Caching** | `experiment/c2-pip-cache` | Same 3 files as C1 | Yes (`cache: pip` + `cache-dependency-path`) | Same as C1 |
| **C3 — Consolidation** | `experiment/c3-consolidation` | 1 merged file (`ci-consolidated.yml`) | No | None (workflow_dispatch bypass) |
| **C4 — Combined** | `experiment/c4-combined` | 1 merged file + caching + path filters | Yes | Combined source path filters |

**C1** establishes the baseline energy consumption of the unmodified pipeline, with only Eco-CI instrumentation added.

**C2** tests the impact of dependency caching in isolation. The `cache: pip` parameter combined with `cache-dependency-path: setup.cfg` ensures the pip cache is keyed to the project's dependency specification file, enabling cache hits on subsequent runs.

**C3** tests the impact of workflow consolidation in isolation. Three separate workflow files are merged into a single `ci-consolidated.yml` with a sequential job chain (`lint → test → coverage`), eliminating the per-workflow runner provisioning overhead while maintaining identical total work.

**C4** tests the combined impact of all three strategies: caching (from C2) + consolidation (from C3) + path-based trigger filtering for push/PR events, which prevents the pipeline from executing when non-source files (documentation, configuration) are changed.

---

## 3.4 Instrumentation: Eco-CI Integration

Each workflow is instrumented with the Eco-CI Energy Estimation tool (`green-coding-solutions/eco-ci-energy-estimation@v5`) following a consistent pattern:

1. `task: start-measurement`: initialises CPU utilisation sampling at job start
2. `task: get-measurement` with `label:`: captures cumulative energy at each stage boundary
3. `task: display-results` with `json-output: true`: serialises all measurements to `/tmp/eco-ci/eco-ci-results.json`
4. `actions/upload-artifact@v4`: uploads the JSON output as a workflow artifact

**Critical implementation requirements:**
- `if: always()` on every `get-measurement` step: prevents step-skipping on test failure
- `continue-on-error: true` on all Eco-CI steps: prevents measurement tool errors from aborting jobs
- `cache-dependency-path: setup.cfg` on C2/C4 `setup-python` steps: required because HTTPie uses `setup.cfg`, not `requirements.txt`

A pre-study audit of all four branches was conducted before data collection, identifying and correcting six critical issues including unresolved merge conflicts, missing `workflow_dispatch` triggers, and an incorrect YAML scope for `continue-on-error`. Full audit findings are documented in Appendix A.

---

## 3.5 Measurement Stages

Energy is measured at the following stage boundaries, labelled consistently across all configurations:

| Stage Label | Pipeline Phase |
|---|---|
| `checkout` | `actions/checkout@v4`: repository clone |
| `dependency-installation` | `make install` / `pip install`: package installation |
| `lint` | `make codestyle`: static analysis (code-style job) |
| `test-execution` | `make test`: full test suite (Python 3.10, 3.11, 3.12 matrix) |
| `coverage` | `make test-cover`: test suite with coverage instrumentation |
| `dist-test` | `make test-dist`: distribution build validation |

---

## 3.6 Data Collection Procedure

1. Each configuration is triggered via `workflow_dispatch` on the relevant experiment branch
2. A minimum inter-run interval of 5 minutes is maintained to reduce shared-runner thermal and warm-up effects
3. No code changes are committed between runs within a configuration
4. Target sample size: **n = 30 per configuration** per project
5. After each run completes, Eco-CI artifacts are automatically uploaded to the repository's Actions artifact store
6. The `scripts/collect_results.py` script queries the GitHub Actions API, downloads all `eco-ci-*` artifacts, and consolidates measurements into `results/raw_data.csv`

The CSV schema:
```
run_id | config | workflow | branch | stage | energy_joules | duration_seconds | timestamp | python_version
```

---

## 3.7 Carbon Calculation: SCI Framework

SCI scores are computed per run per configuration using ISO/IEC 21031:2024:

```
SCI = (E × I) + M
```

Where:
- **E** = total energy per run (J → converted to kWh: divide by 3,600,000)
- **I** = carbon intensity of the electricity grid (gCO₂eq/kWh)
  - Eco-CI reports 472 gCO₂eq/kWh for Azure GitHub-hosted runners
  - Multi-region analysis uses: Ireland 345, Germany 350, Norway 25, USA 386, Singapore 408
- **M** = embodied carbon (reported by Eco-CI per job)
- **R** = 1 complete CI pipeline run (the functional unit)

Result: **gCO₂eq per CI run**

---

## 3.8 Statistical Analysis

All statistical analysis is performed in `analysis/energy_analysis.ipynb` using Python (scipy, pandas, numpy, matplotlib).

**Step 1: Normality testing.** Shapiro-Wilk tests are applied to each (configuration × stage) sample distribution. The dependency-installation stage is expected to be non-normally distributed due to network variability (PyPI CDN response times); test execution is expected to be approximately normally distributed for CPU-bound workloads.

**Step 2: Primary comparison.** Wilcoxon signed-rank tests compare total energy per CI run between C1 (baseline) and each of C2, C3, C4. Paired samples (same project, same runs) justify the signed-rank variant over the unpaired Mann-Whitney U test.

**Step 3: Multiple comparisons correction.** Bonferroni correction adjusts the significance threshold for three simultaneous comparisons:
```
α_corrected = 0.05 / 3 = 0.017
```

**Step 4: Effect size.** Cliff's delta (δ) is computed for each comparison. Interpretation follows Romano et al. (2006): |δ| < 0.147 negligible, < 0.330 small, < 0.474 medium, ≥ 0.474 large.

**Step 5: Cross-project analysis (RQ2).** Effect sizes and percentage reductions are compared across projects by language and size category to assess consistency of strategy effectiveness.

**Rationale for non-parametric approach:** Given the expected non-normality of the dependency-installation stage, non-parametric tests are preferred throughout for consistency. With n = 30 per configuration, Wilcoxon has >95% power to detect medium effect sizes (|δ| > 0.33) at α = 0.017.

---

## 3.9 Ethical and Reproducibility Considerations

All projects studied are public open-source repositories licensed for modification. No private data, user data, or personally identifiable information is involved. All experiment code, raw data, and analysis notebooks are published in the replication package at `https://github.com/Umer-2612/httpie-cli-carbon-study`. The repository includes instructions for reproducing all measurements via `workflow_dispatch`, making the study independently verifiable.

---

