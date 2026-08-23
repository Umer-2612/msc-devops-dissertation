# Chapter 3: Methodology

## 3.1 Research Design

Chapter 2 concluded that no existing study combines a controlled, multi-strategy comparison with a standardised carbon metric across more than one project or language (Section 2.7). Closing that gap requires a design that can attribute an observed change in energy directly to a specific configuration change, rather than to noise, project choice, or measurement drift. A quantitative experimental design, applied consistently to the same subject code across configurations, is the only way to make that attribution defensible; an observational survey of existing projects (as in Saavedra et al., 2025, or Bouzenia and Pradel, 2024) can describe adoption patterns but cannot isolate cause and effect the way this dissertation's research questions require.

This dissertation therefore adopts a quantitative experimental research design. The study is empirical: it collects measured data from real CI/CD pipeline executions rather than relying on simulation, estimation from existing datasets, or qualitative analysis. The design follows the controlled experiment approach described by Wohlin et al. (2012) for software engineering research: a baseline configuration is established, independent variables (pipeline refinement strategies) are applied one at a time, and the dependent variable (energy consumption and the derived SCI carbon score) is measured under controlled conditions for each configuration.

The study uses a within-subjects design: each project is measured under all four configurations (C1 to C4), enabling paired statistical comparisons that eliminate between-project variability as a confound.

## 3.2 Project Selection

### 3.2.1 Selection Criteria

Projects are selected from public GitHub repositories using the following inclusion criteria.

| Criterion | Requirement | Rationale |
|---|---|---|
| CI platform | GitHub Actions only | Eco-CI targets GitHub-hosted runners |
| Runner type | GitHub-hosted `ubuntu-latest` | Eco-CI's SPECpower model targets this hardware profile |
| Stars | > 500 | Indicates real-world active use |
| Last commit | Active within 3 months of study | Ensures maintained CI configuration |
| Test suite | Automated tests executing in CI | Testing is the dominant energy-consuming stage |
| Licence | MIT, Apache 2.0, BSD, or equivalent | Required for forking and workflow modification |
| Dependency manager | pip, npm, Maven, Gradle, or Go modules | Enables the caching strategy in each ecosystem |
| Build isolation | Runs on Ubuntu with no secrets, external services, browsers, or GPUs | Ensures the pipeline is reproducible and self-contained |
| No self-hosted runners | Confirmed `runs-on: ubuntu-latest` | Self-hosted runners differ in hardware profile |

*Table 3.1: Project inclusion criteria and their rationale.*

Projects are excluded where they use only scheduled (cron) triggers without push or pull-request triggers, where workflows are encrypted or Actions permissions are restricted, or where the repository is a monorepo with more than roughly twenty workflow files, whose complexity exceeds the scope of the study.

### 3.2.2 Comparison Strategy for RQ2

RQ2 asks whether the savings are consistent across languages and sizes. A naive design would compare projects that differ in both language and purpose at once, which confounds the two: any observed difference could be attributed either to the language and toolchain or to what the project actually does. To avoid this, the study separates the two axes.

The primary arm holds the application domain constant and varies only language and ecosystem. It does this by studying HTTP-client libraries, a well-defined and comparable class of project, implemented in different languages. Comparing HTTPie (Python) against a JavaScript, a Java, and a Go HTTP client isolates the effect of language and build toolchain on each strategy's effectiveness, because the projects perform the same kind of work.

A secondary arm addresses the size axis, motivated directly by the literature reviewed in Section 2.3.4: because project size does not reliably predict per-task energy on its own, and a minority of CI-intensive projects account for a disproportionate share of aggregate footprint, the effect measured on a small anchor project cannot be assumed to hold at scale. One larger project of a different type is included specifically to test whether the strategy effects hold as project size and build complexity increase. Because this project differs in domain, it is analysed as a size-axis observation rather than as part of the controlled cross-language comparison.

### 3.2.3 Selected Projects

The study applies the four-configuration protocol to all five projects below: the Python anchor, three cross-language HTTP-client parallels, and one size-axis project.

