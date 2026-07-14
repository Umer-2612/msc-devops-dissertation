# Chapter 4: Results


## 4.1 Overview

This chapter presents the energy and carbon measurement results for each experimental configuration. Section 4.2 reports the pilot measurements from the HTTPie CLI project (n = 1 per configuration), which validate the measurement methodology and provide initial directional findings. Section 4.3 will present the full 30-run statistical results once data collection is complete.

All energy measurements are from real Eco-CI runs on GitHub-hosted `ubuntu-latest` runners. Eco-CI reported a carbon intensity of **472 gCO₂eq/kWh** for the Azure runner location throughout all runs.

---

## 4.2 Pilot Measurements: HTTPie CLI (n = 1 per configuration)

> These are real measurements from initial triggered runs. They are presented as descriptive observations only; no statistical inference is drawn from n = 1 data.

### 4.2.1 C1 Baseline: Code-Style Job

| Stage | CPU (%) | Energy (J) | Power (W) | Duration (s) |
|---|---|---|---|---|
| checkout | 25.64 | 4.79 | 4.10 | 1.17 |
| dependency-installation | 28.73 | 48.51 | 4.19 | 11.57 |
| lint | 25.29 | 70.25 | 4.07 | 17.26 |
| **Total** | **26.63** | **123.55** | **4.12** | **30.00** |

**SCI (C1 code-style): 0.0248 gCO₂eq per run**

### 4.2.2 C2 Pip-Cached Pipeline: Test Matrix

| Job | Python | dep-install (J) | test-exec (J) | Total (J) | SCI (gCO₂eq) |
|---|---|---|---|---|---|
| Tests | 3.12 | 104.45 | 367.57 | 477.33 | 0.0998 |
| Tests | 3.11 | 121.94 | 353.86 | 475.80 | 0.0990 |
| Tests | 3.10 | 162.18 | 362.61 | 530.99 | 0.1078 |
| **Test matrix total** | | **388.57** | **1,084.04** | **1,484.12** | **0.3067** |

### 4.2.3 C4 Combined (Caching + Consolidation + Path Filtering)

| Job | Python | dep-install (J) | test-exec (J) | Total (J) | SCI (gCO₂eq) |
|---|---|---|---|---|---|
| Tests | 3.12 | 124.23 | 357.42 | 481.65 | 0.1003 |
| Tests | 3.11 | 93.67 | 335.34 | 433.95 | 0.0911 |
| Tests | 3.10 | 105.33 | 353.33 | 462.86 | 0.0970 |
| Coverage | 3.10 | 82.64 | — | 633.98 | 0.1346 |
| **Test matrix total** | | **323.24** | **1,046.08** | **1,378.46** | **0.2884** |

### 4.2.4 C2 vs C4: Initial Comparison

| Metric | C2 | C4 | C4 vs C2 |
|---|---|---|---|
| Test matrix total (J) | 1,484.12 | 1,378.46 | **−7.1%** |
| dep-install sum (J) | 388.57 | 323.24 | **−16.8%** |
| test-execution sum (J) | 1,084.04 | 1,046.08 | −3.5% |
| SCI test matrix (gCO₂eq) | 0.3067 | 0.2884 | −6.0% |
| Avg. test job duration (s) | 130.94 | 125.79 | −3.9% |

**Key pilot finding:** The 7.1% total energy reduction from C2 to C4 is driven primarily by the dependency installation stage (−16.8%), not test execution (−3.5%). Caching targets the most variable and reducible stage.

### 4.2.5 Multi-Region SCI Analysis (RQ3, Pilot)

| Region | Intensity (gCO₂eq/kWh) | C2 SCI | C4 SCI | C4 vs C2 |
|---|---|---|---|---|
| Ireland | 345 | 0.1422 | 0.1321 | −7.1% |
| Germany | 350 | 0.1443 | 0.1340 | −7.1% |
| Norway | 25 | 0.0103 | 0.0096 | −7.1% |
| USA | 386 | 0.1591 | 0.1478 | −7.1% |
| Singapore | 408 | 0.1682 | 0.1562 | −7.1% |

**Norway vs Singapore ratio:** 0.0103 vs 0.1682 = **15.3× differential** from runner location alone.

---

## 4.3 Full 30-Run Results

This section presents descriptive statistics, normality tests, and Wilcoxon signed-rank comparisons for the full 30-run dataset across all four configurations. Results are drawn from `results/raw_data.csv` produced by `scripts/collect_results.py` after triggering the complete run protocol.

*[Data collection in progress. This section will be completed once all 30 × 4 runs are triggered and collected.]*

---

## 4.4 C3 Results (Consolidation-Only)

C3 isolates the workflow consolidation effect by merging all three stages into a single `ci-consolidated.yml` without adding caching. Without C3 data, it is not possible to attribute the energy change in C4 to consolidation versus caching independently. C3 runs are the next priority after C1 baseline data collection is complete.
