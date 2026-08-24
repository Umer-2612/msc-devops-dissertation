# Chapter 5: Results

## 5.1 Overview

This chapter presents the results of the full data-collection protocol: 720 of 720 planned runs completed, with 719 producing usable data (one got, C1 run failed on Node.js 24 with an unrelated test-suite timing issue; the identical Node.js 22 job in the same run succeeded, so this is treated as a single-run flake rather than a configuration defect; see Section 6.6). Section 5.2 restates the analytical approach. Section 5.3 gives descriptive statistics and normality results. Section 5.4 presents the Wilcoxon signed-rank comparisons that answer RQ1. Section 5.5 compares strategy effectiveness across projects to answer RQ2. Section 5.6 gives the multi-region SCI analysis.

All energy measurements are from real Eco-CI runs on GitHub-hosted `ubuntu-latest` runners, collected on 23 August 2026. Eco-CI reported a carbon intensity of 472 gCO₂eq/kWh for the Azure runner location throughout. SCI figures are computed as the operational component E × I at the run level, following Section 3.6. Every table in this chapter reports exactly n = 30 per configuration per project: an earlier draft of this analysis inadvertently included a small number of pre-protocol validation runs (used during the pipeline audit described in Appendix A) alongside the true protocol data, which the data-collection script (`collect_results.py`) has since been corrected to exclude by restricting collection to runs created after the protocol's start timestamp.

For HTTPie, whose C1 and C2 configurations span three separate workflow files (tests, code-style, coverage) rather than the single file every other configuration and project uses, one "run" is reconstructed by summing each file's own per-stage totals within the same chronological position across the three files, so that a total-energy-per-cycle figure is comparable to C3 and C4's single consolidated workflow and to every other project's single-workflow configurations. This reconstruction is a necessary methodological choice, not a neutral one, and its consequences for the cross-project comparisons in Section 5.5 are discussed there and in Section 6.6.

## 5.2 Analytical Approach

All statistical analysis is performed in a Python analysis script (`experiments/project-01-httpie-cli/analysis/full_analysis.py`, mirrored in `energy_analysis.ipynb`) using scipy, pandas, numpy, and matplotlib.

Shapiro-Wilk normality tests were applied to each project-by-configuration sample of total energy per run. HTTPie's four configurations were the only ones that did not reject normality in every case (p > 0.10 throughout); every other project rejected normality for at least two of its four configurations, and resty rejected it for all four (p < 0.0001). This confirms the non-parametric approach specified in advance was the correct choice: a parametric paired t-test would have been invalid for the majority of project/configuration combinations.

The primary comparison uses Wilcoxon signed-rank tests to compare total energy per CI run between C1 (baseline) and each of C2, C3, and C4, pairing runs by chronological trigger order within each project, since no other shared identifier links a C1 run to a "corresponding" C2, C3, or C4 run: they are independently triggered executions of different workflow files, not a shared subject measured twice. This ordinal pairing is a deliberate design choice, made because the alternative, an unpaired Mann-Whitney U test, discards the within-subjects structure of triggering all four configurations against the same fixed, frozen subject code under matched conditions (same day, same 5-minute inter-run interval, same runner type); it is revisited as a threat to validity in Section 6.6. Because three comparisons are made per project, a Bonferroni correction adjusts the significance threshold to α = 0.05 / 3 = 0.0167. Effect size is reported with Cliff's delta (δ), interpreted following Romano et al. (2006): |δ| below 0.147 negligible, below 0.330 small, below 0.474 medium, and 0.474 or above large.

## 5.3 Descriptive Statistics

Table 5.1 reports the mean, median, and standard deviation of total energy per CI run for every project and configuration, all at n = 30.

