# Research Log — CI/CD Carbon Emissions Study
## *Towards Greener Pipelines: Measuring and Optimising Carbon Emissions in CI/CD Workflows*

**Subject project:** HTTPie CLI (`httpie/cli`)
**Measurement tool:** Eco-CI Energy Estimation v5 (`green-coding-solutions/eco-ci-energy-estimation@v5`)
**Statistical framework:** Wilcoxon signed-rank test · Bonferroni correction (α = 0.017) · Cliff's delta
**Carbon metric:** Software Carbon Intensity (SCI) — ISO/IEC 21031:2024

---

## Experiment Configuration Overview

| Config | Branch | Description |
|--------|--------|-------------|
| **C1** | `experiment/c1-baseline` | 3 separate workflow files (tests, code-style, coverage) + Eco-CI; no caching |
| **C2** | `experiment/c2-pip-cache` | Same 3 workflows + `cache: pip` on all `setup-python` steps |
| **C3** | `experiment/c3-consolidation` | All 3 stages merged into single `ci-consolidated.yml`; no caching |
| **C4** | `experiment/c4-combined` | C3 + `cache: pip` + path-based trigger filters |

Each configuration targets 30 repeated `workflow_dispatch` runs for statistical adequacy (Wilcoxon requires n ≥ 6; 30 runs provides >95% power for medium effect sizes at α = 0.017).

---

## Log Entries

---

### [2026-03-29] — Session 1: Initial Audit & Branch Remediation

#### 1.1 Scope of Audit

Following an initial code review across all four experiment branches, a systematic audit was conducted to assess the integrity of each branch prior to any data collection. The audit examined: (a) correctness of GitHub Actions YAML syntax; (b) presence and placement of Eco-CI measurement steps; (c) availability of `workflow_dispatch` triggers; (d) consistency of artifact upload naming; and (e) presence of requisite source code for CI commands to execute successfully.

#### 1.2 Issues Identified — C1 (`experiment/c1-baseline`)

The C1 branch contains the full HTTPie CLI source tree (merged from `httpie/cli`) alongside three instrumented workflow files. The following defects were identified:

**Bug C1-01 (Critical) — `continue-on-error` misplaced inside `with:` block (`tests.yml`)**
In `tests.yml`, the `Eco-CI Start Measurement` step contains `continue-on-error: true` as a key under `with:`, rather than as a top-level step attribute. In YAML terms, this means the key is passed as an input parameter to the GitHub Action (which silently ignores it) rather than being interpreted by the Actions runner as a step-level fault-tolerance directive. The practical consequence is that if the Eco-CI action fails at start-measurement (e.g., due to an upstream API issue or runner misconfiguration), the entire workflow job fails rather than continuing gracefully. All other Eco-CI steps in `tests.yml` correctly place `continue-on-error: true` at the step level.

*Fix:* Promote `continue-on-error: true` to step-level in the `Eco-CI Start Measurement` step of `tests.yml`.

**Bug C1-02 (High) — `pyopenssl` matrix dimension causing artifact name collisions (`tests.yml`)**
The test job matrix includes `pyopenssl: [0, 1]`, doubling the number of jobs from 3 to 6 (3 Python versions × 2 pyopenssl values). The artifact upload step uses the naming pattern `eco-ci-results-tests-py${{ matrix.python-version }}-${{ matrix.os }}`, which omits the `pyopenssl` dimension. Consequently, two jobs sharing the same Python version (e.g., 3.12) will both attempt to upload an artifact named `eco-ci-results-tests-py3.12-ubuntu-latest`, with the second upload overwriting the first. This results in data loss per run and renders the energy measurements for one pyopenssl variant unrecoverable. Additionally, the pyopenssl matrix dimension is irrelevant to energy consumption measurement; its presence represents an upstream testing concern that was not removed when the workflow was adapted for research purposes.

*Fix:* Remove the `pyopenssl` matrix dimension entirely. Testing with and without PyOpenSSL is not a variable of interest in the energy study.

**Bug C1-03 (Medium) — `ci-consolidated.yml` present on C1 branch**
The C1 branch includes `ci-consolidated.yml`, the workflow file designed for C3/C4 configurations. This file has a `workflow_dispatch` trigger, meaning it can be manually triggered from the GitHub Actions UI while on the `c1-baseline` branch. If triggered accidentally, it would produce energy measurements structurally equivalent to C3 (no caching, consolidated jobs) while being attributed to the C1 branch by the `collect_results.py` script. This would silently corrupt the C1 dataset.

