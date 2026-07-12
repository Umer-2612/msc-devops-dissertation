# MSc Dissertation — Literature Review & Topic Refinement
# Supervisor Meeting Preparation Document

**Student:** Umer Karachiwala (L00196895)  
**Course:** M.Sc. in DevOps, Atlantic Technological University  
**Date:** 23 June 2026  
**Meeting Purpose:** Present refined topic, literature review progress, and gap analysis

---

# PART 1: REFRAMED DISSERTATION TOPIC

## Proposed Title

**Greening the Pipeline: An Empirical Comparison of CI/CD Refinement Strategies and Their Carbon Impact Across Open-Source Projects**

### Key Language Changes from Original Proposal

| Original Phrasing | Revised Phrasing | Rationale |
|---|---|---|
| "Optimisation strategies" | "Refinement strategies" | "Optimisation" implies finding the best/optimal solution. We are *comparing* strategies empirically, not claiming optimality. |
| "How much do strategies reduce carbon emissions" | "What carbon reduction does each strategy produce" | Avoids implying we will find maximum possible reduction |
| "Greatest carbon reduction per unit of effort" | "Most substantial measured reduction relative to implementation effort" | Careful framing — we report what we measure, not what is "best" |
| "Highest carbon return" | "Largest measured carbon savings" | Removes investment-style language that overclaims |
| "Derive practical guidelines" | "Develop evidence-based recommendations" | Guidelines imply authority; recommendations reflect empirical contribution |
| "Optimised baseline" | "Refined configuration" | Consistent terminology |

### Rationale for These Changes

The word "optimise" (and its variants) carries mathematical and engineering connotations of finding an optimal — i.e., the best possible — solution. In operations research, "optimisation" has a precise meaning: finding the maximum or minimum of a function subject to constraints. Our dissertation does **not** solve an optimisation problem. We **empirically compare** the carbon impact of several pipeline refinement strategies across a sample of projects. What we find is descriptive and comparative, not optimal. Using "refinement" or "improvement" is more accurate and defensible.

Similarly, we must avoid claiming our results are generalisable beyond the projects we study. We can say our findings "suggest" or "indicate" patterns, not that they "prove" or "establish" universal truths. Every claim must be grounded in what we actually measure.

---

# PART 2: RESEARCH PAPERS REVIEWED

## Category A: Ecosystem-Level and Large-Scale Measurement Studies

---

### Paper 1: Saavedra, Mendes & Ferreira (2025)
**Full Title:** Environmental Impact of CI/CD Pipelines  
**Authors:** Nuno Saavedra, Alexandra Mendes, Joao F. Ferreira  
**Affiliations:** INESC-ID/IST (University of Lisbon); INESC TEC (University of Porto)  
**Venue:** arXiv preprint 2510.26413v2, October 2025  
**Direct Download:** https://arxiv.org/pdf/2510.26413 (Open Access — Verified)  
**Dataset DOI:** https://doi.org/10.5281/zenodo.16619699

**Summary:**  
This paper estimates the carbon and water footprints of the entire GitHub Actions ecosystem for 2024. The authors build upon the Cloud Carbon Footprint (CCF) framework and extend it with water footprint calculations. The dataset comprises 2,226,729 workflow runs (3,446,572 jobs) from 18,683 public repositories. The reported carbon footprint for 2024 ranges from 150.5 MTCO2e (optimistic — Norway West) to 994.9 MTCO2e (pessimistic — India), with the most likely scenario at 456.9 MTCO2e. The corresponding water footprint most likely scenario is 5,738.2 kiloliters. The authors propose mitigation strategies including deploying runners in low-carbon regions (up to 67.1% reduction), temporal shifting of scheduled runs (3.9% reduction), and reducing repository sizes. The Software Carbon Intensity Specification of the Green Software Foundation is cited as the governing standard.

