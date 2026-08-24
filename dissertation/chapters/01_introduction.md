# Chapter 1: Introduction

## 1.1 Purpose

The purpose of this dissertation is to empirically measure and compare the carbon impact of three Continuous Integration and Continuous Deployment (CI/CD) pipeline refinement strategies across open-source projects hosted on GitHub. The three strategies under investigation, dependency caching, workflow consolidation, and path-based trigger filtering, are individually documented in professional practice but have never been systematically compared against each other in a controlled experiment using standardised carbon measurement. This work applies the Software Carbon Intensity (SCI) specification (ISO/IEC 21031:2024) and the Eco-CI energy estimation tool to produce evidence-based recommendations for open-source maintainers seeking to reduce the environmental footprint of their build pipelines.

## 1.2 Background

### 1.2.1 The Energy Cost of Software Infrastructure

Software development infrastructure has grown substantially in both scale and environmental consequence. The International Energy Agency reported that global data centre electricity consumption exceeded 460 TWh in 2022 and is projected to grow further as cloud-native and AI workloads expand (IEA, 2023). Masanet et al. (2020) document that while improvements in hardware efficiency historically offset growing workload volumes, this balance is increasingly under pressure; the efficiency gains of previous decades cannot be assumed to continue indefinitely.

Within this broader cloud infrastructure footprint, Continuous Integration and Continuous Deployment pipelines represent a significant and largely unexamined source of energy consumption. These pipelines, which build, test, and validate software on every code change, execute on cloud virtual machines that are provisioned, run, and discarded with each trigger event. A moderately active open-source repository may generate tens of thousands of workflow runs per year. Alves et al. (2024) characterise this as the "software frugality" problem: as DevOps practices democratise CI/CD through platforms such as GitHub Actions and GitLab CI, the aggregate energy cost of automated pipelines across millions of repositories becomes environmentally significant, yet remains largely invisible to the developers who configure them.

At ecosystem scale, Saavedra, Mendes and Ferreira (2025) estimate the carbon footprint of the entire GitHub Actions ecosystem in 2024 at between 150.5 and 994.9 metric tonnes of CO₂ equivalent (MTCO₂e), with a most likely scenario of 456.9 MTCO₂e. This is the equivalent of the annual electricity consumption of thousands of homes, produced by automated pipelines that most developers have never audited for environmental efficiency.

Taken together, these figures establish that CI/CD is not a peripheral cost of software delivery but a growing and largely invisible line item in the environmental footprint of the software industry, one that scales directly with how often, and how wastefully, pipelines are triggered. That framing motivates the next question: not whether CI/CD carries an energy cost, but why that cost is so much higher than the work being performed requires.

### 1.2.2 Systemic Inefficiency in CI/CD Configuration

The energy cost of CI/CD pipelines is not primarily a consequence of the work performed (tests must run, code must be compiled) but of how pipelines are configured to perform that work. Three patterns account for much of the excess consumption.

**Unconditional dependency reinstallation.** GitHub-hosted runners are ephemeral: every new job starts with a clean virtual machine and must reinstall all project dependencies from scratch. Without explicit caching, a project that runs 50 builds per day reinstalls the same set of packages 50 times, each time consuming network bandwidth and CPU cycles for identical download-and-install operations. Bouzenia and Pradel (2024) found that only 32.9% of GitHub Actions repositories had enabled dependency caching, despite its availability as a first-class feature.

**Fragmented multi-workflow structures.** Mature open-source projects commonly accumulate separate workflow files for testing, linting, and coverage, each of which independently provisions a runner, checks out the full repository, and installs all dependencies. When these stages are structurally independent, the shared setup cost is duplicated for every parallel workflow. Consolidating them into a sequential or partially-parallel single workflow eliminates this duplication.

**Unrestricted trigger events.** A push event on a CI/CD pipeline without path-based filtering triggers a full test suite execution regardless of whether the changed files are relevant to the build. Editing a documentation file or updating a README triggers the same runner provisioning, dependency installation, and test execution as a substantive code change. Bouzenia and Pradel (2024) find that only 20.7% of repositories apply path-based filtering to reduce unnecessary executions.

