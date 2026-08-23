# MSc Dissertation: Master Working Directory

**Title:** Greening the Pipeline: An Empirical Comparison of CI/CD Refinement Strategies and Their Carbon Impact Across Open-Source Projects

**Student:** Umer Karachiwala · L00196895 · L00196895@atu.ie
**Course:** M.Sc. in DevOps, Atlantic Technological University, Donegal
**Supervisor:** Saim Gafoor
**Started:** 1 July 2026 · **Target Submission:** September 2026

---

## Repository Layout

```
msc-devops-dissertation/
├── dissertation/          ← written chapters (this folder)
├── experiments/           ← one subfolder per project under study
│   ├── README.md          ← index of all projects + standard layout guide
│   └── project-01-httpie-cli/  ← CI/CD workflows, data, analysis, paper draft
├── literature/            ← paper summaries and new papers found
├── notes/                 ← supervisor meeting notes, weekly log, explanations
└── README.md              ← master overview (this file)
```

**Writing lives in** `dissertation/`: chapters, bibliography, appendices.  
**Practical work lives in** `experiments/`: workflows, data, analysis notebooks, paper drafts.  
**As more projects are added**, new folders appear under `experiments/` (project-02, project-03…).

The experiment branches (C1–C4 on GitHub Actions) are at:  
https://github.com/Umer-2612/httpie-cli-carbon-study

---

## Chapter Status

| Chapter | Title | Status | Word Count (target) |
|---|---|---|---|
| 1 | Introduction | Expanded: problem statement, objectives, contributions preview | ~2,200 |
| 2 | Literature Review | Expanded: title+one-liner per paper, gap analysis widened, key takeaway added | ~4,500 |
| 3 | Methodology | Trimmed to research rationale + design; implementation detail moved to Ch4 | ~2,000 |
| 4 | Design | New: pipeline architecture, instrumentation, measurement stages, worked example, diagrams | ~2,000 |
| 5 | Results | Statistical approach + pilot data written; full 30-run data collection pending | ~3,000 |
| 6 | Discussion | Structure written, renumbered from Ch5 | ~2,500 |
| 7 | Conclusion | Structure written, contributions cross-referenced to Ch1 | ~1,200 |
| n/a | Abstract | Not started (write last) | max 250 words |

**Target total:** ~17,500 words

---

## ATU Formatting Requirements (from 2022 template)

- Font: 12pt (body), 10pt (code)
- Line spacing: 1.5
- Alignment: Fully justified
- Referencing: **Harvard** format (Surname, Year)
- Page numbers: Bottom right, from Chapter 1 onwards
- Appendices: Roman numerals (I, II, III…)
- Online sources: No more than 50% of references
- ALL references must be peer-reviewed papers or recognised whitepapers

---

## Key Dates

| Date | Milestone |
|---|---|
| 15 July 2026 (Tue) | Progress meeting: show Introduction draft + pilot data |
| 25 July 2026 | Complete project selection (all 6–8 projects forked) |
| 15 Aug 2026 | All 30-run data collected across C1–C4 |
| 29 Aug 2026 | Statistical analysis complete |
| 12 Sep 2026 | All chapters drafted |
| 26 Sep 2026 | Final submission |