*Fix:* Remove `ci-consolidated.yml` from the C1 branch.

**Note C1-04 (Low) — Upstream non-research workflows present**
The C1 branch retains all original HTTPie upstream workflow files: `benchmark.yml`, `content.yml`, `docs-check-markdown.yml`, `docs-deploy.yml`, `release-*.yml`, `stale.yml`, `test-package-*.yml`. While most are scoped to `push: branches: [master]` and will not trigger on `experiment/**` branches, their presence introduces ambiguity in the GitHub Actions UI and represents unnecessary surface area. These are removed as a precautionary measure to ensure clean data collection.

*Fix:* Remove all non-research workflow files from C1.

---

#### 1.3 Issues Identified — C2 (`experiment/c2-pip-cache`)

The C2 branch was created with the intent of adding `cache: pip` to all `setup-python` steps. The branch was constructed by merging changes on top of the httpie main source, but the merge was not fully resolved, leaving all three workflow files in a broken state.

**Bug C2-01 (Critical) — Unresolved merge conflicts in all three workflow files**
`tests.yml`, `code-style.yml`, and `coverage.yml` all contain unresolved Git merge conflict markers (`<<<<<<< HEAD`, `=======`, `>>>>>>> main`). GitHub Actions YAML parsing is strict: the presence of these markers renders the files syntactically invalid. No workflow on C2 will parse or execute in its current state.

*Fix:* Rewrite all three workflow files from clean, conflict-free definitions.

**Bug C2-02 (Critical) — `workflow_dispatch` trigger absent from all three workflows**
None of the three C2 workflow files include a `workflow_dispatch` trigger. Since the research protocol requires manual triggering of 30 runs per configuration, the absence of this trigger means C2 cannot be triggered on-demand and can only run via `push` or `pull_request` events. This makes controlled data collection impossible without committing dummy changes to the branch.

*Fix:* Add `workflow_dispatch` with a `reason` input to all three C2 workflow files.

**Bug C2-03 (Critical) — Eco-CI instrumentation stripped from `code-style.yml` and `coverage.yml`**
As a consequence of the failed merge resolution, the HEAD-side content (which contained the Eco-CI instrumentation) was effectively discarded in favour of the `main`-side content (which was the original, uninstrumented HTTPie workflow). Both `code-style.yml` and `coverage.yml` on C2 currently contain no Eco-CI steps and would produce no energy measurement artifacts even if triggered.

*Fix:* Restore full Eco-CI instrumentation to `code-style.yml` and `coverage.yml`, and add `cache: pip` to their `setup-python` steps.

**Bug C2-04 (High) — Duplicate `cache: pip` key in `tests.yml`**
In the partially-merged `tests.yml`, the `cache: pip` key appears twice within the same `with:` block for `setup-python`. In YAML, duplicate keys within a mapping are technically undefined behaviour (the second value typically wins in most parsers). Regardless of parser behaviour, the presence of two identical keys is structurally invalid and would be flagged by a YAML linter.

*Fix:* Remove the duplicate `cache: pip` entry in the rewritten `tests.yml`.

**Bug C2-05 (High) — Excessively large test matrix in `tests.yml`**
The C2 `tests.yml` matrix defines `os: [ubuntu-latest, macos-13, windows-latest]`, `python-version: [3.12, 3.11, 3.10, 3.9, 3.8, 3.7]`, and `pyopenssl: [0, 1]`, yielding 3 × 6 × 2 = 36 parallel jobs per run. For the purposes of this energy study, cross-platform and multi-Python comparability is not a variable under investigation. The matrix should be restricted to `ubuntu-latest` and three Python versions (3.10, 3.11, 3.12) to match the C1 configuration and ensure like-for-like comparisons.

*Fix:* Restrict matrix to `ubuntu-latest` and `python-version: [3.12, 3.11, 3.10]` only.

**Bug C2-06 (Medium) — `ci-consolidated.yml` present on C2 branch**
Same issue as C1-03. The consolidated workflow file is present and triggerable from the C2 branch.

*Fix:* Remove `ci-consolidated.yml` and all non-research workflow files from C2.

---

#### 1.4 Issues Identified — C3 (`experiment/c3-consolidation`)

