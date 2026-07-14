# Chapter 2: Literature Review


## 2.1 Introduction

This chapter reviews the body of literature relevant to the measurement and reduction of carbon emissions in software CI/CD pipelines. The review is organised thematically across four areas: (1) ecosystem-scale measurement of CI/CD energy and carbon footprints; (2) energy profiling of individual CI stages and build tools; (3) carbon-aware scheduling and infrastructure-level strategies; and (4) measurement tools, standards, and systematic reviews. A gap analysis in Section 2.5 identifies the precise contribution this dissertation makes to the existing body of knowledge.

The review draws on peer-reviewed papers from IEEE Xplore, the ACM Digital Library, and verified open-access preprints from arXiv, spanning the period 2016–2026. Search terms included: "CI/CD carbon emissions", "GitHub Actions energy", "green software engineering", "software carbon intensity", "Eco-CI", "sustainable DevOps", and "pipeline energy consumption". Papers were included where they directly measure, estimate, or provide tooling for CI/CD energy or carbon consumption, or where they provide foundational methodology (statistical approaches, measurement standards) that this dissertation applies.

---

## 2.2 Ecosystem-Scale Measurement of CI/CD Energy and Carbon

### 2.2.1 The GitHub Actions Ecosystem Footprint

The most comprehensive estimate of the aggregate environmental cost of cloud-based CI/CD is provided by Saavedra, Mendes and Ferreira (2025), who apply the Cloud Carbon Footprint (CCF) framework to quantify the carbon and water footprints of the entire GitHub Actions ecosystem in 2024. Their dataset comprises 2,226,729 workflow runs from 18,683 public repositories, covering 3,446,572 jobs. Operational carbon estimates range from 150.5 MTCO₂e under the most optimistic assumption (runners located in low-carbon Norwegian datacentres) to 994.9 MTCO₂e under the most pessimistic (Indian grid intensity), with the most likely scenario at 456.9 MTCO₂e. The water footprint most likely scenario is 5,738.2 kiloliters.

The paper identifies three mitigation strategies at the ecosystem level: deploying runners in low-carbon regions (up to 67.1% reduction), temporal shifting of scheduled runs (3.9% reduction), and reducing repository sizes. These are high-level strategic recommendations rather than actionable project-level guidance; the study explicitly acknowledges that it estimates resource usage rather than directly measuring it, with only 6.5% of workflows successfully re-executed for validation.

This paper establishes the significance of the problem at scale but does not address how individual maintainers should configure their pipelines. This dissertation addresses that project-level gap directly.

### 2.2.2 Large-Scale Energy Analysis of GitHub Workflows

Alves et al. (2024) conduct the first large-scale analysis of the energy consumption of GitHub Actions workflows by executing workflows locally on a controlled server to measure their energy consumption directly. Their study covers multiple open-source repositories and finds an average aggregated CI energy consumption of 22 kWh per project, with average CO₂ emissions of 10.5 kg, equivalent to the emissions from driving approximately 100 kilometres in a typical European car. The paper frames this as a "software frugality" problem: CI democratisation through GitHub and GitLab has made automated pipelines ubiquitous, but without developer awareness of their energy cost.

The study characterises the distribution as highly skewed: a small number of CI-intensive projects account for disproportionately large energy shares. The authors conclude that developers should have better tools to anticipate and reflect on the environmental consequences of CI configuration choices.

This work provides important empirical grounding for the aggregate energy footprint of CI at the project level, but does not compare refinement strategies or translate energy into standardised carbon units using the SCI framework.

### 2.2.3 Energy Consumption of Continuous Integration in Java Projects

A 2026 IEEE study (DOI: 10.1109/[proceedings].11500151) provides the first comprehensive baseline of CI energy use through a large-scale analysis of 204 open-source Java projects, measuring energy consumption under Maven and Gradle build systems with repeated measurements. The study finds that energy use is highly skewed: while most projects consume energy modestly, a minority of CI-intensive systems reach annual CI energy footprints of hundreds of kilowatt-hours, comparable to a quarter of an average EU household's electricity use.

The finding most relevant to this study is that enabling dependency caching reduced CI energy consumption by 30% on average in Maven projects, and by over 90% in some Gradle cases. This is the strongest empirical validation currently available for dependency caching as a high-impact CI refinement strategy, and it directly supports the inclusion of caching as Configuration C2 here. The study is restricted to Java projects using Maven/Gradle; this study extends the investigation to Python and adds the orthogonal strategies of workflow consolidation and trigger filtering.

---

## 2.3 Energy Profiling of Individual CI Stages

### 2.3.1 Build Automation Tool Energy Profiles

