# Weekly Research Log

**Dissertation:** Greening the Pipeline — CI/CD Carbon Impact Study
**Student:** Umer Karachiwala (L00196895)

---

## Week 1: 1–5 July 2026

**Focus:** Repository setup, branch creation, workflow audit

### Done
- Forked HTTPie CLI to `Umer-2612/httpie-cli-carbon-study`
- Created 4 experiment branches: `experiment/c1-baseline`, `experiment/c2-pip-cache`, `experiment/c3-consolidation`, `experiment/c4-combined`
- Added Eco-CI `v5` instrumentation to all workflows on all branches
- Conducted pre-study audit — found 6 critical bugs (see RESEARCH_LOG.md for full details)
- Fixed all bugs: `continue-on-error` scope, merge conflicts in C2, missing `workflow_dispatch`, missing `cache-dependency-path: setup.cfg`, missing HTTPie source tree in C3/C4
- Added `if: always()` to all Eco-CI measurement steps to prevent data loss on test failures

### Blockers
- None

---

## Week 2: 6–12 July 2026

**Focus:** Pilot data collection, paper draft, dissertation structure

### Done
- Triggered initial pilot runs on C1 (code-style), C2 (tests + code-style), C4 (tests + coverage)
- Collected real Eco-CI measurements — pilot results documented in `paper.md`
- Key finding: C2→C4 test matrix energy reduction of 7.1%; dep-install −16.8%
- Wrote full IEEE paper draft (paper.md) — 9 sections, all tables, SCI multi-region analysis
- Updated literature review — found 3 new 2026 papers (IEEE 11500151, PPTAM𝜂, Alves et al.)
- Created dissertation folder structure (`dissertation/chapters/`, `references/`, `appendices/`)
- Wrote Chapter 1: Introduction (~1,700 words, Harvard refs)
- Wrote Chapter 2: Literature Review (Sections 2.1–2.3, ~1,400 words; Sections 2.4–2.5 outlined)
- Wrote Chapter 3: Methodology (full outline, ~1,100 words)
- Created full bibliography in Harvard format (18 references)
- Updated httpie-cli-carbon-study README

### Blockers
- `raw_data.csv` is still empty — need to run full 30-run protocol to populate it
- C3 data not collected yet (no consolidation-only baseline)
- C1 full data (tests + coverage) not yet triggered

### Decision Log
- Chose Wilcoxon signed-rank over t-test: dep-install distributions expected non-normal
- Chose Bonferroni over FDR correction: conservative, simpler to explain to non-statistician audience
- Chose Cliff's delta over Cohen's d: non-parametric, no normality assumption

---

## Week 3 Plan: 13–19 July 2026

**Focus:** Full 30-run data collection + Literature Review completion

### Targets
- [ ] Trigger 30 × C1 baseline runs (all 3 workflows: tests, code-style, coverage)
- [ ] Verify C1 artifacts are all producing valid Eco-CI JSON output
- [ ] Trigger 30 × C2 cached runs after C1 completes
- [ ] Trigger 30 × C3 consolidation runs
- [ ] Write Lit Review Sections 2.4 (Scheduling) and 2.5 (Tools/Standards/SLR)
- [ ] Attend supervisor meeting Tuesday 15 July — note feedback

### Decision to make this week
- Whether to run C3 before or after C4 (C3 needed to isolate consolidation effect from C4 interpretation)
- How many additional projects to select — confirm with supervisor on Tuesday

---

## Upcoming Weeks

| Week | Dates | Focus |
|---|---|---|
| Week 4 | 20–26 Jul | Trigger C4 runs; select + fork additional projects |
| Week 5 | 27 Jul–2 Aug | Additional project baselines; full Methodology chapter |
| Week 6 | 3–9 Aug | Additional project C2/C3/C4 runs; start Results chapter |
| Week 7 | 10–16 Aug | Complete all data collection |
| Week 8 | 17–23 Aug | Statistical analysis (notebook) |
| Week 9 | 24–30 Aug | Cross-project analysis; Results chapter full draft |
| Week 10 | 31 Aug–6 Sep | Discussion chapter |
| Week 11 | 7–13 Sep | All chapters drafted; Conclusion |
| Week 12 | 14–20 Sep | Polish, proof-read, format in ATU Word template |
| Week 13 | 21–27 Sep | Final submission |