The C3 branch was created from an early repository commit (prior to the httpie source merge) and contains only the research scaffolding files. The `ci-consolidated.yml` workflow file is structurally correct for C3 (no caching, no path filters, all three stages consolidated). However, the branch is missing the entire httpie application source tree.

**Bug C3-01 (Critical) — Missing httpie source code, tests, and Makefile**
The C3 branch contains only `README.md`, `analysis/energy_analysis.ipynb`, `results/`, `scripts/collect_results.py`, and `.github/workflows/ci-consolidated.yml`. The workflow's jobs execute `make venv`, `make install`, `make codestyle`, `make test`, `make test-cover`, and `make test-dist`. None of these commands can succeed without the `Makefile`, `httpie/` source package, `tests/` directory, and `setup.cfg`/`setup.py` build configuration files. Every single CI job would fail at the first `make` invocation.

*Fix:* Cherry-pick the full httpie source tree from `experiment/c1-baseline` into C3 (selective checkout of all non-`.github` content from C1), preserving the existing C3 workflow file.

---

#### 1.5 Issues Identified — C4 (`experiment/c4-combined`)

The C4 branch was branched from C3 and therefore inherits the same missing source tree. The `ci-consolidated.yml` is correctly configured for C4: path filters are uncommented and active, and `cache: pip` is present on all `setup-python` steps.

**Bug C4-01 (Critical) — Missing httpie source code (inherited from C3)**
Same root cause as C3-01. Without the httpie source tree, all CI jobs fail immediately.

*Fix:* Same selective checkout of C1 source files applied to C4.

**Note C4-02 (Low) — Blank line within `with:` block before `cache: pip`**
In the C4 `ci-consolidated.yml`, a blank line appears between `python-version: '...'` and `cache: pip` within the `with:` mapping block. The YAML specification permits blank lines within block collections, and GitHub Actions' parser (which uses the `js-yaml` library) handles this gracefully. However, the style is inconsistent with standard GitHub Actions workflow conventions and warrants cleanup for clarity.

*Fix:* Remove blank lines within `with:` blocks in `ci-consolidated.yml` on C4.

---

#### 1.6 Remediation Actions Taken

All issues identified above were resolved in this session. The following changes were applied to each branch:

| Branch | Actions |
|--------|---------|
| `experiment/c1-baseline` | Fixed `continue-on-error` placement in `tests.yml`; removed `pyopenssl` matrix dimension; removed `ci-consolidated.yml` and all non-research workflow files |
| `experiment/c2-pip-cache` | Rewrote `tests.yml`, `code-style.yml`, `coverage.yml` from clean definitions with full Eco-CI instrumentation, `cache: pip`, `workflow_dispatch`, and correct ubuntu-only matrix; removed non-research workflows |
| `experiment/c3-consolidation` | Imported full httpie source tree from `experiment/c1-baseline`; `ci-consolidated.yml` retained as-is (already correct for C3) |
| `experiment/c4-combined` | Imported full httpie source tree from `experiment/c1-baseline`; removed blank lines within `with:` blocks in `ci-consolidated.yml` |

All changes committed and pushed to origin. Branches are now in a state where `workflow_dispatch` runs should produce valid Eco-CI energy measurement artifacts.

---

#### 1.7 Next Steps

- [ ] Trigger 30 × `workflow_dispatch` runs per branch (C1–C4) via the GitHub Actions UI
- [ ] Verify at least one run per branch produces Eco-CI artifacts before committing to the full 30-run protocol
- [ ] Run `scripts/collect_results.py` after all runs complete
- [ ] Execute `analysis/energy_analysis.ipynb` to produce statistical results
- [ ] Populate Sections 4 and 5 of `paper/paper-draft.md` with quantitative findings

---

---

### [2026-03-29] — Session 2: Full Research Paper Draft Written

#### 2.1 Source Material Analysed

The `DevOps_Optimisation_Strategy.pages` file was inspected at the binary level (Apple Pages IWA protobuf format — not plain text). Extractable metadata confirmed: title *"Measuring the Carbon Footprint of CI/CD Pipelines: A Green Auditing Methodology for GitHub Actions"*; author Umer Karachiwala, Department of Computing, Atlantic Technological University, Letterkenny, Co. Donegal, Ireland (L00196895@atu.ie). The core body content aligns closely with the existing `paper/paper-draft.md` Introduction section, which was used as the primary source of voice, tone, and intellectual framing.

#### 2.2 Literature References Used

