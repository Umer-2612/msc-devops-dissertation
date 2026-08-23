# Chapter 5: Results

## 5.1 Overview

This chapter sets out the statistical analysis approach (Section 5.2) and then presents the energy and carbon measurement results for each experimental configuration. Section 5.3 reports the pilot measurements from the HTTPie CLI project, which validate the measurement methodology and provide initial directional findings. Section 5.4 presents the full 30-run statistical results, Section 5.5 the cross-project comparison, and Section 5.6 the multi-region carbon analysis, once data collection for each project completes.

All energy measurements are from real Eco-CI runs on GitHub-hosted `ubuntu-latest` runners. Eco-CI reported a carbon intensity of 472 gCO₂eq/kWh for the Azure runner location throughout the runs. SCI figures are computed as the operational component E × I at the run level, following Section 3.6.

## 5.2 Analytical Approach

All statistical analysis is performed in a Python analysis notebook using scipy, pandas, numpy, and matplotlib.

The analysis begins with normality testing: Shapiro-Wilk tests are applied to each configuration-by-stage sample distribution. The dependency-installation stage is expected to be non-normally distributed because of network variability (PyPI and registry CDN response times); test execution is expected to be approximately normally distributed for CPU-bound workloads.

The primary comparison uses Wilcoxon signed-rank tests to compare total energy per CI run between C1 (baseline) and each of C2, C3, and C4. Paired samples (same project, same runs) justify the signed-rank variant over the unpaired Mann-Whitney U test. Because three comparisons are made simultaneously, a Bonferroni correction adjusts the significance threshold to α = 0.05 / 3 = 0.017. Effect size is reported with Cliff's delta (δ), interpreted following Romano et al. (2006): |δ| below 0.147 negligible, below 0.330 small, below 0.474 medium, and 0.474 or above large.

For RQ2, effect sizes and percentage reductions are compared across projects by language and size category to assess the consistency of each strategy's effectiveness. Non-parametric tests are preferred throughout, for consistency, given the expected non-normality of the dependency-installation stage. With n = 30 per configuration, Wilcoxon has more than 95% power to detect medium effect sizes (|δ| > 0.33) at α = 0.017.

## 5.3 Pilot Measurements: HTTPie CLI

The pilot runs are single executions per configuration. They are presented as descriptive observations that validate the instrumentation and indicate the direction and mechanism of each effect, using the same underlying figures introduced mechanically in Section 4.6. No statistical inference is drawn from them; that is the role of the full 30-run protocol in Section 5.4.

### 5.3.1 C1 Baseline: Code-Style Job

| Stage | CPU (%) | Energy (J) | Power (W) | Duration (s) |
|---|---|---|---|---|
| checkout | 25.64 | 4.79 | 4.10 | 1.17 |
| dependency-installation | 28.73 | 48.51 | 4.19 | 11.57 |
| lint | 25.29 | 70.25 | 4.07 | 17.26 |
| **Total** | **26.63** | **123.55** | **4.12** | **30.00** |

*Table 5.1: C1 baseline code-style job, per-stage pilot energy measurement.*

The code-style job consumes 123.55 J in total. Applying the Irish grid intensity, this corresponds to an operational SCI of 0.0118 gCO₂eq per run.

### 5.3.2 C2 Pip-Cached Pipeline: Test Matrix

| Job | Python | dep-install (J) | test-exec (J) | Total (J) |
|---|---|---|---|---|
| Tests | 3.12 | 104.45 | 367.57 | 477.33 |
| Tests | 3.11 | 121.94 | 353.86 | 475.80 |
| Tests | 3.10 | 162.18 | 362.61 | 530.99 |
| **Test matrix total** | | **388.57** | **1,084.04** | **1,484.12** |

*Table 5.2: C2 (caching) pilot test-matrix energy by Python version.*

### 5.3.3 C4 Combined (Caching and Consolidation): Test Matrix

