# Chapter 2: Literature Review

## 2.1 Introduction

This chapter reviews the body of literature relevant to the measurement and reduction of carbon emissions in software CI/CD pipelines. The review is organised thematically across four areas: ecosystem-scale measurement of CI/CD energy and carbon footprints; energy profiling of individual CI stages and build tools; carbon-aware scheduling and infrastructure-level strategies; and measurement tools, standards, and systematic reviews. A gap analysis in Section 2.6 identifies the precise contribution this dissertation makes to the existing body of knowledge, and Section 2.7 draws out the single takeaway that motivates the research design in Chapter 3.

The review draws on peer-reviewed papers from IEEE Xplore, the ACM Digital Library, and verified open-access preprints from arXiv, spanning the period 2016 to 2026. Search terms included "CI/CD carbon emissions", "GitHub Actions energy", "green software engineering", "software carbon intensity", "Eco-CI", "sustainable DevOps", and "pipeline energy consumption". Papers were included where they directly measure, estimate, or provide tooling for CI/CD energy or carbon consumption, or where they provide foundational methodology (statistical approaches, measurement standards) that this dissertation applies.

---

## 2.2 Ecosystem-Scale Measurement of CI/CD Energy and Carbon

### 2.2.1 The GitHub Actions Ecosystem Footprint

Saavedra, Mendes and Ferreira (2025), in "Environmental Impact of CI/CD Pipelines," apply the Cloud Carbon Footprint (CCF) framework to quantify the carbon and water footprints of the entire GitHub Actions ecosystem in 2024. **One-line takeaway: at ecosystem scale, GitHub Actions produces an estimated 456.9 MTCO₂e per year, and geographic runner placement is the single largest lever available to reduce it.**

Their dataset comprises 2,226,729 workflow runs from 18,683 public repositories, covering 3,446,572 jobs. Operational carbon estimates range from 150.5 MTCO₂e under the most optimistic assumption (runners located in low-carbon Norwegian datacentres) to 994.9 MTCO₂e under the most pessimistic (Indian grid intensity), with the most likely scenario at 456.9 MTCO₂e. The water footprint most likely scenario is 5,738.2 kiloliters.

The paper identifies three mitigation strategies at the ecosystem level: deploying runners in low-carbon regions (up to 67.1% reduction), temporal shifting of scheduled runs (3.9% reduction), and reducing repository sizes. These are high-level strategic recommendations rather than actionable project-level guidance; the study explicitly acknowledges that it estimates resource usage rather than directly measuring it, with only 6.5% of workflows successfully re-executed for validation.

This paper establishes the significance of the problem at scale but does not address how individual maintainers should configure their pipelines. This dissertation addresses that project-level gap directly.

### 2.2.2 Large-Scale Energy Analysis of GitHub Workflows

Alves et al. (2024), in "Software Frugality in an Accelerating World: the Case of Continuous Integration," conduct the first large-scale analysis of the energy consumption of GitHub Actions workflows by executing workflows locally on a controlled server to measure their energy consumption directly. **One-line takeaway: aggregate CI energy consumption is highly skewed across projects, and developers currently have no tooling to see this cost at the point where they make configuration decisions.**

Their study covers multiple open-source repositories and finds an average aggregated CI energy consumption of 22 kWh per project, with average CO₂ emissions of 10.5 kg, equivalent to the emissions from driving approximately 100 kilometres in a typical European car. The paper frames this as a "software frugality" problem: CI democratisation through GitHub and GitLab has made automated pipelines ubiquitous, but without developer awareness of their energy cost.

The study characterises the distribution as highly skewed: a small number of CI-intensive projects account for disproportionately large energy shares. The authors conclude that developers should have better tools to anticipate and reflect on the environmental consequences of CI configuration choices.

This work provides important empirical grounding for the aggregate energy footprint of CI at the project level, but does not compare refinement strategies or translate energy into standardised carbon units using the SCI framework.

### 2.2.3 Energy Consumption of Continuous Integration in Java Projects

A 2026 IEEE study, "On the Energy Consumption of Continuous Integration in Open-Source Java Projects" (Document 11500151), provides the first comprehensive baseline of CI energy use through a large-scale analysis of 204 open-source Java projects, measuring energy consumption under Maven and Gradle build systems with repeated measurements. **One-line takeaway: dependency caching cuts CI energy by 30% on average and by over 90% in the best cases, making it the single strongest empirically validated intervention in the literature.**