De Medeiros, Lefeuvre, Combemale and Perez (2025) investigate the energy consumption of tasks managed by Apache Maven and Gradle within GitHub Actions CI workflows, using the SmartWatts hardware performance counter tool at 2 Hz sampling. Their dataset comprises 1,167 CI workflows from popular Java projects, yielding 183,355 analysed tasks. Key findings: Maven and Gradle tasks represent 24–28% of total CI workflow energy; testing-related tasks consume the most energy (47% for Maven, 36% for Gradle); and project size does not strongly predict per-task energy consumption (Cliff's Delta predominantly "negligible").

The paper is noteworthy for its measurement rigour (direct hardware measurement via SmartWatts rather than estimation) but is limited to CPU energy (RAM, disk, and network excluded), to Java projects only, and to a "clean environment" execution design that deliberately excludes caching as a worst-case scenario. The authors identify as future work the quantification of energy savings from caching.

This study follows up on that identified future work: it applies caching, measures the before-and-after difference, and does so in Python rather than Java, enabling a cross-language comparison that de Medeiros et al. did not attempt.

### 2.3.2 Platform and Language Energy Comparison

Niang (2024) examines CI/CD pipeline energy consumption by varying three parameters (CI platform, programming language, and build tool) using a single small-scale application of 455 lines of code: GitHub Actions versus GitLab CI/CD, Java versus Python. Energy is estimated using the Eco-CI tool. Key findings: GitHub Actions averaged 13.36 joules per execution compared to GitLab's 21.81 joules; Java averaged 11.36 joules versus Python's 14.62 joules. The study acknowledges its primary limitation explicitly: a single tiny project with no statistical generalisation.

This paper demonstrates the practical application of Eco-CI as a measurement instrument in a CI/CD research context, providing a methodological precedent for this dissertation's use of the same tool. It also establishes GitHub Actions as the lower-energy platform relative to GitLab for the same workload, justifying the focus on GitHub Actions in this study.

### 2.3.3 Energy Measurement in Containerised CI/CD

Ehlers et al. (2026) present PPTAM𝜂, an automated pipeline that integrates power and energy measurement into GitLab CI for containerised API systems. The system coordinates load generation, container monitoring, and hardware power probes to collect comparable metrics at each commit. The pipeline makes energy visible to developers on a per-commit basis, enabling version comparison and trend analysis. Their evaluation on a JWT-authenticated API across four commits demonstrates the methodology's practical applicability.

PPTAM𝜂 is architecturally distinct from this dissertation's approach: it targets containerised microservices on self-hosted infrastructure with direct hardware power probes, while this dissertation targets GitHub-hosted runners using the Eco-CI model-based approach. The two approaches are complementary rather than competing: PPTAM𝜂 achieves higher measurement fidelity on self-hosted systems; Eco-CI enables measurement on shared cloud infrastructure where hardware access is unavailable. This dissertation extends Eco-CI's applicability to a multi-configuration, multi-strategy comparative study, which PPTAM𝜂 does not address.

---

## 2.4 Carbon-Aware Scheduling and Infrastructure Strategies

An orthogonal class of CI/CD carbon reduction strategies focuses not on what the pipeline does but on when and where it runs. Claßen, Thierfeldt, Tochman-Szewc, Wiesner and Kao (2023) propose a system architecture for carbon-aware CI/CD services that aligns workflow execution with periods of low-carbon energy availability. Using real carbon intensity data from WattTime across twelve regions and 7,392 GitHub Actions workflow executions from ten repositories, they find that location shifting alone achieves a 25.31% carbon reduction, with user-supplied execution deadlines enabling combined savings approaching 31.2%. The approach treats CI/CD execution as a schedulable workload that can be deferred within developer-specified tolerances, analogous to demand response in energy systems.

At ecosystem scale, Saavedra, Mendes and Ferreira (2025) find that deploying runners in low-carbon regions is the single most impactful intervention available, with up to 67.1% carbon reduction from regional selection relative to the worst-case (India-region) scenario.

These spatial and temporal scheduling strategies address the carbon intensity of the electricity (I in the SCI formula) rather than the energy consumed (E). This dissertation addresses the orthogonal dimension: reducing E through pipeline configuration changes. The two approaches are complementary: configuration refinement reduces the work performed; scheduling reduces the carbon cost of that work. Combining both represents the most complete available reduction strategy, but each is independently actionable. For open-source maintainers who do not control runner geography (the majority using free GitHub-hosted runners), configuration refinement is the primary available lever.

---

## 2.5 Measurement Tools, Standards, and Systematic Reviews

### 2.5.1 The Software Carbon Intensity Standard

The Software Carbon Intensity specification, published by the Green Software Foundation in 2022 and subsequently adopted as ISO/IEC 21031:2024, defines a standardised, reproducible metric for expressing the carbon intensity of a unit of software functionality (Green Software Foundation, 2024). The formula SCI = ((E × I) + M) / R expresses operational energy (E), grid carbon intensity (I), embodied hardware carbon (M), and a functional unit (R). Unlike absolute carbon footprint metrics, SCI cannot be reduced to zero through offsets or neutralisation credits; only genuine efficiency improvements reduce the score. This property makes it appropriate for comparing pipeline configurations, as it is insensitive to accounting choices.

The specification provides the measurement framework for this dissertation but offers no CI/CD-specific guidance and no empirical data on what configuration changes actually reduce SCI in practice. This dissertation provides that empirical data.

### 2.5.2 Eco-CI Energy Estimation

Eco-CI (Green Coding Solutions, v5.3.0) is a GitHub Actions action that estimates per-stage energy consumption inside CI workflows without requiring hardware instrumentation (Green Coding Solutions, 2023). It uses an XGBoost machine learning model trained on the SPECpower benchmark database to map CPU utilisation to power draw, integrating over elapsed time to produce per-stage energy values in joules. The model is appropriate for GitHub Actions `ubuntu-latest` runners, which run on Intel Xeon Platinum processors on Azure infrastructure, a hardware configuration well characterised in the SPECpower corpus.

Any systematic model bias affects all four experiment configurations equally and does not distort relative comparisons between configurations, which is this dissertation's primary concern. Niang (2024) applies Eco-CI in a prior CI/CD energy comparison study, providing a methodological precedent for its use in this research context.

### 2.5.3 GitHub Actions Resource Usage Analysis

Bouzenia and Pradel (2024) provide the most comprehensive prior empirical study of resource usage in GitHub Actions. Analysing 952 repositories, 1.3 million workflow runs, and 3.7 million jobs, they find that 91.2% of resources are consumed by testing and building. They document adoption rates for six optimisation strategies: caching (32.9% adoption), fail-fast (75.9%), cancel-in-progress (10.1%), skip-workflow (9.7%), path filtering (20.7%), and custom timeout (14.0%), and estimate the VM time savings each produces. This study provides the empirical baseline for understanding which strategies practitioners actually use and their relative VM time impact.

Two limitations stand out: the study measures VM time and monetary cost rather than energy or carbon, and it estimates optimisation impact retrospectively from historical data rather than running a controlled experiment. Both of those are things this study does differently.

### 2.5.4 Systematic Review of Sustainable DevOps

Alamer and Alharbi (2025) conduct a systematic literature review of 50 studies (2020–2025) on sustainability in DevOps CI/CD pipelines. They identify a methodological shift from hardware-based profiling (RAPL) to ML prediction models, and classify techniques into three categories: carbon-aware scheduling, test-suite optimisation, and lightweight build strategies. The review concludes by identifying the absence of standardised measurement and empirical comparative data as the primary gap in the field, which is precisely what this study addresses.

The review also notes that practical guidance for developers is largely absent from the literature. Existing studies either characterise the problem at scale or propose theoretical frameworks; none provide the project-level experimental evidence that developers need to justify specific configuration choices. This dissertation provides that evidence.

---

## 2.6 Gap Analysis

### Cross-Paper Comparison

| Dimension | Saavedra et al. (2025) | de Medeiros et al. (2025) | Alves et al. (2024) | Bouzenia & Pradel (2024) | Claßen et al. (2023) | IEEE (2026) |
|---|---|---|---|---|---|---|
| **Scale** | 18,683 repos (ecosystem) | 1,167 workflows | Multiple repos | 952 repos | 10 repos | 204 Java repos |
| **What measured** | Carbon + water (estimated) | Per-task CPU energy (J) | Energy per project (kWh) | VM time + cost | Relative carbon intensity | Energy per project (kWh) |
| **Intervention tested** | None (observational) | None (profiling only) | None (characterisation) | None (retrospective) | Temporal scheduling only | Caching only |
| **Multiple strategies compared** | No | No | No | No (adoption rates only) | No | No |
| **Uses SCI standard** | Referenced | No | No | No | No | No |
| **Python projects** | Yes (mixed) | No (Java only) | Yes (mixed) | Yes (mixed) | Yes (mixed) | No (Java only) |
| **Actionable project-level guidance** | Indirect | Limited | Limited | Moderate | Limited | Partial (caching only) |

### The Unified Gap

No existing study has:
1. Experimentally applied multiple CI/CD pipeline refinement strategies (not just documented adoption rates)
2. Across diverse real-world open-source projects in multiple languages
3. Measuring actual carbon impact using a standardised methodology (SCI)
4. Comparing strategies against each other to identify relative effectiveness

Each prior paper addresses a piece of this puzzle:
- **Saavedra et al. (2025):** scale of the ecosystem problem, not what to do about it
- **de Medeiros et al. (2025):** which CI stages consume the most (testing), not how to reduce them
- **Alves et al. (2024):** aggregate project-level energy, not configuration-level interventions
- **IEEE (2026):** validates caching in Java, not multi-strategy comparison or Python
- **Bouzenia & Pradel (2024):** adoption rates and estimated VM time savings, not carbon measurement
- **Claßen et al. (2023):** when to run, not how to configure what runs

**This dissertation occupies the intersection.** It uses SCI (ISO/IEC 21031:2024) as the measurement framework, Eco-CI as the instrument, and applies the pipeline configuration changes identified in the literature to conduct the first experimental, cross-project, multi-strategy comparison with standardised carbon measurement.

---