Citations were drawn from verifiable published works. Web search was unavailable in this session (network sandbox); citations are based on established works with high bibliographic confidence. The following references are included in the draft:

| Ref | Citation | Confidence |
|-----|----------|-----------|
| [1] | IEA, *Data Centres and Data Transmission Networks*, 2023 | High |
| [2] | Masanet et al., "Recalibrating Global Data Center Energy-Use Estimates," *Science* 367, 2020, doi:10.1126/science.aba3758 | High |
| [3] | Pinto & Castor, "Energy Efficiency: A New Concern for Application Software Developers," *CACM* 60(12), 2017, doi:10.1145/3154384 | Medium-High |
| [4] | Hilton et al., "Usage, Costs, and Benefits of CI in Open-Source Projects," *ASE 2016*, doi:10.1145/2970276.2970358 | High |
| [5] | Green Software Foundation, *SCI Specification v1.0*, 2022 / ISO/IEC 21031:2024 | High |
| [6] | Green Coding Solutions, *Eco-CI Energy Estimation*, GitHub, 2023 | High (tool reference) |
| [7] | Pereira et al., "Energy Efficiency across Programming Languages," *SLE 2017*, doi:10.1145/3136014.3136031 | Very High |
| [8] | HTTPie, *HTTPie CLI*, GitHub, 2024 | High |
| [9] | EU Commission, CSRD Directive 2022/2464 | High |
| [10] | GitHub Inc., *GitHub Actions Documentation*, 2024 | High |

**Action required before submission:** Verify DOIs [3] and [4] against ACM Digital Library. Cross-check Eco-CI author list against Green Coding Solutions GitHub repository commits/releases page. Replace tool-only reference [6] with a peer-reviewed paper citation if one is published before submission.

#### 2.3 Paper Structure Decisions

The draft is structured as a standard IEEE conference paper with the following sections:
Abstract → I. Introduction → II. Related Work → III. Measurement Methodology → IV. Experiment Design → V. Statistical Analysis → VI. Results → VII. Discussion → VIII. Conclusion → References.

Key structural decisions:
- **Background merged into Methodology (Section III)** rather than a standalone section, to stay within the 6-page limit. SCI formula and Eco-CI architecture are explained concisely inline.
- **Five-region SCI analysis** included in Table VII using Electricity Maps annual average grid intensities (Ireland 345, Germany 350, Norway 25, USA 386, Singapore 408 gCO₂eq/kWh). Note: the `energy_analysis.ipynb` notebook currently computes only Ireland and Norway; it will need to be extended to include Germany, USA, and Singapore before results are populated.
- **Threats to Validity** section included within Discussion (Section VII.D) rather than as a standalone section, saving approximately half a column.
- **All numerical results** are marked `[TBD — insert after pipeline runs complete]`. Tables V, VI, VII and Figures 1–3 are structurally complete with correct column headers and row labels.

#### 2.4 Files Created / Modified

| File | Action |
|------|--------|
| `research_paper_draft.md` | Created — full IEEE-format paper draft, root of repo |
| `RESEARCH_LOG.md` | Updated — this entry |

#### 2.5 Notebook Extension Required

The `analysis/energy_analysis.ipynb` currently computes SCI scores for Ireland and Norway only (Section 5, cell 11). Before populating Table VII, the notebook's `sci_rows` loop must be updated to include Germany (350), USA (386), and Singapore (408) gCO₂eq/kWh. This is a minor addition to the existing loop.

#### 2.6 Next Steps

- [ ] Trigger 30 × `workflow_dispatch` runs per branch (C1–C4); verify first run on each produces valid Eco-CI artifacts before committing to full protocol
- [ ] Run `scripts/collect_results.py` with `GITHUB_TOKEN` and `GITHUB_REPO` set
- [ ] Extend `energy_analysis.ipynb` to include 5-region SCI calculation
- [ ] Run all notebook cells; save output figures to `results/figures/`
- [ ] Populate `[TBD]` placeholders in `research_paper_draft.md` with actual values
- [ ] Verify references [3] and [4] DOIs; source Eco-CI peer-reviewed citation if available
- [ ] Final proofread for IEEE style compliance (figure captions, table numbering, citation inline format)

---

### [2026-08-23] — Session 3: First Successful Run Diagnosed and Fixed

#### 3.1 Finding: Zero Successful Runs Prior to This Session

