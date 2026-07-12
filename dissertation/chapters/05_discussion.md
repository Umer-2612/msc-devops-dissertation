# Chapter 5: Discussion


## 5.1 Overview

This chapter interprets the results in relation to the three research questions, situates the findings within the existing literature, and examines threats to validity.

---

## 5.2 RQ1 — Carbon Reduction per Strategy

This section discusses the statistical results for each strategy (C2, C3, C4 vs C1), provides a mechanistic explanation for why each stage is or is not affected, and interprets the effect sizes in terms of practical significance.

The pilot data suggests that the dependency installation stage is the primary energy lever for caching (−16.8% in C2→C4 pilot). The test execution stage shows configuration stability (−3.5%), consistent with a CPU-bound workload whose energy cost is determined by the computation itself rather than pipeline overhead. The C3 consolidation-only data, once collected, will isolate the structural overhead reduction independently of caching.

*[Statistical results to be discussed here once 30-run data collection is complete.]*

---

## 5.3 RQ2 — Cross-Project Consistency

This section compares percentage energy reductions and Cliff's delta effect sizes across projects by programming language, project size (lines of code), and dependency graph size.

The working hypothesis is that caching will show larger absolute savings in projects with more dependencies (larger dep-install stage energy) and that consolidation will show larger savings in projects with more parallel workflows. Project characteristics (LOC, dependency count, workflow file count, test suite duration) will be used as covariates to explain variation in strategy effectiveness.

*[Cross-project analysis to be written once all project data is collected.]*

---

## 5.4 RQ3 — Strategy Effectiveness Relative to Implementation Effort

This section quantifies the implementation effort for each strategy and expresses carbon savings on a per-effort basis:

- **Caching:** 2 lines per workflow file (`cache:` + `cache-dependency-path:`) — the lowest-effort intervention
- **Path filtering:** 4–8 lines per workflow file — moderate effort
- **Consolidation:** ~50–100 lines of YAML restructuring — highest effort

The pilot data suggests caching delivers the largest carbon saving per line of YAML changed. Path filtering's real-world saving (preventing unnecessary runs entirely) is not captured in `workflow_dispatch`-based measurements but represents a significant reduction for active repositories.

*[Final ranking and recommendations to be written once all data is available.]*

---

## 5.5 The Regional Carbon Dominance Finding

> *[Write this section — it is the most striking finding from the pilot]*

The multi-region SCI analysis reveals that runner location produces carbon differentials of up to 15.3× (Norway vs Singapore in pilot data) — an order of magnitude larger than any configuration optimisation measured. This has practical implications:

1. For organisations with latitude over runner region (self-hosted runners, enterprise GitHub with regional selection), geographic optimisation delivers more carbon impact than any YAML change
2. For the majority of open-source projects using default GitHub-hosted runners without regional control, configuration refinement remains the primary actionable lever
3. The two approaches are complementary: configuration reduces the work done; regional selection reduces the carbon intensity of that work

This situates pipeline configuration refinement within a hierarchy of interventions, consistent with Saavedra et al.'s (2025) finding that regional deployment can achieve up to 67.1% carbon reduction at the ecosystem level.

---

## 5.6 Threats to Validity

### 5.6.1 Construct Validity
- Eco-CI estimates CPU energy only; network I/O during dependency installation is not captured
- Measured reductions are therefore a lower bound on actual energy savings from caching
- Functional unit (1 CI run) may understate real-world savings: path filtering prevents many runs from executing entirely

### 5.6.2 Internal Validity
- GitHub-hosted runners are shared multi-tenant infrastructure; CPU and network variability introduces run-to-run noise
- pip cache state on first run (cache miss) produces elevated dep-install energy; the 30-run protocol distributes this effect across the sample
- `workflow_dispatch` bypasses `paths:` filters; C4's trigger filtering benefit is not captured in per-run energy measurements

### 5.6.3 External Validity
- HTTPie CLI represents one Python project archetype; absolute values will not transfer to projects with larger dependency graphs or longer test suites
- The directional findings (caching targets dep-install, test execution is configuration-stable) are mechanistically grounded and expected to generalise
- Java, Go, and JavaScript projects may show different caching efficiency characteristics

### 5.6.4 Conclusion Validity
- Non-parametric tests (Wilcoxon) are appropriate given expected non-normality of dep-install distributions
- Bonferroni correction is conservative; it reduces Type I error at the cost of reduced power for detecting small effects
- n = 30 provides >95% power for medium effect sizes at α = 0.017
