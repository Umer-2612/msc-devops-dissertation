# Chapter 6: Discussion

## 6.1 Overview

This chapter interprets the results against the three research questions, situates the findings within the literature, and examines threats to validity.

## 6.2 RQ1: Carbon Reduction per Strategy

The pilot data indicates that the dependency installation stage is the primary energy lever for caching, falling 16.8% between the C2 and C4 pilot runs, while test execution changes little (−3.5%). This is mechanistically expected: dependency installation is dominated by downloading and unpacking packages, which caching removes on a cache hit, whereas test execution is a CPU-bound workload whose energy is determined by the computation itself rather than by pipeline overhead. The direction aligns with de Medeiros et al. (2025), who identify testing as the dominant CI energy stage, and with the IEEE (2026) Java study, which isolates caching as the highest-impact single intervention. The full statistical results, once collected (Section 5.4), quantify the caching effect against the C1 baseline and, for projects with multiple workflows, isolate the consolidation effect through the C1-versus-C3 comparison.

## 6.3 RQ2: Cross-Project Consistency

The cross-language arm is designed to test whether these effects hold when only the language and toolchain change. The working hypothesis is that caching shows larger absolute savings in projects with heavier dependency-installation stages, and that consolidation shows larger savings in projects that ship more separate workflows. Because the primary-arm projects share the HTTP-client domain, differences in strategy effectiveness across them are attributable to language and ecosystem rather than to what the project does. The Go caching result is interpreted in light of the module-cache and build-cache distinction noted in Section 3.2.5, and the consolidation comparison is reported only where a project has more than one workflow to merge.

## 6.4 RQ3: Strategy Effectiveness Relative to Implementation Effort

The three strategies differ markedly in implementation cost. Caching is roughly two lines per workflow file (a `cache:` key and, where needed, a `cache-dependency-path:`), the lowest-effort intervention. Path filtering is a few lines per file, moderate effort. Consolidation is the highest effort, on the order of fifty to a hundred lines of workflow restructuring (Section 4.3). The pilot data suggests caching delivers the largest carbon saving per line of configuration changed. Path filtering's real-world saving, preventing unnecessary runs from executing at all, is not captured by the `workflow_dispatch`-based measurement but is significant for actively developed repositories. The final ranking and the recommendations for maintainers are produced once the full dataset is available.

## 6.5 The Regional Carbon Dominance Finding

The multi-region analysis (Section 5.6) shows runner location producing carbon differentials of up to 15.3× (Norway versus Singapore in the pilot data), an order of magnitude larger than any configuration optimisation measured. This places pipeline configuration within a hierarchy of interventions. For organisations with control over runner region, through self-hosted runners or enterprise regional selection, geographic placement delivers more carbon impact than any workflow change. For the majority of open-source projects using default GitHub-hosted runners without regional control, configuration refinement remains the primary actionable lever. The two are complementary: configuration reduces the work done, and regional selection reduces the carbon intensity of that work. This is consistent with Saavedra et al.'s (2025) finding that regional deployment can achieve up to 67.1% carbon reduction at the ecosystem level.

## 6.6 Threats to Validity

**Construct validity.** Eco-CI estimates CPU energy only; network and disk activity during dependency installation are not captured, so the measured caching reductions are a lower bound on the true energy savings. The functional unit of one CI run may also understate real-world savings, because path filtering prevents many runs from executing entirely (Section 3.3).

**Internal validity.** GitHub-hosted runners are shared multi-tenant infrastructure, so CPU and network variability introduce run-to-run noise; the 30-run protocol and non-parametric tests are chosen to accommodate this. The first run under a caching configuration is a cache miss and produces elevated dependency-installation energy; distributing this across 30 runs limits its influence. Because runs are triggered via `workflow_dispatch`, the path filters in C4 do not fire, so that strategy's benefit is not reflected in per-run energy.

**External validity.** The absolute values are specific to the projects studied and will not transfer to projects with much larger dependency graphs or longer test suites. The cross-language design mitigates one form of this threat by holding the domain constant, so that language and ecosystem effects are not confounded with project purpose. The directional findings (caching targets dependency installation, test execution is configuration-stable) are mechanistically grounded and are expected to generalise.

**Conclusion validity.** Non-parametric tests are appropriate given the expected non-normality of the dependency-installation distributions. The Bonferroni correction is conservative, trading power against Type I error; n = 30 provides more than 95% power for medium effect sizes at α = 0.017 (Section 5.2).

---