These patterns are not the product of deliberate decisions to consume energy; they reflect engineering choices made without visibility into their environmental consequences. Pinto and Castor (2017) observe that energy efficiency has historically been treated as a concern for embedded or high-performance computing, not for the typical application developer. Engineers who routinely optimise query latency and memory footprint have no equivalent instinct or toolchain for measuring what a git push costs the planet.

The three patterns identified here, unconditional reinstallation, fragmented workflows, and unrestricted triggers, are the practical target of this dissertation's three refinement strategies. Each maps directly onto one of the four experimental configurations introduced in Chapter 3: dependency caching addresses the first pattern, workflow consolidation the second, and path-based filtering the third, with a fourth configuration combining all three.

### 1.2.3 The Measurement and Regulatory Gap

Three developments make the measurement of CI/CD carbon impact both feasible and timely.

First, the Green Software Foundation published the Software Carbon Intensity (SCI) specification in 2022, subsequently adopted as ISO/IEC 21031:2024 (Green Software Foundation, 2024). The SCI standard provides a reproducible, standardised formula (SCI = ((E × I) + M) / R) for expressing the carbon intensity of a unit of software functionality. It is designed to be comparable across different software systems and measurement contexts, enabling like-for-like comparison of pipeline configurations.

Second, the Eco-CI Energy Estimation tool (Green Coding Solutions, 2023) makes energy measurement inside cloud CI environments practically achievable. GitHub-hosted runners do not expose hardware-level energy counters; Eco-CI addresses this by using a machine learning model trained on the SPECpower database to estimate energy consumption from CPU utilisation data, producing per-stage energy measurements in joules without requiring physical instrumentation. A 2026 IEEE study applying this class of tool to 204 open-source Java projects found that enabling dependency caching reduced CI energy consumption by 30% on average for Maven projects and by over 90% in some Gradle cases, directly validating caching as a high-impact intervention (IEEE, 2026).

Third, the EU Corporate Sustainability Reporting Directive (CSRD), effective from January 2024, requires large organisations to disclose Scope 3 emissions, a category that includes cloud infrastructure usage (European Commission, 2022). As sustainability reporting obligations mature, the energy cost of CI/CD pipelines will increasingly appear in corporate carbon accounts. This regulatory pressure creates organisational incentives for pipeline efficiency that complement the environmental motivation.

Despite these developments, a critical gap remains. No existing study has experimentally applied and compared multiple CI/CD pipeline refinement strategies across diverse real-world projects using standardised carbon measurement. Saavedra et al. (2025) estimate ecosystem-scale footprints but provide no project-level guidance. Bouzenia and Pradel (2024) document optimisation adoption rates and estimate VM time savings, but do not translate these into carbon units. Claßen et al. (2023) demonstrate carbon-aware temporal scheduling but do not evaluate pipeline configuration changes. Alamer and Alharbi (2025) systematically review the literature and identify the absence of empirical comparative data as the primary gap. That is the gap this dissertation fills.

The standard, the tool, and the regulatory pressure now each exist independently, but no study has put all three together to test, in a controlled way, which specific pipeline changes are actually worth making, and by how much.

### 1.2.4 Problem Statement

The result is a persistent gap between what is now measurable and what is actually known. Pipelines continue to reinstall dependencies, run fragmented workflows, and trigger on irrelevant changes (Section 1.2.2), not because these inefficiencies are unknown in principle, but because no study has quantified their carbon cost in a way a maintainer can act on. The instruments needed to close this gap exist (Section 1.2.3), yet nobody has applied them systematically, across more than one project and more than one strategy, using a standardised metric that permits genuine comparison. The problem this dissertation addresses is therefore concrete: open-source maintainers who want to reduce the carbon footprint of their CI/CD pipelines currently have no evidence-based way to decide which of several plausible configuration changes is worth making first, or whether that decision even holds outside the specific project where a saving happens to have been observed.

## 1.3 Research Questions

This dissertation is organised around three research questions, each designed to address a distinct dimension of the pipeline carbon measurement problem:

**RQ1:** What carbon reduction does each of the three pipeline refinement strategies (dependency caching, workflow consolidation, and path-based trigger filtering) produce compared to an unrefined baseline in real open-source GitHub Actions projects?

**RQ2:** Do the carbon savings from these refinement strategies remain consistent across projects of different sizes, programming languages, and build complexities, or does the effectiveness of each strategy vary by project type?