| Job | Python | dep-install (J) | test-exec (J) | Total (J) |
|---|---|---|---|---|
| Tests | 3.12 | 124.23 | 357.42 | 481.65 |
| Tests | 3.11 | 93.67 | 335.34 | 433.95 |
| Tests | 3.10 | 105.33 | 353.33 | 462.86 |
| **Test matrix total** | | **323.24** | **1,046.08** | **1,378.46** |

*Table 5.3: C4 (combined) pilot test-matrix energy by Python version.*

### 5.3.4 C2 versus C4: Initial Comparison

| Metric | C2 | C4 | Change |
|---|---|---|---|
| Test matrix total (J) | 1,484.12 | 1,378.46 | −7.1% |
| dep-install sum (J) | 388.57 | 323.24 | −16.8% |
| test-execution sum (J) | 1,084.04 | 1,046.08 | −3.5% |
| SCI test matrix, Ireland (gCO₂eq) | 0.1422 | 0.1321 | −7.1% |
| Average test job duration (s) | 130.94 | 125.79 | −3.9% |

*Table 5.4: Pilot comparison between C2 and C4 test-matrix energy and SCI.*

The 7.1% total energy reduction from C2 to C4 is driven primarily by the dependency installation stage (−16.8%), not test execution (−3.5%). Caching targets the most variable and reducible stage. This comparison is between C2 and C4 rather than against the C1 baseline, because the C1 and C3 pilot runs for the full test matrix are not part of the pilot set; the baseline-referenced comparisons that attribute savings to caching and consolidation separately are produced by the full protocol in Section 5.4.

## 5.4 Full 30-Run Results

This section reports descriptive statistics, Shapiro-Wilk normality tests, and Wilcoxon signed-rank comparisons of total energy per run between C1 and each of C2, C3, and C4, with Bonferroni-corrected significance and Cliff's delta effect sizes, for the full 30-run dataset. It is populated once collection of the 30 runs per configuration completes for each project (Section 3.5). The consolidation comparison (C1 versus C3) is reported for the projects that ship more than one workflow, per Section 3.2.5.

*[Figure 5.1: Grouped bar chart of mean total energy per run, by configuration (C1–C4) and by pipeline stage, with 95% confidence intervals — to be generated once the 30-run dataset is collected.]*

*[Figure 5.2: Box plots of the per-run energy distributions underlying the Wilcoxon comparisons, one panel per configuration pair (C1 vs C2, C1 vs C3, C1 vs C4) — to be generated once the 30-run dataset is collected.]*

## 5.5 Cross-Project Comparison (RQ2)

This section compares the percentage energy reductions and Cliff's delta effect sizes across the selected projects, along the language axis (Python, JavaScript, Java, Go, holding the HTTP-client domain constant) and the size axis. It is populated as each project's dataset completes.

*[Figure 5.3: Grouped bar chart of percentage energy reduction (C1 to C4) by project and language, illustrating whether the effect size is consistent across the language axis — to be generated once cross-project data is collected.]*

## 5.6 Multi-Region SCI Analysis

Holding the estimated test-matrix energy constant and varying only the grid intensity gives the operational carbon of one run across five regions.

| Region | Intensity (gCO₂eq/kWh) | C2 SCI | C4 SCI | Change |
|---|---|---|---|---|
| Ireland | 345 | 0.1422 | 0.1321 | −7.1% |
| Germany | 350 | 0.1443 | 0.1340 | −7.1% |
| Norway | 25 | 0.0103 | 0.0096 | −7.1% |
| USA | 386 | 0.1591 | 0.1478 | −7.1% |
| Singapore | 408 | 0.1682 | 0.1562 | −7.1% |

*Table 5.5: SCI per run across five electricity grid regions, C2 versus C4 pilot energy figures.*

The Norway-to-Singapore ratio, 0.0103 against 0.1682, is a 15.3× differential arising from runner location alone, with the pipeline and its energy held constant.

*[Figure 5.4: Coloured bar chart of SCI per run by region (Ireland, Germany, Norway, USA, Singapore), C2 and C4 side by side, to visualise the regional carbon differential against the configuration-level effect — to be generated once the full dataset confirms the pilot direction.]*

---