An audit of the GitHub Actions run history for this repository found that only two runs had ever been triggered (both `P01 HTTPie C1 Tests`, 2026-07-14), and both failed at the `Run tests` step. No other workflow (code-style, coverage, C2, C3, C4) had been triggered even once. `results/raw_data.csv` contained a header row only. This means every energy and SCI figure reported in the dissertation up to this point is drawn from earlier local pilot instrumentation testing, not from a run of the committed workflow files; this has been made explicit with provenance notes in Chapter 4 (`4.6 Worked SCI Calculation Example`) and Chapter 5 of the dissertation.

#### 3.2 Root Cause

The `Run tests` step (`make test`) was reproduced locally against `httpie/cli@3.2.4` on Python 3.11, matching the CI matrix. Of 1,019 collected tests, exactly two failed:

- `tests/test_encoding.py::test_terminal_output_response_charset_detection[big5-...]`
- `tests/test_encoding.py::test_terminal_output_request_charset_detection[big5-...]`

Both assert a specific character-set detection result for a Big5-encoded string. HTTPie 3.2.4 declares `charset_normalizer>=2.0.0` with no upper bound, so `pip install` resolves the newest release of `charset_normalizer` available today, which classifies that byte sequence differently than it did when the test was written in 2023. This is upstream dependency drift external to both HTTPie's application logic and this study's pipeline configurations; it is not something the four experimental configurations can or should fix, since the subject code is frozen and must not be modified (Section 3.2.4).

**Bug C1-05 (Critical) — Two `charset_normalizer`-version-dependent test failures block every configuration**

*Fix:* `PYTEST_ADDOPTS: "-k 'not big5'"` set as a step-level environment variable on every `make test` and `make test-cover` invocation, across all eight workflow files (`p01-httpie-c1-tests.yml`, `p01-httpie-c1-coverage.yml`, `p01-httpie-c2-tests.yml`, `p01-httpie-c2-coverage.yml`, `p01-httpie-c3-consolidated.yml` test and coverage jobs, `p01-httpie-c4-combined.yml` test and coverage jobs). This deselects the two affected parametrized cases without modifying HTTPie's source or test suite, applied identically and symmetrically to all four configurations so it introduces no bias between them. Verified locally: `1007 passed, 5 skipped, 12 deselected, 4 xfailed` with zero failures (12 deselected reflects all `big5`-parametrized cases across both affected test functions, not only the two that fail).

#### 3.3 First Live Run After the Fix: A Second, Version-Specific Failure

The fix was committed, pushed (`main` at `f5f9205`), and triggered live via `workflow_dispatch` on `P01 HTTPie C1 Tests` (run ID `32641295842`). The Python 3.10 and 3.11 matrix jobs passed cleanly with zero failures, confirming the Big5 fix holds on a real GitHub-hosted runner, not just locally. The Python 3.12 job failed on a single, different test:

- `tests/test_cli_ui.py::test_naked_invocation[args3-...]`

Python 3.12 changed how `argparse` renders `invalid choice` error messages: it dropped the quotes around each choice (`choose from all, colors, format, none` instead of `choose from 'all', 'colors', 'format', 'none'`). HTTPie's test asserts the exact old-style string. This is the same category of issue as C1-05: an interpreter-version drift external to pipeline configuration, appearing only because the C1–C4 matrix runs three live Python versions rather than one pinned version.

**Bug C1-06 (Critical) — `argparse` error-format change breaks one test, Python 3.12 only**

*Fix:* Folded into the same `PYTEST_ADDOPTS` deselection: `-k 'not big5 and not test_naked_invocation'`, applied uniformly across the same eight workflow locations and across the full Python 3.10/3.11/3.12 matrix (not conditionally per version), so the deselection is identical and symmetric for every configuration and interpreter version.

#### 3.4 Next Steps

- [x] Trigger one `workflow_dispatch` run per configuration (C1–C4) to confirm the fix holds in the actual GitHub Actions environment, not just locally — C1 confirmed for the Big5 fix; C1-06 found and fixed as a result
- [ ] Re-trigger C1–C4 to confirm both fixes together produce a fully green run across the whole matrix
- [ ] Begin the full 30-run protocol per Section 3.5 once all four configurations are confirmed green
- [ ] Extend the same fork-and-fix procedure to the remaining four projects (got, Retrofit, resty, size-axis) as each is instrumented

---

*Log maintained by: research author*
*Last updated: 2026-08-23*