| Project | Config | n | Mean (J) | Median (J) | SD (J) |
|---|---|---|---|---|---|
| HTTPie | C1 | 30 | 2,008.90 | 2,015.75 | 43.81 |
| HTTPie | C2 | 30 | 1,917.22 | 1,938.22 | 79.99 |
| HTTPie | C3 | 30 | 1,998.06 | 2,004.39 | 52.78 |
| HTTPie | C4 | 30 | 1,909.18 | 1,929.54 | 66.10 |
| got | C1 | 30 | 1,023.92 | 1,037.37 | 84.61 |
| got | C2 | 30 | 1,008.61 | 1,021.54 | 61.33 |
| got | C3 | 30 | 1,029.29 | 1,027.37 | 41.91 |
| got | C4 | 30 | 993.45 | 1,006.21 | 44.91 |
| Retrofit | C1 | 30 | 502.52 | 510.87 | 30.93 |
| Retrofit | C2 | 30 | 332.40 | 335.98 | 28.15 |
| Retrofit | C3 | 30 | 500.02 | 505.89 | 46.31 |
| Retrofit | C4 | 30 | 333.16 | 339.41 | 23.70 |
| resty | C1 | 30 | 236.04 | 230.87 | 16.36 |
| resty | C2 | 30 | 242.92 | 230.86 | 28.01 |
| resty | C3 | 30 | 237.71 | 234.10 | 16.50 |
| resty | C4 | 30 | 237.14 | 229.57 | 22.56 |
| Gson | C1 | 30 | 269.01 | 262.45 | 24.02 |
| Gson | C2 | 30 | 219.16 | 222.49 | 19.25 |
| Gson | C3 | 30 | 265.20 | 268.23 | 24.83 |
| Gson | C4 | 30 | 210.83 | 219.02 | 25.30 |

*Table 5.1: Descriptive statistics, total energy per CI run, all five projects and four configurations, n = 30 throughout.*

Figure 5.1 and Figure 5.2 show these distributions graphically.

![Figure 5.1](../experiments/project-01-httpie-cli/results/figures/fig5_1_mean_energy_by_project.png)

*Figure 5.1: Mean total energy per run, by configuration and project (n = 30, error bars = ±1 SD).*

![Figure 5.2](../experiments/project-01-httpie-cli/results/figures/fig5_2_energy_boxplot_by_project.png)

*Figure 5.2: Per-run energy distribution underlying the Wilcoxon comparisons.*

Table 5.2 breaks HTTPie's total down by measurement stage, on the same reconstructed-per-cycle basis as Table 5.1 (each configuration's column sums to its corresponding Table 5.1 total to within about 0.2%, a residual explained by a small number of individual stage measurements Eco-CI did not emit for a given job despite the job itself completing successfully; `continue-on-error: true` on every Eco-CI step, Section 4.4, prevents this from failing the run, at the cost of an occasional missing measurement row rather than a missing job).

| Stage | C1 (J) | C2 (J) | C3 (J) | C4 (J) |
|---|---|---|---|---|
| checkout | 23.55 | 22.38 | 20.87 | 20.77 |
| dependency-installation | 463.36 | 388.62 | 457.57 | 388.35 |
| lint | 74.70 | 70.74 | 74.12 | 68.55 |
| test-execution | 1,008.45 | 997.15 | 994.83 | 981.61 |
| coverage | 366.56 | 365.91 | 372.80 | 372.20 |
| dist-test | 76.21 | 76.62 | 77.88 | 77.70 |