**RQ3:** Which refinement strategy produces the largest measured carbon reduction relative to implementation effort, and what evidence-based recommendations can be developed for open-source maintainers?

RQ1 establishes whether individual strategies produce measurable, statistically significant carbon reductions. RQ2 tests whether findings from one project type generalise to others, and is addressed with a design that holds the application domain constant while varying language and ecosystem (Section 3.2). RQ3 synthesises the comparative evidence into actionable recommendations, accounting for both the magnitude of carbon saving and the implementation cost of each strategy.

### 1.3.1 Objectives

To answer the research questions above, this dissertation pursues the following objectives:

- Instrument four progressively refined GitHub Actions pipeline configurations, baseline, caching, consolidation, and combined, with the Eco-CI energy estimation tool across a set of real open-source projects.
- Convert the measured energy consumption of each configuration into a standardised carbon figure using the Software Carbon Intensity (SCI) specification (ISO/IEC 21031:2024).
- Statistically compare each refinement strategy against the unrefined baseline to establish which produce a measurable and significant carbon reduction (addressing RQ1).
- Assess whether the magnitude and direction of each strategy's effect holds across projects of different programming languages and sizes (addressing RQ2).
- Rank the three strategies by carbon saved per unit of implementation effort and translate that ranking into evidence-based recommendations for maintainers (addressing RQ3).

### 1.3.2 Main Contributions

This dissertation is expected to make the following contributions, confirmed in full once the complete dataset is analysed (Chapter 7):

1. The first multi-strategy, cross-project empirical comparison of CI/CD pipeline refinement strategies under a standardised carbon metric (SCI / ISO/IEC 21031:2024).
2. A replicable green CI/CD audit methodology, comprising an Eco-CI instrumentation pattern, a pre-study audit checklist, data-collection scripts, and analysis notebooks, published as an open replication package.
3. A cross-language experimental design that isolates language and ecosystem effects from application purpose by holding the HTTP-client domain constant across the projects studied.
4. Evidence-based, effort-weighted recommendations for open-source maintainers on which pipeline configuration change is worth making first.
5. A multi-region SCI analysis quantifying the carbon impact of runner geographic location relative to configuration-level optimisation.

## 1.4 Scope and Limitations

This dissertation focuses on GitHub Actions as the CI/CD platform and restricts analysis to publicly available open-source repositories hosted on GitHub. The study examines pipeline-level configuration changes only; it does not address test-suite restructuring, application-level code optimisation, or infrastructure-level interventions such as geographic runner selection or temporal scheduling. Carbon measurement is performed using Eco-CI for energy estimation and the SCI specification for carbon intensity calculation; the inherent limitations of model-based energy estimation in shared cloud environments are acknowledged and addressed in the Methodology chapter.

The scope is bounded to the three refinement strategies identified from the literature as having both documented adoption precedent and plausible energy impact: dependency caching, workflow consolidation, and path-based trigger filtering. Strategies requiring non-standard infrastructure, such as self-hosted runners or private registries, are excluded to ensure reproducibility.

## 1.5 Report Outline

- **Chapter 2 (Literature Review)** surveys the literature across four thematic areas and identifies the specific contribution this dissertation makes.
- **Chapter 3 (Methodology)** describes the research design and the reasoning behind it: the rationale for a controlled, within-subjects experiment; project selection criteria; the four experimental configurations at a conceptual level; the SCI carbon-calculation framework; the data collection procedure; and the ethical and reproducibility considerations.
- **Chapter 4 (Design)** presents the concrete technical implementation that realises the methodology: the pipeline architecture for each configuration, the Eco-CI instrumentation pipeline, the measurement stage boundaries, and a worked example of the SCI calculation, illustrated with diagrams.
- **Chapter 5 (Results)** sets out the statistical analysis approach, then presents the energy and carbon measurements for each project and configuration: descriptive statistics, significance tests, SCI scores, and the multi-region carbon intensity analysis.
- **Chapter 6 (Discussion)** interprets the findings in relation to the three research questions, compares results to prior literature, and identifies the principal threats to validity.
- **Chapter 7 (Conclusion)** confirms the contributions of the dissertation, states the practical recommendations for open-source maintainers, acknowledges the limitations of the study, and identifies directions for future work.

---