| # | Project | Language | Ecosystem / manager | Licence | Role |
|---|---|---|---|---|---|
| 1 | HTTPie CLI | Python | pip (`setup.cfg`) | BSD-3 | Anchor |
| 2 | got | JavaScript / TypeScript | npm | MIT | Cross-language parallel |
| 3 | Retrofit | Java | Gradle | Apache 2.0 | Cross-language parallel |
| 4 | resty (go-resty) | Go | Go modules | MIT | Cross-language parallel |
| 5 | Gson | Java | Maven | Apache 2.0 | Size-axis observation |

*Table 3.2: Projects selected for the study, their role, and the ecosystem exercised.*

Projects 2 to 4 are all HTTP-client libraries, matching the domain of the anchor. Each satisfies the inclusion criteria: a permissive licence, a self-contained test suite that runs on `ubuntu-latest` without external services (for example, got and Retrofit spin up local mock servers rather than calling the network), and a tagged release to pin against. Project 5, Gson, is a larger Maven multi-module Java project (24,000+ stars) selected to satisfy the size axis described in Section 3.2.2: a different domain (JSON serialisation rather than an HTTP client) and a larger, more complex build than any of the cross-language parallels. Bibliographic references for each project repository are given alongside HTTPie's in the References section.

### 3.2.4 HTTPie CLI: The Anchor Project

