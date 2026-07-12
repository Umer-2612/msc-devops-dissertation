# Supervisor Progress Meeting — Tuesday 15 July 2026

**What to bring / show:**
- This document (printed or screen share)
- GitHub repo: https://github.com/Umer-2612/httpie-cli-carbon-study (Actions tab open)
- `dissertation/chapters/01_introduction.md` (open in editor)

---

## What Has Been Done in 2 Weeks (1–12 July 2026)

### Writing Progress

| Deliverable | Status |
|---|---|
| Introduction chapter (~1,700 words) | **Complete draft** |
| Literature Review — Sections 2.1, 2.2, 2.3 | **Drafted** (~1,400 words) |
| Literature Review — Sections 2.4, 2.5, gap analysis | Outline only (to complete next week) |
| Methodology chapter — full outline | **Complete outline** |
| Bibliography (Harvard format, 18 references) | **Complete** (includes 3 new 2026 papers) |
| Results chapter — pilot data tables | **Data entered** (awaiting 30-run full data) |

**Total words written: ~3,500** across chapters 1–3 (introduction fully drafted; lit review ~40% written)

### Practical Progress

| Deliverable | Status |
|---|---|
| HTTPie CLI forked to `Umer-2612/httpie-cli-carbon-study` | ✅ Done |
| 4 experiment branches set up (C1, C2, C3, C4) | ✅ Done |
| Eco-CI instrumented in all 4 configurations | ✅ Done |
| Pre-study audit: 6 critical bugs found and fixed | ✅ Done (documented in RESEARCH_LOG.md) |
| Real pilot data collected (C1, C2, C4 partial) | ✅ Done — **real measurements** |
| Analysis notebook structure (Wilcoxon, Bonferroni, Cliff's delta) | ✅ Framework ready |
| Data collection script (`collect_results.py`) | ✅ Written and tested |
| Paper draft (IEEE format) with pilot results | ✅ 9 sections, tables, SCI scores |

**Pilot key finding:** Test matrix energy C2→C4: **−7.1%** (1,484 J → 1,378 J). Dependency installation stage: **−16.8%**. Norway vs Singapore runner location: **15.3× carbon differential**.

---

## What to Show the Supervisor

### 1. Open the GitHub repo → Actions tab
Show that the 4 experiment branches exist and have run successfully. Point to the Eco-CI artifacts in the completed runs.

### 2. Open `paper.md` → Table V and Table VI
Show the real pilot energy measurements — these are actual numbers from GitHub-hosted runners, not simulations.

### 3. Open `dissertation/chapters/01_introduction.md`
Show the complete Introduction chapter draft with Harvard references.

### 4. Open `dissertation/references/bibliography.md`
Show 18 references including 3 new 2026 papers found this week.

---

## Questions to Ask Supervisor

1. **Project selection:** Do you approve the selection criteria for the additional 5–7 projects? Should I target specific languages (Java, JavaScript/TypeScript, Go)?

2. **Dissertation scope:** The pilot is a single project (HTTPie CLI). Is one well-documented pilot plus 3–4 additional projects sufficient for the dissertation scope, or should I aim for 6–8?

3. **Statistical approach:** Is Wilcoxon signed-rank with Bonferroni correction and Cliff's delta appropriate? Or would you prefer a mixed-effects model?

4. **C3 priority:** Should I collect C3 (consolidation-only) data next week to isolate the consolidation effect? Or is completing C1 and C2 full 30-run data the priority?

5. **ATU formatting:** Should I start writing in Word using the 2022 ATU template now, or continue in Markdown and convert at the end?

6. **IEEE paper:** Is submitting to GREENS 2026 (already passed) or GREENS 2027 worth pursuing as an additional output alongside the dissertation? The paper.md draft is largely complete.

---

## Next Steps (15–25 July 2026)

| Week | Priority Tasks |
|---|---|
| **This week (15–18 Jul)** | Trigger C1 baseline full 30 runs; verify Eco-CI artifacts produce valid data |
| **Next week (19–25 Jul)** | Trigger C2, C3, C4 full 30 runs; write Lit Review Sections 2.4–2.5 |
| **Following week (26 Jul–1 Aug)** | Select and fork 2–3 additional projects; write Methodology chapter in full |