The study finds that energy use is highly skewed: while most projects consume energy modestly, a minority of CI-intensive systems reach annual CI energy footprints of hundreds of kilowatt-hours, comparable to a quarter of an average EU household's electricity use.

The finding most relevant to this study is that enabling dependency caching reduced CI energy consumption by 30% on average in Maven projects, and by over 90% in some Gradle cases. This is the strongest empirical validation currently available for dependency caching as a high-impact CI refinement strategy, and it directly supports the inclusion of caching as **Configuration C2** in this dissertation's design. The study is restricted to Java projects using Maven and Gradle; this study extends the investigation to Python, JavaScript, and Go, and adds the orthogonal strategies of workflow consolidation and trigger filtering, neither of which the IEEE study evaluates.

### 2.2.4 Section Summary

Together, these three studies establish that the CI/CD carbon problem is real, large, and skewed towards a minority of intensive projects, and that at least one intervention (caching) already has strong empirical backing in a single-language context. None of the three, however, tests more than one strategy, and none applies a standardised carbon metric consistently across configurations, which is the specific gap this dissertation's four-configuration design is built to close.

---

## 2.3 Energy Profiling of Individual CI Stages

### 2.3.1 Build Automation Tool Energy Profiles

De Medeiros, Lefeuvre, Combemale and Perez (2025), in "Evaluating the Energy Profile of Tasks Managed by Build Automation Tools in Continuous Integration Workflows," investigate the energy consumption of tasks managed by Apache Maven and Gradle within GitHub Actions CI workflows, using the SmartWatts hardware performance counter tool at 2 Hz sampling. **One-line takeaway: testing is the dominant CI energy stage (36 to 47% of total), and project size does not reliably predict per-task energy consumption.**