**Identified Gaps:**
- Ecosystem-level estimation only — no actionable project-level guidance
- No comparison of refinement strategies (caching, consolidation, filtering) across projects
- Resource usage estimated, not directly measured (only 6.5% of workflows successfully re-executed)
- No longitudinal analysis — single-year snapshot
- Limited to GitHub Actions public repositories
- Regional deployment uncertain — GitHub does not officially disclose runner locations

**How Our Dissertation Addresses These Gaps:**  
Where Saavedra et al. estimate ecosystem footprint from aggregated data, we trace causal links between specific pipeline configuration changes and carbon reduction for individual projects. We apply and compare specific refinement strategies (caching, job consolidation, trigger filtering) across multiple real-world projects, producing meso-level evidence that developers can act upon. Our work complements their macro-level findings with project-level measurements.

---

### Paper 2: de Medeiros, Lefeuvre, Combemale & Perez (ICT4S 2025)
**Full Title:** Evaluating the Energy Profile of Tasks Managed by Build Automation Tools in Continuous Integration Workflows  
**Authors:** Sergio Queiroz de Medeiros, Romain Lefeuvre, Benoit Combemale, Quentin Perez  
**Affiliations:** Federal University of Rio Grande do Norte (Brazil); INRIA/IRISA (France)  
**Venue:** ICT4S 2025, Dublin, Ireland  
**Direct Download:** https://hal.science/hal-05090865v1/file/Evaluating_the_energy_profile_Maven_Gradle_Queiros_de_Medeiros_etal_2025.pdf (Open Access — Verified, 740 KB, CC BY 4.0)  
**DOI:** 10.1109/ICT4S68164.2025.00011