HTTPie CLI (https://github.com/httpie/cli) is a production-grade Python HTTP client at version 3.2.4. Its pre-study GitHub Actions configuration consists of three independent workflow files (`tests.yml`, `code-style.yml`, `coverage.yml`) that each reinstall all project dependencies from scratch on every trigger, with no caching strategy. This is representative of how mature Python open-source projects accumulate CI configuration without revisiting default behaviours over time, and it makes all three refinement strategies applicable.

For every configuration, the research workflow checks out `httpie/cli` at the fixed tag `3.2.4` externally and runs the project's own `make` targets, without modifying the project's source. This keeps the subject code frozen and identical across all four configurations, so the only variable between C1 and C4 is the pipeline configuration itself. The same fixed-tag, external-checkout approach is applied to every other project. The concrete implementation of this pattern is described in Chapter 4.

### 3.2.5 Cross-Ecosystem Considerations

Two points affect how the strategies are compared across languages, and both are reported alongside the results rather than smoothed over.

The consolidation strategy (C3) applies only to projects that ship more than one workflow file, because it merges separate workflows into one. A project whose CI is already a single workflow, such as got, has nothing to consolidate; for such a project C1 and C3 are structurally identical and only caching (C2) and the combined configuration (C4) represent genuine change. Which projects support a consolidation comparison is stated explicitly in the results.

Dependency caching (C2) is implemented with the idiomatic mechanism of each ecosystem: `cache: pip` for Python, `cache: npm` for JavaScript, `cache: gradle` or `cache: maven` for Java, and `cache: true` on `setup-go` for Go. These are not identical treatments. In particular, Go maintains a module cache (`~/go/pkg/mod`) and a build cache (`~/.cache/go-build`) as separate mechanisms, so a Go caching result is not strictly the same intervention as a pip or npm one. Cross-language caching comparisons are interpreted with this difference in mind.

## 3.3 Experiment Configurations

Four configurations are evaluated per project, summarised in Table 3.3. Each represents an independently applicable and incrementally additive refinement, chosen because it is exactly the strategy the literature review identified as under-adopted (caching, path filtering; Section 2.5.3) or entirely untested as an isolated intervention (consolidation; Section 2.6).

| Config | Structure | Dependency cache | Path filters |
|---|---|---|---|
| **C1 — Baseline** | Project's existing separate workflow files | No | None |
| **C2 — Caching** | Same files as C1 | Yes (idiomatic per ecosystem) | None |
| **C3 — Consolidation** | Separate workflows merged into one | No | None |
| **C4 — Combined** | Merged workflow + caching | Yes | Path filters defined |

*Table 3.3: The four experimental configurations and what changes between them.*

C1 establishes the baseline energy consumption of the unmodified pipeline, with only Eco-CI instrumentation added. C2 isolates dependency caching. C3 isolates workflow consolidation, merging the separate workflow files into a single sequential chain while keeping the total work identical, so that any energy difference from C1 is attributable to eliminating duplicated runner-provisioning overhead rather than to doing less work. C4 tests the combined effect of all three strategies. Path-based trigger filtering is defined as part of the combined configuration, but because all research runs are triggered manually via `workflow_dispatch` against a fixed external ref, the path filters do not fire during measurement; their real-world benefit, preventing runs entirely when only documentation changes, is treated as a construct-validity consideration rather than captured in per-run energy (Section 6.6). The exact per-project, per-ecosystem implementation of each configuration, including the specific caching keys and merge structure used for HTTPie, is presented in Chapter 4.

## 3.4 Instrumentation: Eco-CI Integration

GitHub-hosted runners are virtual machines on Microsoft Azure, and the guest environment does not expose hardware energy counters such as Intel RAPL or IPMI power sensors. Measuring energy in joules directly inside the runner is therefore not possible. Eco-CI (Section 2.5.2) was chosen over the alternatives reviewed in Chapter 2 precisely because it works around this constraint without requiring hardware access: rather than reading a physical meter, it estimates energy from processor utilisation, which the guest can read, using a regression model trained on the SPECpower benchmark dataset. This is the only approach among those surveyed in the literature review that is viable on free, shared GitHub-hosted runners, which is the infrastructure the majority of open-source maintainers actually use (Section 2.4).

Two consequences of this choice follow, and both are treated as fixed constraints on interpretation throughout this dissertation. The estimate covers processor energy only, so it excludes network and disk activity and represents a lower bound on the true energy of stages such as dependency installation, which are network-heavy. And because any systematic bias in the model applies identically to all four configurations, it does not distort the relative comparison between them, which is the concern of RQ1. Absolute values are treated as estimates throughout; the comparisons between configurations are the load-bearing results. The mechanics of the estimation, and a worked numerical example, are given in Section 4.6.

Each workflow is instrumented with the Eco-CI Energy Estimation tool (`green-coding-solutions/eco-ci-energy-estimation@v5`) at four points in every job: start-measurement at job start, get-measurement at each stage boundary, display-results at job end, and an artifact upload of the resulting JSON. The full instrumentation pattern, including the implementation requirements established during the pre-study audit, is presented in Section 4.4.

## 3.5 Data Collection Procedure

1. Each configuration is triggered via `workflow_dispatch`.
2. A minimum inter-run interval of 5 minutes is maintained to reduce shared-runner thermal and warm-up effects.
3. No code changes are committed between runs within a configuration; the subject code is a fixed external checkout.
4. Target sample size: n = 30 per configuration per project.
5. After each run completes, Eco-CI artifacts are automatically uploaded to the repository's Actions artifact store.
6. A collection script queries the GitHub Actions API, downloads all Eco-CI artifacts, and consolidates measurements into a single dataset.

The dataset schema is: `run_id`, `config`, `workflow`, `stage`, `energy_joules`, `duration_seconds`, `timestamp`, `language_version`. The full operational procedure is given in Appendix B.

## 3.6 Carbon Calculation: SCI Framework

SCI scores are computed per run per configuration using ISO/IEC 21031:2024:

```
SCI = ((E × I) + M) / R
```

Where E is total energy per run (joules, converted to kWh by dividing by 3,600,000); I is the carbon intensity of the electricity grid in gCO₂eq/kWh (Eco-CI reports 472 gCO₂eq/kWh for the Azure GitHub-hosted runner location, and the multi-region analysis additionally uses Ireland 345, Germany 350, Norway 25, USA 386, and Singapore 408); M is embodied carbon reported by Eco-CI; and R is one complete CI pipeline run, the functional unit. The result is expressed as gCO₂eq per CI run. Because R is one run, the divisor is 1 throughout, and the reported SCI figures in this dissertation are the operational component E × I; a full worked numerical example applying this formula to real measurements is given in Section 4.6.

## 3.7 Statistical Analysis

The statistical approach (normality testing, Wilcoxon signed-rank comparisons, Bonferroni correction, and Cliff's delta effect sizes) is presented together with the results it produces in Section 5.2, rather than separately here, so that the analytical method and its output can be read as one continuous account.

## 3.8 Ethical and Reproducibility Considerations

All projects studied are public open-source repositories licensed for modification. No private data, user data, or personally identifiable information is involved. All experiment code, raw data, and analysis notebooks are published in the replication package at https://github.com/Umer-2612/msc-devops-dissertation. The repository includes instructions for reproducing all measurements via `workflow_dispatch`, making the study independently verifiable.

---