Their dataset comprises 1,167 CI workflows from popular Java projects, yielding 183,355 analysed tasks. Key findings: Maven and Gradle tasks represent 24 to 28% of total CI workflow energy; testing-related tasks consume the most energy (47% for Maven, 36% for Gradle); and project size does not strongly predict per-task energy consumption (Cliff's Delta predominantly negligible).

The paper is noteworthy for its measurement rigour (direct hardware measurement via SmartWatts rather than estimation) but is limited to CPU energy (RAM, disk, and network excluded), to Java projects only, and to a clean-environment execution design that deliberately excludes caching as a worst-case scenario. The authors identify as future work the quantification of energy savings from caching.

This study follows up on that identified future work: it applies caching, measures the before-and-after difference, and does so across multiple languages, enabling a cross-language comparison that de Medeiros et al. did not attempt.

### 2.3.2 Platform and Language Energy Comparison

Niang (2024), in "CI/CD Pipelines: Good Software Development Practice, But Green?," examines CI/CD pipeline energy consumption by varying three parameters (CI platform, programming language, and build tool) using a single small-scale application of 455 lines of code: GitHub Actions versus GitLab CI/CD, Java versus Python. **One-line takeaway: GitHub Actions is measurably less energy-intensive than GitLab CI/CD for an identical workload, and Eco-CI is a workable instrument for capturing that difference.**

Energy is estimated using the Eco-CI tool. Key findings: GitHub Actions averaged 13.36 joules per execution compared to GitLab's 21.81 joules; Java averaged 11.36 joules versus Python's 14.62 joules. The study acknowledges its primary limitation explicitly: a single tiny project with no statistical generalisation.

Beyond the headline platform comparison, the study is significant for this dissertation because it is one of the few published uses of Eco-CI outside the tool's own documentation, and because its language comparison (Java lower-energy than Python for the same task) raises a question this dissertation's cross-language design is well placed to probe further: whether that language-level gap narrows or widens once a real, non-trivial dependency graph and test suite are involved, rather than a 455-line demonstration program. Niang's platform finding also has a direct design consequence: because GitHub Actions is already the lower-energy platform, any savings measured within this study represent genuine additional reduction on top of a platform choice that is not itself the source of excess energy.

This paper demonstrates the practical application of Eco-CI as a measurement instrument in a CI/CD research context, providing a methodological precedent for this dissertation's use of the same tool. It also establishes GitHub Actions as the lower-energy platform relative to GitLab for the same workload, justifying the focus on GitHub Actions in this study.

### 2.3.3 Energy Measurement in Containerised CI/CD

Ehlers et al. (2026), in "PPTAM𝜂: Energy Aware CI/CD Pipeline for Container Based Applications," present PPTAM𝜂, an automated pipeline that integrates power and energy measurement into GitLab CI for containerised API systems. **One-line takeaway: per-commit energy visibility is achievable with direct hardware power probes on self-hosted infrastructure, but that fidelity comes at the cost of portability to the shared, GitHub-hosted runners most open-source projects actually use.**

The system coordinates load generation, container monitoring, and hardware power probes to collect comparable metrics at each commit. The pipeline makes energy visible to developers on a per-commit basis, enabling version comparison and trend analysis. Their evaluation on a JWT-authenticated API across four commits demonstrates the methodology's practical applicability.

The per-commit framing is the paper's most transferable idea: PPTAM𝜂 treats energy the way most teams already treat test coverage or build time, as a number that appears on every commit and can be watched for regressions over time. This dissertation does not adopt PPTAM𝜂's hardware-probe architecture, since that requires infrastructure open-source maintainers on free GitHub-hosted runners do not control, but the underlying idea, that carbon visibility is most useful when it is continuous rather than a one-off audit, motivates the future-work recommendation in Section 7.4 for a reusable Eco-CI-based workflow template that reports SCI on every push.

PPTAM𝜂 is architecturally distinct from this dissertation's approach: it targets containerised microservices on self-hosted infrastructure with direct hardware power probes, while this dissertation targets GitHub-hosted runners using the Eco-CI model-based approach. The two approaches are complementary rather than competing: PPTAM𝜂 achieves higher measurement fidelity on self-hosted systems; Eco-CI enables measurement on shared cloud infrastructure where hardware access is unavailable. This dissertation extends Eco-CI's applicability to a multi-configuration, multi-strategy comparative study, which PPTAM𝜂 does not address.

### 2.3.4 Why Scale Matters

Two findings from this section, taken together, motivate a design decision made in Chapter 3. De Medeiros et al. (2025) find that project size does not strongly predict per-task energy consumption within Java projects (Section 2.3.1), while Alves et al. (2024) and the IEEE (2026) study both find that a small minority of CI-intensive projects account for a disproportionate share of aggregate CI energy (Sections 2.2.2 to 2.2.3). Read together, these results suggest that the relationship between project scale and CI carbon footprint is not linear and cannot be assumed from a single small anchor project: a larger, more CI-intensive project might behave like the anchor, or it might belong to the disproportionate minority the aggregate studies describe. This is the literature-grounded reasoning behind including a larger, differently-scoped project on the size axis of this study's design (Section 3.2.2), rather than restricting the cross-project comparison to same-size HTTP-client libraries alone.

---

## 2.4 Carbon-Aware Scheduling and Infrastructure Strategies

An orthogonal class of CI/CD carbon reduction strategies focuses not on what the pipeline does but on when and where it runs. Claßen, Thierfeldt, Tochman-Szewc, Wiesner and Kao (2023), in "Carbon-Awareness in CI/CD," propose a system architecture for carbon-aware CI/CD services that aligns workflow execution with periods of low-carbon energy availability. **One-line takeaway: shifting CI/CD execution to low-carbon regions and low-carbon time windows can cut carbon by up to 31.2% without changing what the pipeline actually does.**

Using real carbon intensity data from WattTime across twelve regions and 7,392 GitHub Actions workflow executions from ten repositories, they find that location shifting alone achieves a 25.31% carbon reduction, with user-supplied execution deadlines enabling combined savings approaching 31.2%. The approach treats CI/CD execution as a schedulable workload that can be deferred within developer-specified tolerances, analogous to demand response in energy systems.

The mechanism is worth setting out in a little more detail, because it clarifies exactly what this dissertation does not attempt. WattTime supplies near-real-time marginal carbon intensity forecasts per grid region; Claßen et al.'s scheduler consumes these forecasts and, for any workflow run that carries a developer-supplied deadline (for example, "must complete within four hours"), searches for the lowest-carbon feasible start time within that window before dispatching the job to a runner. The 25.31% figure comes purely from choosing a better region for a fixed job; the additional headroom up to 31.2% comes from also choosing a better time within that region. Neither lever touches the pipeline's own configuration, which is the point of contrast with this dissertation: Claßen et al. hold the pipeline fixed and vary region and time, while this dissertation holds region and time fixed (via `workflow_dispatch` on a single runner location) and varies the pipeline configuration.

At ecosystem scale, Saavedra, Mendes and Ferreira (2025) find that deploying runners in low-carbon regions is the single most impactful intervention available, with up to 67.1% carbon reduction from regional selection relative to the worst-case (India-region) scenario.

These spatial and temporal scheduling strategies address the carbon intensity of the electricity (I in the SCI formula) rather than the energy consumed (E). This dissertation addresses the orthogonal dimension: reducing E through pipeline configuration changes. The two approaches are complementary: configuration refinement reduces the work performed; scheduling reduces the carbon cost of that work. Combining both represents the most complete available reduction strategy, but each is independently actionable. For open-source maintainers who do not control runner geography (the majority using free GitHub-hosted runners), configuration refinement is the primary available lever.

---

## 2.5 Measurement Tools, Standards, and Systematic Reviews

### 2.5.1 The Software Carbon Intensity Standard

The Software Carbon Intensity specification, published by the Green Software Foundation in 2022 and subsequently adopted as ISO/IEC 21031:2024, defines a standardised, reproducible metric for expressing the carbon intensity of a unit of software functionality (Green Software Foundation, 2024). **One-line takeaway: SCI gives this study a comparison metric that cannot be gamed by offsets, but it provides no CI/CD-specific guidance of its own.**

The formula SCI = ((E × I) + M) / R expresses operational energy (E), grid carbon intensity (I), embodied hardware carbon (M), and a functional unit (R). Unlike absolute carbon footprint metrics, SCI cannot be reduced to zero through offsets or neutralisation credits; only genuine efficiency improvements reduce the score. This property makes it appropriate for comparing pipeline configurations, as it is insensitive to accounting choices.

The specification provides the measurement framework for this dissertation but offers no CI/CD-specific guidance and no empirical data on what configuration changes actually reduce SCI in practice. This dissertation provides that empirical data.

### 2.5.2 Eco-CI Energy Estimation

Eco-CI (Green Coding Solutions, v5.x) is a GitHub Actions action that estimates per-stage energy consumption inside CI workflows without requiring hardware instrumentation (Green Coding Solutions, 2023). **One-line takeaway: Eco-CI is the only practical way to get per-stage energy figures on shared GitHub-hosted runners, at the cost of being a model-based estimate rather than a hardware measurement.**

It uses a machine learning model trained on the SPECpower benchmark database to map CPU utilisation to power draw, integrating over elapsed time to produce per-stage energy values in joules. The model is appropriate for GitHub Actions `ubuntu-latest` runners, which run on Intel Xeon Platinum processors on Azure infrastructure, a hardware configuration well characterised in the SPECpower corpus.

Any systematic model bias affects all four experiment configurations equally and does not distort relative comparisons between configurations, which is this dissertation's primary concern. Niang (2024) applies Eco-CI in a prior CI/CD energy comparison study, providing a methodological precedent for its use in this research context. The mechanism by which Eco-CI derives energy is described in detail in Chapter 4.

### 2.5.3 GitHub Actions Resource Usage Analysis

Bouzenia and Pradel (2024), in "Resource Usage and Optimization Opportunities in Workflows of GitHub Actions," provide the most comprehensive prior empirical study of resource usage in GitHub Actions. **One-line takeaway: caching and path filtering are both under-adopted relative to their availability, which is direct evidence that maintainers lack the guidance this dissertation aims to provide.**

Analysing 952 repositories, 1.3 million workflow runs, and 3.7 million jobs, they find that 91.2% of resources are consumed by testing and building. They document adoption rates for six optimisation strategies: caching (32.9% adoption), fail-fast (75.9%), cancel-in-progress (10.1%), skip-workflow (9.7%), path filtering (20.7%), and custom timeout (14.0%), and estimate the VM time savings each produces. This study provides the empirical baseline for understanding which strategies practitioners actually use and their relative VM time impact.

The 20.7% path-filtering adoption figure is the direct empirical motivation for including path-based trigger filtering as part of **Configuration C4** in this dissertation: fewer than one in four repositories in Bouzenia and Pradel's sample use it, despite it being a native GitHub Actions feature that prevents entire runs, not just individual stages, from executing.

Two limitations stand out: the study measures VM time and monetary cost rather than energy or carbon, and it estimates optimisation impact retrospectively from historical data rather than running a controlled experiment. Both of those are things this study does differently.

### 2.5.4 Systematic Review of Sustainable DevOps

Alamer and Alharbi (2025), in "Sustainable DevOps: A Systematic Literature Review on Reducing Energy Footprint in Continuous Integration and Deployment (CI/CD) Pipelines," conduct a systematic literature review of 50 studies (2020 to 2025) on sustainability in DevOps CI/CD pipelines. **One-line takeaway: the field has moved from hardware profiling to ML-based estimation, but still lacks standardised measurement and empirical comparative data, which is precisely the gap this dissertation targets.**

They identify a methodological shift from hardware-based profiling (RAPL) to ML prediction models, and classify techniques into three categories: carbon-aware scheduling, test-suite optimisation, and lightweight build strategies. The review concludes by identifying the absence of standardised measurement and empirical comparative data as the primary gap in the field, which is precisely what this study addresses.

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
| **Multi-language** | Yes (mixed) | No (Java only) | Yes (mixed) | Yes (mixed) | Yes (mixed) | No (Java only) |
| **Design type** | Observational | Observational (profiling) | Observational | Observational (retrospective) | Controlled (scheduling) | Controlled (caching only) |
| **Sample size per condition** | N/A (ecosystem-wide) | N/A (per-task) | N/A (per-project) | N/A (adoption survey) | 7,392 runs, no per-condition paired design | Not reported per condition |
| **Actionable project-level guidance** | Indirect | Limited | Limited | Moderate | Limited | Partial (caching only) |

The two added dimensions matter for positioning this dissertation methodologically, not just thematically. Every prior study in this table is either purely observational or, where an intervention is tested (Claßen et al.'s scheduling, the IEEE study's caching), evaluated without the paired, repeated-measures statistical design (Section 5.2) this dissertation applies. None reports a per-condition sample size sufficient for the kind of significance and effect-size testing (Wilcoxon signed-rank, Cliff's delta) that a controlled comparison of four configurations requires.

### The Unified Gap

No existing study has, together:
1. Experimentally applied multiple CI/CD pipeline refinement strategies (not just documented adoption rates), evaluated as a controlled within-subjects comparison rather than an observational survey;
2. Across diverse real-world open-source projects in multiple languages, holding application domain constant where possible to avoid confounding language with purpose;
3. Measuring actual carbon impact using a standardised methodology (SCI), rather than energy alone or an ecosystem-level carbon estimate;
4. Comparing strategies against each other, and against a common baseline, to identify relative effectiveness and rank them by effort.

Each prior paper addresses a piece of this puzzle: Saavedra et al. (2025) establish the scale of the ecosystem problem and show regional selection dominates all other levers, but not what an individual maintainer without regional control should do instead; de Medeiros et al. (2025) identify which CI stages consume the most (testing) and show project size is a weak predictor on its own, but do not test any intervention that would reduce that consumption; Alves et al. (2024) measure aggregate project-level energy and expose the skewed distribution across projects, but not configuration-level interventions that a maintainer could apply; the IEEE (2026) study validates caching rigorously but only in Java, leaving open whether the effect holds in other ecosystems or alongside other strategies; Bouzenia and Pradel (2024) report adoption rates and estimated VM time savings that reveal caching and path filtering are both under-used, but not their carbon cost; and Claßen et al. (2023) address when and where to run a pipeline, deliberately leaving what the pipeline does unchanged. No paper in this review isolates workflow consolidation as a standalone, measured intervention at all; the closest is Bouzenia and Pradel's observation that fragmented workflows exist at scale, without ever testing the effect of merging them. That absence is what **Configuration C3** in this dissertation's design fills directly.

This dissertation occupies the intersection. It uses SCI (ISO/IEC 21031:2024) as the measurement framework, Eco-CI as the instrument, and applies the pipeline configuration changes identified in the literature to conduct the first experimental, cross-project, multi-strategy comparison with standardised carbon measurement.

---

## 2.7 Summary and Key Takeaway

Drawing the sections above together, three conclusions carry forward into the research design in Chapter 3. First, the literature strongly validates dependency caching as an effective intervention (Section 2.2.3) but has never tested it outside a single-language context, nor alongside other strategies. Second, the largest carbon lever identified anywhere in the literature is not a pipeline configuration change at all but runner geography (Sections 2.2.1 and 2.4), which sets a realistic ceiling on what configuration-level refinement alone should be expected to achieve, and is precisely why this dissertation treats the multi-region SCI analysis (Section 4.6, Section 5.6) as a companion finding rather than the primary result. Third, and most directly, no study has combined a controlled, within-subjects, multi-strategy design with a standardised carbon metric across more than one project or language (Section 2.6); this is the specific, actionable gap that the four-configuration, cross-language design introduced in Chapter 3 is constructed to close.

---