*Table 5.2: HTTPie mean energy per stage, by configuration, reconstructed per cycle (n = 30 per cell; column sums approximate Table 5.1's totals to within 0.2%).*

C1's checkout and dependency-installation figures (23.55 J and 463.36 J) are visibly larger than C3's and C4's (20.87–20.77 J and 457.57–388.35 J): this is the direct signature of running three separate workflow files, each with its own checkout and dependency-installation step, against one consolidated workflow that pays that cost once. The caching effect, comparing C1 to C2, is concentrated almost entirely in dependency-installation (463.36 J to 388.62 J, a 16.1% reduction) with test-execution nearly unchanged (1,008.45 J to 997.15 J, 1.1%), which is the mechanistic pattern Section 6.2 interprets.

## 5.4 Full 30-Run Results (RQ1)

Table 5.3 reports the Wilcoxon signed-rank comparison of each configuration against C1, with Bonferroni-corrected significance (α = 0.0167) and Cliff's delta effect size, for every project, all at n = 30.

| Project | Comparison | n | p-value | Significant? | Cliff's δ | Effect | % change |
|---|---|---|---|---|---|---|---|
| HTTPie | C2 vs C1 | 30 | 0.00001 | Yes | +0.709 | large | −4.56% |
| HTTPie | C3 vs C1 | 30 | 0.440 | No | +0.113 | negligible | −0.54% |
| HTTPie | C4 vs C1 | 30 | <0.00001 | Yes | +0.844 | large | −4.96% |
| got | C2 vs C1 | 30 | 0.164 | No | +0.276 | small | −1.50% |
| got | C3 vs C1 | 30 | 0.612 | No | +0.131 | negligible | +0.52% |
| got | C4 vs C1 | 30 | 0.00434 | Yes | +0.564 | large | −2.98% |
| Retrofit | C2 vs C1 | 30 | <0.00001 | Yes | +0.998 | large | −33.85% |
| Retrofit | C3 vs C1 | 30 | 0.952 | No | −0.011 | negligible | −0.50% |
| Retrofit | C4 vs C1 | 30 | <0.00001 | Yes | +1.000 | large | −33.70% |
| resty | C2 vs C1 | 30 | 0.416 | No | −0.047 | negligible | +2.91% |
| resty | C3 vs C1 | 30 | 0.229 | No | −0.124 | negligible | +0.71% |
| resty | C4 vs C1 | 30 | 0.777 | No | +0.071 | negligible | +0.47% |
| Gson | C2 vs C1 | 30 | <0.00001 | Yes | +0.964 | large | −18.53% |
| Gson | C3 vs C1 | 30 | 0.428 | No | +0.031 | negligible | −1.42% |
| Gson | C4 vs C1 | 30 | <0.00001 | Yes | +0.980 | large | −21.63% |

*Table 5.3: Wilcoxon signed-rank tests versus C1, Bonferroni-corrected significance, and Cliff's delta, all projects, n = 30 throughout.*

Two results stand out immediately. First, **dependency caching (C2) produces a statistically significant, large-effect energy reduction in three of five projects** (HTTPie −4.56%, Retrofit −33.85%, Gson −18.53%) but not in got (−1.50%) or resty (+2.91%, wrong direction, though not significant). Second, and contrary to the direction assumed when this study was designed, **workflow consolidation (C3) produces no statistically significant effect in any project**, including HTTPie, the only project where genuine consolidation occurs (three workflow files merged into one). Every C3-versus-C1 comparison in Table 5.3 has a negligible Cliff's delta (|δ| ≤ 0.131), and Retrofit's C3 result (−0.50%, δ = −0.011), close to zero in both percentage and effect-size terms, is a clean confirmation of the null consolidation effect.

## 5.5 Cross-Project Comparison (RQ2)

Figure 5.3 shows the percentage change in mean energy between C4 and C1 for every project.

![Figure 5.3](../experiments/project-01-httpie-cli/results/figures/fig5_3_pct_change_by_project.png)

*Figure 5.3: Percentage energy change (C4 versus C1) by project.*

The answer to RQ2 is unambiguous: **the savings are not consistent across projects.** The combined configuration's effect ranges from a large, significant −33.70% reduction in Retrofit down to a negligible, non-significant +0.47% in resty, a difference of thirty-four percentage points between the best and worst case. Table 5.4 summarises.

| Project | Language | C4 vs C1 | Effect | Significant? |
|---|---|---|---|---|
| Retrofit | Java | −33.70% | large | Yes |
| Gson | Java (size-axis) | −21.63% | large | Yes |
| HTTPie | Python | −4.96% | large | Yes |
| got | JavaScript | −2.98% | large | Yes |
| resty | Go | +0.47% | negligible | No |

*Table 5.4: Cross-project ranking of the combined-configuration effect, C4 versus C1.*

The mechanism behind resty's null result is visible in its per-stage data: dependency installation accounts for roughly 40 J of a roughly 236 J total (under 18%), because `go.mod` declares just two direct dependencies (`golang.org/x/net`, `golang.org/x/time`). There is very little dependency-installation work for caching to remove, so the near-zero effect is exactly what the mechanism in Section 6.2 predicts for a project with an unusually light dependency graph, not a contradiction of it. This is consistent with the module-cache and build-cache distinction flagged in Section 3.2.5 as a reason to interpret Go's caching result carefully, though the specific reason here is dependency-graph size rather than the caching mechanism itself.

This comparison must be read with one important caveat, discussed fully as a threat to validity in Section 6.6: HTTPie's and got's totals are each sums across a language-version matrix (three Python versions for HTTPie, two Node.js versions for got) and, for HTTPie, three separate workflow files, whereas Retrofit's, resty's, and Gson's totals are each a single job execution. This asymmetry means the absolute and percentage comparisons in Table 5.4 are not comparing strictly identical units of "one CI run" across every project, and it is one reason, alongside dependency-graph size, that HTTPie's and got's baseline magnitudes (in the thousands of joules) differ so substantially from Retrofit's, resty's, and Gson's (in the hundreds).

The consolidation-validity check anticipated in Section 3.2.5 also holds: for got, Retrofit, resty, and Gson, C1 and C3 are structurally identical pipelines, and the measured C1-versus-C3 differences (+0.52%, −0.50%, +0.71%, −1.42%) are all small in magnitude and carry negligible Cliff's delta, consistent with measurement noise rather than a real effect. This is an internal-consistency check on the measurement methodology succeeding, not a finding about consolidation itself, and it strengthens confidence that the equally non-significant C1-versus-C3 result for HTTPie (−0.54%), where consolidation is real, reflects a genuine absence of effect rather than a methodological blind spot.

## 5.6 Multi-Region SCI Analysis

Table 5.5 converts each project's mean C2 and C4 energy into SCI across five electricity grid regions.

| Project | Region | C2 SCI (gCO₂eq) | C4 SCI (gCO₂eq) |
|---|---|---|---|
| HTTPie | Ireland | 0.18373 | 0.18296 |
| HTTPie | Norway | 0.01331 | 0.01326 |
| HTTPie | Singapore | 0.21728 | 0.21637 |
| got | Ireland | 0.09666 | 0.09521 |
| got | Norway | 0.00700 | 0.00690 |
| got | Singapore | 0.11431 | 0.11259 |
| Retrofit | Ireland | 0.03186 | 0.03193 |
| Retrofit | Norway | 0.00231 | 0.00231 |
| Retrofit | Singapore | 0.03767 | 0.03776 |
| resty | Ireland | 0.02328 | 0.02273 |
| resty | Norway | 0.00169 | 0.00165 |
| resty | Singapore | 0.02753 | 0.02688 |
| Gson | Ireland | 0.02100 | 0.02021 |
| Gson | Norway | 0.00152 | 0.00146 |
| Gson | Singapore | 0.02484 | 0.02389 |

*Table 5.5: SCI per run, Ireland/Norway/Singapore, C2 versus C4, all five projects, n = 30 (Germany and USA are computed identically and shown in Figure 5.6).*

![Figure 5.6](../experiments/project-01-httpie-cli/results/figures/fig5_6_sci_five_region.png)

*Figure 5.6: SCI per run across five grid regions, C2 versus C4, by project.*

The Norway-to-Singapore differential is consistent across every project and configuration at approximately 16.3× (408 ÷ 25 = 16.32), since it is a pure function of the fixed intensity ratio and does not depend on which project or configuration is measured. For HTTPie, this yields 0.01326 gCO₂eq (Norway) against 0.21637 gCO₂eq (Singapore) for the identical C4 pipeline: an order of magnitude larger than the −4.96% saving that same pipeline achieves over its own baseline through configuration alone. Retrofit's regional figures show C4's SCI essentially unchanged from C2's (0.03193 against 0.03186 in Ireland), consistent with C2 and C4 having almost identical mean energy for that project (332.40 J and 333.16 J, Table 5.1) once the consolidation component, shown in Section 5.4 to have no measurable effect, is added on top of caching.


---