**Summary:**  
This paper investigates the energy consumption profile of tasks managed by Apache Maven and Gradle within GitHub Actions CI workflows. The dataset comprises 1,167 CI workflows from popular Java projects, yielding 183,355 analysed tasks. Energy measurement was performed via SmartWatts with hardware performance counters at 2 Hz. Key findings: Maven/Gradle tasks represent 24-28% of total CI workflow energy; testing-related tasks consume the most energy (47% for Maven, 36% for Gradle); project size does not strongly predict energy consumption per task (Cliff's Delta predominantly "negligible"). The authors acknowledge that only CPU energy is captured; RAM, disk, and network are excluded.

**Identified Gaps:**
- Profiling without intervention — characterises energy but does not test whether any strategy reduces it
- No carbon translation — energy in joules only, no CO2e conversion
- Limited to Java/Maven/Gradle ecosystems
- No across-project comparison of pipeline configurations
- Clean-environment execution deliberately lacks caching (worst-case scenarios only)
- Single hardware configuration (Dell Xeon workstation)

**How Our Dissertation Addresses These Gaps:**  
Where de Medeiros et al. profile energy consumption statically, we apply specific refinement strategies and measure before-and-after energy and carbon differences across multiple projects. We translate energy savings into CO2e using grid carbon intensity data. By including projects in multiple languages and build systems, we test whether their Java-specific findings generalise. By measuring with and without caching, we quantify the real-world energy reduction that caching provides — the "future work" they identify.

---

### Paper 3: Berger-Levrault Research (2024)
**Full Title:** CI/CD Pipelines: Good Software Development Practice, But Green?  
**Author:** Boubou Thiam Niang  
**Affiliation:** Berger-Levrault (software company, France/Canada)  
**Venue:** BL Research blog, September 2024  
**Direct Link:** https://www.research-bl.com/ci-cd-pipelines-good-software-development-practice-but-green/ (Verified)

**Summary:**  
This study examines CI/CD pipeline energy consumption by varying three parameters — CI platform (GitHub Actions vs GitLab CI/CD), programming language (Java vs Python), and build tool — using a single small-scale application (455 LOC, 3 classes). Energy is estimated using Eco-CI. Key findings: GitHub Actions averaged 13.36 joules per execution vs GitLab's 21.81 joules; Java averaged 11.36 joules vs Python's 14.62 joules. The authors acknowledge the study is based on a single small-scale project and larger-scale projects require further study.

**Identified Gaps:**
- Single tiny project (455 LOC) — no generalisability
- No refinement strategy comparison — only platform and language differences
- Eco-CI estimation vs. direct measurement (no ground truth validation)
- Build stage only — excludes testing and deployment (the dominant energy consumers)
- No statistical analysis (23 iterations per scenario, but no tests applied)
- No carbon-to-action translation for developers

**How Our Dissertation Addresses These Gaps:**  
We study multiple real-world projects of varying sizes and complexity, addressing their explicit call for "further experiments on larger-scale projects." Where they compare platforms, we compare refinement strategies. Where they exclude deployment, we include full pipeline assessments. Where they rely solely on Eco-CI estimation, we cross-validate with multiple measurement approaches. Our work extends their platform-comparison question into a configuration-comparison answer.

---

## Category B: Optimisation and Strategy Studies

---

### Paper 4: Bouzenia & Pradel (ICSE 2024)
**Full Title:** Resource Usage and Optimization Opportunities in Workflows of GitHub Actions  
**Authors:** Islem Bouzenia, Michael Pradel  
**Affiliation:** University of Stuttgart, Germany  
**Venue:** ICSE 2024, Lisbon, Portugal  
**Direct Download (Preprint):** https://software-lab.org/publications/icse2024_workflows.pdf (Open Access — Verified, full 12 pages)  
**ACM DL:** https://dl.acm.org/doi/10.1145/3597503.3623303 (Paywalled)  
**Dataset:** 952 repos, 1.3M workflow runs, 3.7M jobs, 34.3M steps

**Summary:**  
The first comprehensive empirical study of computational resource usage in GitHub Actions workflows. Key findings: paid-tier repos consume ~$504/year; 91.2% of resources consumed by testing/building; pull requests (50.7%), pushes (30.9%), and scheduled events (15.5%) account for 97.1% of VM time. Six optimisations studied: caching (32.9% adoption, -3.4% VM time), fail-fast (75.9% adoption, -1.5%), cancel-in-progress (10.1%, -4.1%), skip workflow (9.7%), filtering target files (20.7%), and custom timeout (14.0%, -8.1%). The paper identifies that deactivating scheduled workflows on inactive repos could reduce execution time by 1.1-31.6%.

**Identified Gaps:**
- **No carbon or energy measurement** — VM time and cost only, not environmental impact
- Optimisation impact is estimated via before-after comparison, not experimentally validated
- No comparison of strategies against each other for different project types
- No ranking by effectiveness per unit of implementation effort
- 30.7% of jobs unclassified in name-based analysis

**How Our Dissertation Addresses These Gaps:**  
Our dissertation directly addresses the carbon measurement gap by applying the SCI standard to quantify the carbon emissions of specific pipeline refinement strategies. Unlike Bouzenia and Pradel's estimated approach, we experimentally implement and measure caching, workflow consolidation, and path-based trigger filtering on actual repositories, providing ground-truth carbon reduction data. By comparing strategies across diverse project types, we fill the comparative analysis gap they identify as future work.

---

### Paper 5: Claßen et al. (2023/2024)
**Full Title:** Carbon-Awareness in CI/CD  
**Authors:** Henrik Claßen, Jonas Thierfeldt, Julian Tochman-Szewc, Philipp Wiesner, Odej Kao  
**Affiliation:** Technical University Berlin, Germany  
**Venue:** ICSOC 2024 Workshops (arXiv 2310.18718, October 2023)  
**Direct Download:** https://arxiv.org/pdf/2310.18718 (Open Access — Verified, full 12 pages)

**Summary:**  
This paper discusses opportunities for reducing CI/CD carbon footprint by aligning execution with periods of low-carbon energy availability. The authors propose a system architecture for carbon-aware CI/CD services. Evaluation uses 7,392 workflow executions from ten popular GitHub repositories combined with carbon intensity data from WattTime covering 12 regions. Results: location shifting alone achieves 25.31% carbon reduction; adding user-provided deadlines yields up to ~31.2% total reduction. The authors acknowledge their simulation uses estimated durations closely matching actual runtimes, which may not reflect real-world conditions.

**Identified Gaps:**
- Single strategy focus: temporal and spatial scheduling only
- Simulation-based, not real deployment
- Limited to ten repositories — may not represent diversity
- No dependency information between workflow steps
- Results are relative carbon intensity reductions, not absolute grams CO2e
- Does not evaluate pipeline configuration changes (caching, consolidation, filtering)

**How Our Dissertation Addresses These Gaps:**  
Our dissertation complements Claßen et al.'s temporal scheduling by examining an orthogonal class of optimisations: pipeline configuration refinements that reduce total work performed. While they ask "when and where should we run this job?", we ask "can we run fewer jobs, or run them more efficiently?". By measuring caching, consolidation, and trigger filtering across multiple projects, we provide the cross-project comparative analysis they do not perform. Combining both approaches represents a more complete solution.

---

### Paper 6: Kruglov, Succi & Vasuez (2021)
**Full Title:** Incorporating Energy Efficiency Measurement into CI/CD Pipeline  
**Authors:** Artem Kruglov, Giancarlo Succi, Xavier Vasuez  
**Affiliation:** Innopolis University, Russia  
**Venue:** 2nd European Symposium on Software Engineering (ESSE 2021)  
**Direct Download (ACM eReader):** https://dl.acm.org/doi/epdf/10.1145/3501774.3501777 (Free access — Verified)

**Summary:**  
This paper presents a method and tool (Innometrics framework) linking static code analysis with energy efficiency measurement. The approach defines custom energy efficiency metrics including EE_m (per class), EE_struct (structural coefficient), and EE_sp_j (per story point). A preliminary evaluation on a single project showed story points correlate strongly with energy (r=0.998). The approach is tightly coupled to SonarQube and macOS Data Collector on Intel hardware.

**Identified Gaps:**
- Extremely small, preliminary dataset on a single project
- Tightly coupled to SonarQube and Innometrics framework
- CPU-only measurement, single platform (macOS), single Intel CPU
- Object-oriented metrics bias — may not apply to non-OO languages
- No comparison across projects or strategies
- Relative measurement only — cannot compare absolute efficiency across codebases

**How Our Dissertation Addresses These Gaps:**  
We work with diverse real-world open-source projects using standard GitHub Actions runners (Linux-based, the dominant CI/CD platform). Where they measure energy efficiency correlation with code metrics on one project, we measure the actual carbon impact of specific CI/CD configuration changes across multiple projects, providing actionable recommendations that do not require proprietary frameworks.

---

## Category C: Standards, Tools, and Systematic Reviews

---

### Paper 7: Green Software Foundation — SCI Specification
**Full Title:** Software Carbon Intensity (SCI) Specification  
**Source:** Green Software Foundation Standards Working Group  
**Standard:** ISO/IEC 21031:2024 (published March 2024)  
**Formula:** SCI = ((E x I) + M) / R  
**Links:**
- Specification: https://sci.greensoftware.foundation/ (Verified)
- GitHub: https://github.com/Green-Software-Foundation/sci (Verified, 293 stars)
- ISO: https://www.iso.org/standard/86612.html (Verified)

**Summary:**  
The SCI specification defines a standardised methodology for calculating the rate of carbon emissions for a software system. E = energy consumed, I = location-specific carbon intensity, M = embodied carbon of hardware, R = functional unit. SCI is a score (lower is better; zero is impossible). The standard is applicable from large cloud systems to small libraries. It explicitly excludes offsets and neutralisation credits from SCI reduction claims. The specification became ISO/IEC 21031:2024 in March 2024.

**Identified Gaps:**
- Measurement framework only — provides the "how to measure" but not "what to measure" or "which choices reduce emissions"
- No CI/CD-specific guidance beyond general advice to create "carbon-aware pipelines"
- Functional unit selection for CI/CD pipelines is not explored
- No validation study demonstrating reliable, reproducible results across CI environments
- Embodied carbon data (M) is difficult to obtain in shared CI environments

**How Our Dissertation Uses/Builds Upon This:**  
Our dissertation adopts SCI as the primary measurement framework for calculating carbon intensity of CI/CD pipeline runs. We provide one of the first empirical applications of ISO/IEC 21031:2024 to CI/CD environments, systematically measuring how specific configuration changes affect the SCI score of real projects. Our work demonstrates both the applicability and practical limitations of using SCI in shared CI environments.

---

### Paper 8: Alamer & Alharbi (2025)
**Full Title:** Sustainable DevOps: A Systematic Literature Review on Reducing Energy Footprint in Continuous Integration and Deployment (CI/CD) Pipelines  
**Authors:** Rand Alamer, Ohoud Alharbi  
**Affiliation:** King Saud University, Saudi Arabia  
**Venue:** International Journal of Computations, Information and Manufacturing (IJCIM), Vol. 5, No. 2, 2025  
**Direct Download (PDF):** https://journals.gaftim.com/index.php/ijcim/article/download/565/338/1583 (Open Access — Verified)  
**DOI:** https://doi.org/10.54489/ijcim.v5i2.565

**Summary:**  
This systematic literature review analyses 50 studies published 2020-2025 on sustainability in DevOps. Key findings: a clear methodological shift from hardware-based profiling (RAPL) to ML prediction models; persistent practical challenges include limited visibility into energy metrics, overly triggered pipelines, and organisational priorities favouring speed over sustainability. Three main technique categories identified: carbon-aware scheduling, test-suite optimisation, and lightweight build strategies. The review concludes by highlighting the need for clearer frameworks integrating sustainability into CI/CD design.

**Identified Gaps:**
- No original empirical data — synthesises findings but conducts no new experiments
- No cross-project comparison of strategies
- Limited standardised measurement across the 50 reviewed studies
- No validation of ML-based estimation tools in CI environments
- Practical guidance absent — no actionable recommendations for practitioners

**How Our Dissertation Uses/Builds Upon This:**  
Where Alamer and Alharbi catalogued techniques from the literature, our work implements and measures multiple pipeline refinement strategies across diverse real-world projects, producing original empirical data that the review explicitly calls for. We use a standardised measurement approach (Eco-CI combined with SCI) enabling meaningful comparison across projects. Our findings provide the evidence-based guidance the review identified as missing.

---

### Paper 9: Eco-CI Energy Estimation Tool
**Full Name:** Eco-CI Energy Estimation  
**Source:** Green Coding Solutions GmbH, Berlin, Germany  
**Type:** Open-source measurement tool (GitHub Action / GitLab plugin)  
**Links:**
- GitHub Repository: https://github.com/green-coding-solutions/eco-ci-energy-estimation (Verified, 111 stars, MIT license)
- Documentation: https://www.green-coding.io/blog/eco-ci-energy-estimation/ (Verified)
- Live Dashboard: https://metrics.green-coding.io/ci-index.html (Verified)
- Case Study: https://www.green-coding.io/case-studies/carbon-cost-of-testing-pipelines/ (Verified)

**Summary:**  
Eco-CI is an open-source tool for estimating energy consumption in CI environments. It uses an XGBoost ML model trained on the SPECPower database to estimate energy from CPU utilisation data. The tool outputs energy in Joules, average power in Watts, and estimated CO2 equivalent. Since shared CI runners do not provide access to hardware-level energy counters (RAPL), Eco-CI provides a practical alternative. The tool was referenced by GitHub in their "10 best tools to green your software" blog post. Current version: v5.3.0 (April 2026).

**Identified Gaps:**
- Estimation, not direct measurement — ML model has known limitations (idle power, memory-heavy workloads)
- No strategy comparison framework — measures without comparing or advising
- Limited validation against ground truth in actual CI environments
- Opaque hardware in shared environments — GitHub can change runner hardware without notice
- Does not prescribe which strategies to apply or quantify trade-offs

**How Our Dissertation Uses/Builds Upon This:**  
We use Eco-CI as the primary measurement instrument for collecting energy consumption data. We apply Eco-CI to measure baseline energy and re-measure after applying refinement strategies, enabling before-and-after comparison. By combining Eco-CI's energy estimates with SCI's carbon intensity calculation, we produce standardised carbon scores for each pipeline configuration. Our work extends Eco-CI from passive measurement to active experimental instrumentation.

---

# PART 3: GAP ANALYSIS MATRIX

## Cross-Paper Comparison Table

| Dimension | Saavedra et al. (2025) | de Medeiros et al. (2025) | Berger-Levrault (2024) | Bouzenia & Pradel (ICSE 2024) | Claßen et al. (2023) | Kruglov et al. (2021) |
|---|---|---|---|---|---|---|
| **Scale** | Ecosystem (2.2M runs, 18K repos) | Large (1,167 workflows, 183K tasks) | Single tiny project (455 LOC) | Large (952 repos, 1.3M runs) | Medium (7,392 execs, 10 repos) | Single project |
| **What is measured** | Carbon & water footprint | Per-task CPU energy (joules) | Platform/language energy (joules) | VM time and monetary cost | Relative carbon intensity | Relative energy efficiency |
| **Intervention tested** | None — observational | None — profiling only | None — comparison only | None — retrospective | None — simulation | None — demonstration |
| **Strategies compared** | None | None | None | 6 strategies (adoption only) | 1 strategy (scheduling) | None |
| **Carbon measured** | Yes (ecosystem level) | No (joules only) | Yes (estimated) | No | Yes (relative) | No |
| **Uses SCI standard** | Cited | No | No | No | No | No |
| **Multiple projects** | 18,683 repos | 1,167 workflows | 1 project | 952 repos | 10 repos | 1 project |
| **Multiple strategies** | No | No | No | Yes (descriptive) | No | No |
| **Build/test/deploy** | All via execution time | Build + test only | Build only | All stages | All stages | Not specified |
| **Actionable guidance** | Indirect (high-level) | Limited (test is high) | Limited | Moderate (adoption rates) | Limited (scheduling only) | None |

## The Unified Gap: What NO Existing Paper Does

**No existing study systematically applies and compares multiple CI/CD pipeline refinement strategies across diverse real open-source projects while measuring actual carbon impact using a standardised methodology.**

Each paper addresses a piece of the puzzle:
- **Saavedra et al.** tell us the ecosystem-scale problem exists (456.9 MTCO2e) but not what individual projects should do
- **de Medeiros et al.** tell us which tasks consume the most energy (testing) but not how to reduce that consumption
- **Berger-Levrault** compares platforms but not configurations, and at too small a scale to generalise
- **Bouzenia & Pradel** tell us which optimisations are adopted and their estimated VM time impact, but not their carbon impact
- **Claßen et al.** show temporal shifting helps (~31% reduction) but do not evaluate pipeline configuration changes
- **Kruglov et al.** provide a measurement method but evaluate it on a single project with limited generalisability
- **SCI** provides the measurement standard but no empirical data
- **Alamer & Alharbi** catalogue techniques but produce no original measurements
- **Eco-CI** provides the measurement tool but no comparison framework

**Our dissertation occupies the intersection:** we use SCI (Paper 7) as the framework, Eco-CI (Paper 9) as the instrument, and apply the techniques catalogued by Alamer & Alharbi (Paper 8) to conduct the first experimental, cross-project comparison of pipeline refinement strategies with standardised carbon measurement.

---

# PART 4: HOW OUR DISSERTATION FILLS THE GAP

## Unique Contribution Statement

This dissertation conducts the first empirical study that:

1. **Selects multiple real-world open-source projects** spanning different languages, sizes, and build complexities (6-8 projects)
2. **Applies four specific, reproducible refinement strategies** — baseline, dependency caching, workflow consolidation, and path-based trigger filtering — under controlled conditions
3. **Measures energy consumption and carbon emissions** using Eco-CI (energy estimation) and the SCI specification (carbon intensity standard)
4. **Compares strategies both individually and in combination** across all selected projects
5. **Analyses whether project characteristics** (size, language, build complexity) influence the effectiveness of each strategy
6. **Develops evidence-based recommendations** for open-source maintainers on which strategies produce the largest measured carbon reductions

## Research Questions (Revised Wording)

**RQ1:** What carbon reduction does each of three pipeline refinement strategies — dependency caching, workflow consolidation, and path-based trigger filtering — produce compared to an unrefined baseline in real open-source GitHub Actions projects?

**RQ2:** Do the carbon savings from these refinement strategies remain consistent across projects of different sizes, languages, and build complexities, or does effectiveness vary by project type?

**RQ3:** Which refinement strategy produces the largest measured carbon reduction relative to implementation effort, and what evidence-based recommendations can be offered to open-source maintainers?

## Methodology Summary

- **Project Selection:** 6-8 open-source GitHub Actions projects, diverse in language and size
- **Instrument:** Eco-CI for energy estimation; SCI specification for carbon calculation
- **Design:** Four configurations per project (baseline, caching, consolidation, path-filtering), 30 runs each
- **Analysis:** Wilcoxon signed-rank tests with Bonferroni correction; Cliff's Delta effect sizes
- **Artefact:** Public replication package with forked repos, workflow YAML files, measurement data, analysis scripts

---

# PART 5: PAPERS TO DOWNLOAD (Quick Reference)

| # | Paper | Direct Download Link | Status |
|---|---|---|---|
| 1 | Saavedra et al. (2025) | https://arxiv.org/pdf/2510.26413 | Open Access |
| 2 | de Medeiros et al. (2025) | https://hal.science/hal-05090865v1/file/Evaluating_the_energy_profile_Maven_Gradle_Queiros_de_Medeiros_etal_2025.pdf | Open Access |
| 3 | Berger-Levrault (2024) | https://www.research-bl.com/ci-cd-pipelines-good-software-development-practice-but-green/ | Open Access |
| 4 | Bouzenia & Pradel (ICSE 2024) | https://software-lab.org/publications/icse2024_workflows.pdf | Open Access (preprint) |
| 5 | Claßen et al. (2023) | https://arxiv.org/pdf/2310.18718 | Open Access |
| 6 | Kruglov et al. (2021) | https://dl.acm.org/doi/epdf/10.1145/3501774.3501777 | Free (ACM eReader) |
| 7 | SCI Specification | https://sci.greensoftware.foundation/ | Open Access |
| 8 | Alamer & Alharbi (2025) | https://journals.gaftim.com/index.php/ijcim/article/download/565/338/1583 | Open Access |
| 9 | Eco-CI Tool | https://github.com/green-coding-solutions/eco-ci-energy-estimation | Open Source (MIT) |

---

# PART 6: NOTES FOR SUPERVISOR DISCUSSION

## Points to Raise

1. **Topic wording:** The shift from "optimisation" to "refinement" — does this framing appropriately convey the empirical, comparative nature of the study without overclaiming?

2. **Project selection criteria:** Should we define specific inclusion criteria (e.g., minimum 100 stars, active in last 6 months, specific language distribution) before the selection phase?

3. **Measurement validation:** Eco-CI is an estimator, not direct measurement. Should we include a validation component comparing Eco-CI estimates against RAPL on a self-hosted runner for a subset of runs?

4. **Statistical approach:** Wilcoxon signed-rank with Bonferroni correction and Cliff's Delta — is this appropriate for comparing four configurations across multiple projects? Should we consider a mixed-effects model?

5. **Scope boundaries:** Should we include test-suite-level changes (e.g., test parallelisation) or keep to pipeline-configuration changes only?

6. **Prior paper integration:** How should the prior HTTPie CLI single-project study be positioned — as a pilot study that informs this expanded work?

---

*Document prepared for supervisor meeting — Umer Karachiwala — 23 June 2026*
