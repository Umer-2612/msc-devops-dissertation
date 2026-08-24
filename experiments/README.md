# Experiments

This folder holds one subfolder per open-source project studied. Each project runs the same four pipeline configurations (C1–C4), instrumented as workflow files in this repository's own `.github/workflows/` (no forking — every project is checked out externally at a fixed tag).

## Where the Data Actually Lives

**All measurement data for all five projects is consolidated into a single file: `project-01-httpie-cli/results/raw_data.csv`.** The other four projects' `results/raw_data.csv` files are empty header-only stubs, left over from an earlier per-project layout plan.

This happened because `collect_results.py` infers each row's project and configuration from the *workflow filename* (`p{NN}-{project}-c{1-4}-*.yml`), not from which directory it is run from, and it queries the GitHub Actions API for the entire repository in one pass. The script was only ever run once, from `project-01-httpie-cli/scripts/`, and its output — spanning all five projects — was written to that directory's `results/raw_data.csv`. `analysis/full_analysis.py` and `analysis/energy_analysis.ipynb` (also under `project-01-httpie-cli/`) read from that single file and select each project's rows with `df['project'] == '<name>'`. If you are trying to reproduce Chapter 5's results, this is the one file and the two scripts that matter; the other four projects' `results/` folders can be ignored.

---

## Projects

| # | Folder | Project | Language | Role |
|---|---|---|---|---|
| 01 | `project-01-httpie-cli/` | [HTTPie CLI](https://github.com/httpie/cli) | Python | Anchor |
| 02 | `project-02-got/` | [got](https://github.com/sindresorhus/got) | JavaScript/TypeScript | Cross-language parallel |
| 03 | `project-03-retrofit/` | [Retrofit](https://github.com/lysine-dev/retrofit) | Java | Cross-language parallel |
| 04 | `project-04-resty/` | [resty](https://github.com/go-resty/resty) | Go | Cross-language parallel |
| 05 | `project-05-gson/` | [Gson](https://github.com/google/gson) | Java (Maven) | Size-axis observation |

The full n = 30 statistical protocol (Section 3.5) is complete for all five projects: 720 of 720 runs dispatched, 719 producing usable data. Results, statistical tests, and figures are in `dissertation/DISSERTATION.md`, Chapter 5.

---

## The Four Configurations

Defined once per project as workflow files named `p{NN}-{project}-c{1-4}-{type}.yml`, all living in this repository's root `.github/workflows/`.

| Config | What changes | Strategy |
|---|---|---|
| **C1** | Nothing — Eco-CI added for measurement only | Baseline |
| **C2** | Dependency caching enabled (idiomatic per ecosystem: `cache: pip` / `npm` cache action / `cache: gradle` / `cache: maven` / `cache: true` on setup-go) | Caching only |
| **C3** | Separate workflow files merged into one, where the project has more than one to merge | Consolidation only |
| **C4** | C3's structure + caching | Caching + consolidation |

C4 was originally also intended to include path-based trigger filtering, but every workflow file in every project, C4 included, is triggered exclusively via `workflow_dispatch` so the protocol can dispatch an exact, controlled run count. No file defines a `push`/`paths` trigger, so path filtering's carbon effect is not exercised or measured anywhere in this study (dissertation Section 3.3, 6.6).

For every project except HTTPie, the upstream CI is already a single self-contained job, so C1 and C3 are structurally identical (Section 3.2.5) — this is stated explicitly in each project's README, not discovered as a surprise in the results.

---

## Folder Structure per Project

```
project-NN-name/
├── README.md                 # project summary, configuration table
└── results/
    ├── raw_data.csv          # populated ONLY for project-01 (see above)
    └── figures/               # charts, populated ONLY for project-01
```

`project-01-httpie-cli/` additionally holds `analysis/` (the analysis scripts and notebook), `scripts/` (`trigger_runs.py`, `collect_results.py`), and `RESEARCH_LOG.md` (the full audit trail of bugs found and fixed during data collection — this documents issues found across all five projects, not just HTTPie, despite living in the HTTPie folder for the same historical reason the dataset does).
