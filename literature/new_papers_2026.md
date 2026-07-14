# New Papers Found: July 2026 Search

Searched 12 July 2026. These papers were NOT in the original June 2026 literature review.
Papers are peer-reviewed or clearly identifiable academic preprints. No AI-generated content included.

---

## Paper 10: IEEE (2026), Energy Consumption of CI in Java Projects

**Full Title:** On the Energy Consumption of Continuous Integration in Open-Source Java Projects
**Source:** IEEE Conference Proceedings 2026 (DOI source: IEEE Xplore Document 11500151)
**URL:** https://ieeexplore.ieee.org/document/11500151/
**Accessed:** 12 July 2026

**Why It Matters:**
This is the most directly relevant new 2026 paper for this dissertation. It:
- Studies 204 open-source Java projects with repeated CI energy measurements
- Finds energy use is highly skewed (most projects modest, few very high)
- **Key finding: Enabling dependency caching cut CI energy by 30% on average for Maven and by 90%+ in some Gradle cases**
- Describes annual CI energy footprints reaching hundreds of kWh for CI-intensive projects

**How to Use in Dissertation:**
- Literature Review Section 2.2.3: cite as the strongest empirical validation of dependency caching's energy impact (2026 peer-reviewed IEEE paper)
- Introduction Section 1.2.3: cite as direct evidence that "enabling dependency caching cuts energy by 30% on average" to establish empirical stakes
- Methodology Section 3.2: cite to justify why caching is included as a primary experimental strategy
- Discussion: compare our Python/HTTPie results . If consistent, this supports cross-language generalisability (RQ2)

**Gap this paper leaves (for our dissertation):**
- Java only (Maven/Gradle), no Python or other languages
- Does not compare consolidation or trigger filtering strategies
- Does not use SCI framework, energy in kWh only, no gCO₂eq per run
- Does not apply cross-project statistical comparison across configurations

---

## Paper 11: Ehlers et al. (2026), PPTAM𝜂: Energy Aware CI/CD for Containers

**Full Title:** PPTAM𝜂: Energy Aware CI/CD Pipeline for Container Based Applications
**Authors:** Ehlers et al. (confirmed via arXiv)
**ArXiv:** https://arxiv.org/abs/2602.12081
**IEEE Xplore:** https://ieeexplore.ieee.org/document/11500255/
**Published:** February 2026
**Accessed:** 12 July 2026

**Summary:**
Integrates power and energy measurement into GitLab CI for containerised API systems using hardware power probes (not model-based estimation). Coordinates load generation, container monitoring, and hardware power probes to collect comparable per-commit energy metrics. Evaluated on a JWT-authenticated API across 4 commits.

**How to Use in Dissertation:**
- Literature Review Section 2.3.3: cite as contemporary 2026 work on CI energy measurement
- Contrast with Eco-CI (model-based, cloud runners) vs PPTAM𝜂 (hardware probes, self-hosted)
- Use to frame the "construct validity" trade-off in Methodology: direct hardware measurement vs. practical cloud estimation

**Key distinction from this dissertation:**
- Self-hosted infrastructure only (direct hardware probe access)
- GitLab CI, not GitHub Actions
- Containerised microservices, not general-purpose pipelines
- No multi-configuration or multi-strategy comparison

---

## Paper 12: Alves et al. (2024), Software Frugality and CI Energy

**Full Title:** Software Frugality in an Accelerating World: the Case of Continuous Integration
**ArXiv:** https://arxiv.org/abs/2410.15816
Under review at Communications of the ACM (as of Oct 2024)
**Published:** October 2024
**Accessed:** 12 July 2026

**Summary:**
First large-scale analysis of GitHub Actions workflow energy consumption via local controlled server execution. Key numbers: average project CI energy = 22 kWh, average CO₂ emissions = 10.5 kg (equivalent to ~100 km driving a European car). Energy use is highly skewed. Argues for developer awareness of CI environmental costs as a "frugality" concern.

**How to Use in Dissertation:**
- Introduction Section 1.2.1: cite the 22 kWh/project and 10.5 kg CO₂ statistics to establish aggregate scale of the problem at project level
- Literature Review Section 2.2.2: cite as a cross-project characterisation study that motivates intervention research
- Gap: Does not compare any refinement strategies; measurement via local execution (not GitHub-hosted runners); no SCI framework

**Note:** This paper is not yet published in a final journal (under review). Use with the caveat that it is a preprint/under review. Check for final publication status before dissertation submission.

---

## GREENS 2026 Workshop @ ICSE 2026

**Event:** 10th IEEE/ACM International Workshop on Green and Sustainable Software
**Co-located with:** ICSE 2026, Rio de Janeiro, Brazil, April 12–18, 2026
**Proceedings URL:** https://conf.researchr.org/home/icse-2026/greens-2026
**ACM DL:** https://dl.acm.org/doi/proceedings/10.5555/979-8-3315-3815-6 (GREENS 2025, check for 2026 proceedings)

**Why Relevant:**
- This is the exact target venue listed in `paper.md` for the HTTPie CLI study
- The dissertation's empirical work directly targets the GREENS workshop audience
- Review the 2026 proceedings for any papers on CI/CD carbon measurement that may overlap , check for priority/novelty conflicts

Download GREENS 2026 proceedings and check for any papers that overlap with this dissertation's methodology. If a paper with a similar multi-strategy CI/CD comparison was published at GREENS 2026, it needs to be cited and the dissertation's contribution differentiated accordingly.

---

## Papers Still to Verify

These appeared in searches but need full access to confirm details:

| Paper | Source | Why It May Matter |
|---|---|---|
| "A Comprehensive Framework for Optimizing API Calls, CI/CD Pipelines, and Energy Testing" | Springer 2026 | CI/CD energy optimisation framework |
| "Assessing the Impact of Refactoring Energy-Inefficient Code Patterns" | arXiv 2506.09370 | Code-level energy impact (contrast with pipeline-level) |
| ICSA 2026 Workshops papers | conf.researchr.org | Architecture-level sustainability |

---

## Search Terms That Should Be Run Again Before Submission

Run these searches again in September 2026 to catch any papers published after July 2026:

- `"GitHub Actions" "energy" "carbon" 2026 site:arxiv.org`
- `"CI/CD" "carbon emissions" "measurement" IEEE 2026`
- `"software carbon intensity" "pipeline" 2026`
- `"Eco-CI" 2026`
- `GREENS 2026 proceedings ACM`
