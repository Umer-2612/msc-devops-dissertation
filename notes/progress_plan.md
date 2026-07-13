# Dissertation Progress Plan
**Student:** Umer Karachiwala (L00196895)  
**Course:** MSc DevOps, ATU Donegal  
**Topic:** Greening the Pipeline: An Empirical Comparison of CI/CD Refinement Strategies and Their Carbon Impact Across Open-Source Projects  
**Plan Created:** 12 July 2026  
**Progress Meeting:** Tuesday 15 July 2026  

---

## SITUATION SUMMARY

You are 2 weeks in. You have completed:
- 9-paper literature review with gap analysis
- Research questions defined (RQ1, RQ2, RQ3)
- Methodology outlined (Eco-CI + SCI, 4 configs, 30 runs, Wilcoxon + Cliff's Delta)
- Supervisor meeting notes prepared (23 June)

**What is missing for Tuesday:** A written chapter draft + one working practical demonstration.

---

## PART A — WHAT TO SHOW ON TUESDAY (3 DAYS)

This is your immediate priority. The professor wants to see **real progress** — not plans, but actual work done.

### Writing Target for Tuesday

| Chapter Section | Target Word Count | Status |
|---|---|---|
| Introduction — Background & Motivation | ~400 words | To write |
| Introduction — Problem Statement | ~300 words | To write |
| Introduction — Research Questions | ~200 words | To write (already defined, just format it) |
| Introduction — Dissertation Structure | ~150 words | To write |
| **Total Introduction Draft** | **~1,050 words** | **Saturday–Sunday** |

> This gives you a solid, complete Introduction draft to show your professor. It does not need to be polished — a working draft is fine.

### Practical Target for Tuesday

| Task | What to Show | When |
|---|---|---|
| Select 1–2 candidate projects | GitHub links + justification table | Saturday |
| Fork one project to your GitHub | Working fork with modified YAML | Saturday |
| Integrate Eco-CI into the workflow | YAML file with Eco-CI steps added | Sunday |
| Run baseline measurement (5–10 runs) | Screenshot or CSV of energy readings | Sunday–Monday |
| Document the setup | A short README in your fork | Monday |

> You do NOT need all 6–8 projects by Tuesday. One working project with a baseline measurement is excellent 2-week progress.

---

### Day-by-Day Plan (Saturday–Tuesday)

#### Saturday 12 July
- [ ] Write Introduction draft (~1,050 words) — see template below
- [ ] Pick 2–3 candidate projects using the selection criteria below
- [ ] Fork the best one to your GitHub account

#### Sunday 13 July
- [ ] Add Eco-CI to the forked project's `.github/workflows/` YAML
- [ ] Trigger 5–10 baseline workflow runs
- [ ] Save the energy output (CSV or screenshots)

#### Monday 14 July
- [ ] Review and tighten the Introduction draft
- [ ] Write a 1-page "Methodology Overview" (bullet points are fine — just the structure)
- [ ] Prepare 3–4 bullet points of what you will show on Tuesday

#### Tuesday 15 July (Meeting Day)
- [ ] Show Introduction draft (printed or screen share)
- [ ] Show the forked repo with Eco-CI integrated
- [ ] Show baseline energy readings
- [ ] Ask supervisor to confirm project selection criteria and statistical approach

---

## PART B — PROJECT SELECTION CRITERIA

Use these criteria to select your 6–8 projects. For Tuesday, select 1–2.

| Criterion | Requirement | Why |
|---|---|---|
| Stars | > 500 GitHub stars | Indicates real-world relevance |
| Last commit | Active in last 3 months | Ensures pipeline is maintained |
| CI system | GitHub Actions only | Eco-CI works on GitHub Actions runners |
| Languages | Mix: at least 1 JavaScript/TypeScript, 1 Python, 1 Java/Go | Tests RQ2 (cross-language) |
| Pipeline size | 2–10 workflow YAML files | Not too simple, not too complex |
| Has tests | Must run automated tests in CI | Testing = dominant energy consumer |
| No self-hosted runners | Ubuntu/Linux GitHub-hosted only | Eco-CI model trained on standard runners |
| Forkable | MIT, Apache 2.0, or similar licence | You need to fork and modify YAML |

**Good starting search:** GitHub topic search → `language:python stars:>500 topic:ci` etc.

---

## PART C — FULL 3-MONTH DISSERTATION TIMELINE

Your dissertation runs approximately **June 23 – September 20, 2026** (~13 weeks total).

### Phase Overview

| Phase | Weeks | Dates | Focus |
|---|---|---|---|
| 0 — Foundation | Weeks 1–2 | Jun 23 – Jul 11 | Literature, RQs, methodology design |
| 1 — Setup | Weeks 3–4 | Jul 12 – Jul 25 | Project selection, environment, first baseline runs |
| 2 — Data Collection | Weeks 5–7 | Jul 26 – Aug 15 | All 6–8 projects × 4 configs × 30 runs |
| 3 — Analysis | Weeks 8–9 | Aug 16 – Aug 29 | Statistical analysis, Wilcoxon, Cliff's Delta |
| 4 — Writing | Weeks 10–11 | Aug 30 – Sep 12 | Chapters: Lit Review, Methodology, Results, Discussion |
| 5 — Polish | Weeks 12–13 | Sep 13 – Sep 26 | Conclusion, abstract, proof-read, submission |

---

### Detailed Weekly Plan

#### PHASE 0 — Foundation (Done)
- [x] Literature review: 9 papers with gap analysis
- [x] Research questions: RQ1, RQ2, RQ3
- [x] Methodology: tools, design, statistical tests
- [x] Supervisor meeting prepared

---

#### PHASE 1 — Setup (Weeks 3–4: Jul 12–25)

**Week 3 (Jul 12–18):** Progress meeting week
- [ ] Write Introduction draft (show Tuesday)
- [ ] Fork 1 project, integrate Eco-CI, run baseline (show Tuesday)
- [ ] After Tuesday: incorporate supervisor feedback
- [ ] Finalise project selection criteria based on feedback

**Week 4 (Jul 19–25):** Complete setup
- [ ] Fork all 6–8 selected projects
- [ ] Add Eco-CI to all baseline workflows
- [ ] Collect 30 baseline runs per project
- [ ] Document each project: name, language, pipeline structure, star count

**Writing this phase:**
- Introduction (working draft by Tuesday, final by Jul 25)
- Research Questions section (already drafted in README — formalise it)

---

#### PHASE 2 — Data Collection (Weeks 5–7: Jul 26–Aug 15)

This is the heaviest practical phase. You will implement and run 3 refinement strategies on each project.

**Strategy 1 — Dependency Caching (Week 5: Jul 26–Aug 1)**
- Add `actions/cache` to all projects
- Run 30 triggered workflow runs per project
- Collect Eco-CI output: energy (J), power (W), estimated CO2e
- Save raw data in CSV: `project | config | run_number | energy_J | co2e_g`

**Strategy 2 — Workflow Consolidation (Week 6: Aug 2–8)**
- Merge parallel/redundant jobs into fewer workflows
- Run 30 triggered workflow runs per project
- Collect same metrics as above

**Strategy 3 — Path-Based Trigger Filtering (Week 7: Aug 9–15)**
- Add `paths:` and `paths-ignore:` filters to `on: push` and `on: pull_request` triggers
- Run 30 triggered workflow runs per project
- Collect same metrics

**Data format target (end of Week 7):**
```
project | strategy | run | energy_J | power_W | co2e_g | duration_s
```
6 projects × 4 configs × 30 runs = 720 rows minimum

**Writing this phase:**
- Literature Review chapter draft (Weeks 5–6)
- Methodology chapter draft (Week 7)

---

#### PHASE 3 — Analysis (Weeks 8–9: Aug 16–29)

**Week 8 (Aug 16–22):**
- [ ] Calculate SCI score per configuration: `SCI = (E × I + M) / R`
  - E = Eco-CI energy (J → kWh)
  - I = GitHub Actions carbon intensity (use IE region or AIE average)
  - M = embodied carbon (estimate from Green Software Foundation data)
  - R = 1 workflow run (your functional unit)
- [ ] Run Wilcoxon signed-rank tests: baseline vs each strategy, per project
- [ ] Apply Bonferroni correction across multiple comparisons
- [ ] Calculate Cliff's Delta effect sizes

**Week 9 (Aug 23–29):**
- [ ] Cross-project comparison: does strategy effectiveness vary by language/size?
- [ ] Combination analysis: caching + filtering together vs. individually
- [ ] Create visualisations: box plots, bar charts, heatmap of strategy × project
- [ ] Summarise key findings against each RQ

**Writing this phase:**
- Results chapter draft (Week 8–9)

---

#### PHASE 4 — Writing (Weeks 10–11: Aug 30–Sep 12)

| Chapter | Target Words | Week |
|---|---|---|
| Introduction | 1,200 | Done in Phase 1 — revise |
| Literature Review | 3,500 | Week 10 — write final version |
| Methodology | 2,500 | Week 10 — write final version |
| Results | 3,000 | Week 11 — write from analysis |
| Discussion | 2,500 | Week 11 — interpret findings vs. RQs |
| **Running total** | **~12,700** | |

**Week 10 priorities:**
- Lit Review: Synthesise papers by theme, not paper-by-paper (group: ecosystem studies, strategy studies, tools, standards)
- Methodology: Describe exactly what you did (reproducible — someone else could replicate this)

**Week 11 priorities:**
- Results: Tables + figures + statistical results (let the data speak)
- Discussion: Answer each RQ, compare to prior work, acknowledge limitations

---

#### PHASE 5 — Polish (Weeks 12–13: Sep 13–26)

**Week 12 (Sep 13–19):**
- [ ] Write Conclusion (~1,000 words): summary, contributions, future work
- [ ] Write Abstract (~300 words): last thing written, first thing read
- [ ] Compile replication package (data CSVs, analysis scripts, YAML files)
- [ ] Check all citations (IEEE or Harvard — confirm with ATU)

**Week 13 (Sep 20–26):**
- [ ] Full proof-read (print it out — find different errors on paper)
- [ ] Format check against ATU dissertation guidelines
- [ ] Submit replication package to GitHub/Zenodo
- [ ] Final submission

---

## PART D — WRITING SPLIT vs PRACTICAL SPLIT

### Overall split recommendation

| Work Type | % of Total Time | Actual Hours (est.) |
|---|---|---|
| Practical (setup, runs, analysis) | 50% | ~60 hours |
| Writing (all chapters) | 40% | ~48 hours |
| Admin (meetings, revisions, formatting) | 10% | ~12 hours |

### Why 50/50 practical vs writing?

Your dissertation is **empirical** — the data is your contribution. No data = no dissertation. But equally, a researcher who collected all the data and wrote nothing also fails. The split works like this:

- **Phases 1–3 (July 12 – Aug 29):** ~70% practical, ~30% writing (lit review + methodology draft in parallel)
- **Phases 4–5 (Aug 30 – Sep 26):** ~20% practical (revisions), ~80% writing

---

## PART E — INTRODUCTION DRAFT TEMPLATE

Use this structure on Saturday. Fill in the `[...]` sections.

---

### Introduction

#### 1.1 Background and Motivation

The global software industry now accounts for approximately [X]% of worldwide electricity consumption, with cloud infrastructure and automated pipelines representing a growing portion of this footprint. Continuous Integration and Continuous Deployment (CI/CD) pipelines — particularly those built on platforms such as GitHub Actions — execute millions of times daily across open-source and commercial projects. Saavedra et al. (2025) estimated the GitHub Actions ecosystem produced between 150.5 and 994.9 metric tonnes of CO2 equivalent in 2024 alone, with a most likely scenario of 456.9 MTCO2e. As the scale of automated software delivery grows, understanding and reducing the environmental impact of CI/CD pipelines has become an emerging priority for sustainable software engineering.

Despite this scale, individual open-source maintainers and DevOps engineers lack practical, evidence-based guidance on which pipeline configuration changes produce measurable carbon reductions. Existing studies have characterised the scale of the problem (Saavedra et al., 2025), profiled energy consumption at the task level (de Medeiros et al., 2025), and catalogued available techniques (Alamer & Alharbi, 2025), but no study has experimentally applied and compared multiple pipeline refinement strategies across diverse real-world projects using a standardised carbon measurement methodology.

#### 1.2 Problem Statement

The core problem this dissertation addresses is the absence of project-level, evidence-based guidance on CI/CD pipeline carbon reduction. While ecosystem-level estimates establish the significance of the problem, they cannot tell an individual developer which configuration change to make first. Pipeline refinement strategies — such as dependency caching, workflow consolidation, and path-based trigger filtering — are individually documented but have never been systematically compared against each other across multiple real-world projects using standardised carbon measurement (ISO/IEC 21031:2024, the Software Carbon Intensity specification).

This absence of comparative, project-level empirical data represents a gap between macro-level awareness and micro-level action. This dissertation addresses that gap directly.

#### 1.3 Research Questions

This dissertation investigates three research questions:

**RQ1:** What carbon reduction does each of three pipeline refinement strategies — dependency caching, workflow consolidation, and path-based trigger filtering — produce compared to an unrefined baseline in real open-source GitHub Actions projects?

**RQ2:** Do the carbon savings from these refinement strategies remain consistent across projects of different sizes, languages, and build complexities, or does effectiveness vary by project type?

**RQ3:** Which refinement strategy produces the largest measured carbon reduction relative to implementation effort, and what evidence-based recommendations can be offered to open-source maintainers?

#### 1.4 Scope and Boundaries

This dissertation focuses on GitHub Actions as the CI/CD platform, using publicly available open-source repositories hosted on GitHub. The study examines pipeline-level configuration changes only — it does not address test-suite restructuring, application-level code changes, or infrastructure-level interventions such as geographic runner selection or temporal scheduling. Carbon measurement is performed using Eco-CI (v5.3.0) for energy estimation and the SCI specification for carbon intensity calculation.

#### 1.5 Dissertation Structure

Chapter 2 reviews existing literature across four themes: ecosystem-scale measurement studies, energy profiling research, carbon-aware scheduling work, and measurement tools and standards. Chapter 3 describes the research methodology in detail, including project selection criteria, experimental design, measurement instrumentation, and statistical analysis approach. Chapter 4 presents the experimental results for each project and strategy. Chapter 5 discusses findings in relation to the research questions and prior literature. Chapter 6 concludes with contributions, limitations, and directions for future work.

---

*End of Introduction Template — ~1,050 words*

---

## PART F — QUESTIONS TO RAISE WITH SUPERVISOR ON TUESDAY

1. **Project selection:** Do you approve the selection criteria (>500 stars, active, GitHub Actions, Ubuntu runners)? Any specific languages you recommend including?
2. **Statistical approach:** Is Wilcoxon signed-rank with Bonferroni + Cliff's Delta the right approach, or would you prefer a mixed-effects model?
3. **Eco-CI vs RAPL:** Do you want a validation component (Eco-CI vs RAPL on self-hosted runner), or is Eco-CI alone sufficient given the scope?
4. **Chapter structure:** Is the 6-chapter structure above what ATU requires, or should methodology be split further?
5. **Replication package:** Should the dataset be submitted to Zenodo, or is a GitHub repository sufficient as the artefact?

---

*Plan created 12 July 2026 — Review after Tuesday supervisor meeting*
