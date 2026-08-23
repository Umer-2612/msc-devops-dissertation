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

## Week 8: 17–23 August 2026

**Focus:** Get the pipeline actually working end to end; supervisor feedback pass on the dissertation text

### Status check at the start of this week

An audit found that, despite the Week 1–3 setup work, **no CI workflow had ever produced a successful run**. Only two runs existed in GitHub Actions history (both `P01 HTTPie C1 Tests`, triggered 14 July), both failing at `make test`. `results/raw_data.csv` had a header row and nothing else. Every energy/SCI figure written into the dissertation so far (the "7.1% pilot finding") came from earlier local instrumentation testing, not from a real, committed-workflow run — this is now stated explicitly as a provenance note wherever those figures appear (Chapter 4 §4.6, Chapter 5 §5.3).

### Done

- **Restructured the dissertation** per supervisor feedback: split Design out as a new Chapter 4 (pipeline architecture, instrumentation, worked SCI example, Mermaid diagrams), expanded the Literature Review (title + one-liner per paper, wider gap analysis, key-takeaway synthesis), added an Introduction problem statement/objectives/contributions preview, renumbered Results→5, Discussion→6, Conclusion→7, added bibliography entries for got/Retrofit/resty.
- **Diagnosed and fixed the real blocker.** Reproduced `make test` locally against `httpie/cli@3.2.4`: found two independent, unrelated-to-our-config causes.
  - **Bug C1-05:** `charset_normalizer`'s newer releases changed Big5 charset detection versus what HTTPie 3.2.4's tests expect (unpinned dependency, resolved fresh each install).
  - **Bug C1-06:** Python 3.12's `argparse` changed how it formats invalid-choice error messages (dropped quotes), breaking one exact-string test assertion — only surfaced once we ran the real Python-version matrix live.
  - Fixed both via a `PYTEST_ADDOPTS` deselection applied identically across all 8 workflow files and the full Python 3.10/3.11/3.12 matrix, so no bias is introduced between configurations. Logged in `RESEARCH_LOG.md` and Appendix A as C1-05/C1-06.
- **First real, verified pipeline data.** Triggered one validation run per configuration (C1–C4); all four completed successfully with valid Eco-CI artifacts — the first time every configuration has actually worked. Example real numbers (C1 baseline, not the 30-run protocol): 330–463 J per Python version, SCI ≈ 0.070–0.097 gCO₂eq/run.
- Fixed a real security gap: `.env` (holding the GitHub token) was not in `.gitignore`.

### Blockers

- Artifact **download** (not triggering) is blocked in the assistant's sandbox — GitHub's artifact API redirects to Azure blob storage, which isn't on the allowlist. Workaround: trigger/poll works fine via the API; artifact retrieval for `collect_results.py` needs to be run locally.
- Still no n=30 data for any project. Decision made: validate all 5 projects (one clean run per config each) before committing to the expensive full 30-run protocol on any of them, to avoid discovering a blocking bug mid-batch.

### Decision Log

- Fix dependency/interpreter-drift test failures via `PYTEST_ADDOPTS` deselection rather than modifying HTTPie's source — keeps the subject code frozen per Section 3.2.4, and the fix is symmetric across all four configurations so it can't bias the comparison.
- Validate-then-scale: get one clean run per configuration across all 5 projects first, then run the full n=30 protocol across all of them, rather than finishing one project's full 30 runs before starting the next.

---

## Final Sprint Plan: 23–28 August 2026 (hard deadline)

**The submission deadline is 28 August 2026 — 5 days from today.** This replaces the earlier week-by-week plan below, which assumed a September deadline.

| Day | Date | Focus |
|---|---|---|
| Day 1 | Sat 23 Aug | HTTPie pipeline fixed and validated (done — all 4 configs green, real Eco-CI data confirmed). Dissertation restructure per supervisor feedback (done). |
| Day 2 | Sun 24 Aug | Instrument remaining projects using the external-checkout pattern; validate one run per config each. Start full-protocol data collection on whichever projects are validated first, running in parallel in the background. |
| Day 3 | Mon 25 Aug | Continue/finish data collection across all validated projects. Begin statistical analysis as each project's dataset completes — don't wait for all projects before starting. |
| Day 4 | Tue 26 Aug | Finish statistical analysis (Wilcoxon, Bonferroni, Cliff's delta); populate Chapter 5 figures and tables with real numbers; write Chapter 6 (Discussion) against actual findings, not the pilot narrative. |
| Day 5 | Wed 27 Aug | Finalise Chapter 7 (Conclusion); full proofread; fix any remaining `[Figure/Table TBD]` placeholders; format check against ATU template. |
| Submission | Thu 28 Aug | Final submission. |

**Given 5 days, not 5 weeks, scope has to be prioritised honestly.** Running the full n=30 protocol across all 5 projects, in full statistical rigor, is unlikely to fit alongside the writing and analysis time still required. See the scope discussion below before committing further background CI time.

**Scope decision (23 Aug):** proceeding with all 5 projects at full n=30, accepting the schedule risk this carries. Setup/validation for got, Retrofit, resty, and the size-axis project happens today and tomorrow; the full 30-run protocol runs in parallel across all validated projects as each becomes ready, rather than waiting for all 5 before starting any data collection.



