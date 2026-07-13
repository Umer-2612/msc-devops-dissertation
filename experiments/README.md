# Experiments

Each folder here is one project under study. The dissertation measures four CI/CD configurations on each project and compares their carbon impact.

When a new project is added, create a new `project-NN-name/` folder following the same structure.

---

## Projects

| # | Folder | Project | Language | Stars | Status |
|---|---|---|---|---|---|
| 01 | `project-01-httpie-cli/` | [HTTPie CLI](https://github.com/httpie/cli) | Python | 34,000+ | Pilot data collected — 30-run protocol pending |
| 02 | *(next project)* | TBD | TBD | — | Not started |

---

## Standard Folder Layout Per Project

```
project-NN-name/
├── .github/
│   └── workflows/
│       ├── tests.yml           # C1/C2 — original workflows + Eco-CI
│       ├── code-style.yml      # C1/C2 — lint + Eco-CI
│       ├── coverage.yml        # C1/C2 — coverage + Eco-CI
│       └── ci-consolidated.yml # C3/C4 — merged single workflow
├── analysis/
│   └── energy_analysis.ipynb  # Wilcoxon, Bonferroni, Cliff's delta, SCI scores
├── results/
│   ├── raw_data.csv           # Eco-CI measurements (populated by collect_results.py)
│   └── figures/               # Charts from notebook
├── scripts/
│   └── collect_results.py     # Downloads Eco-CI artifacts from GitHub Actions API
├── README.md                  # Project overview, pilot results, how to run
├── RESEARCH_LOG.md            # Technical audit log, decisions, bug fixes
└── ieee_paper_draft.md        # IEEE paper draft for this project (writing lives here)
```

## Configurations Per Project

| Config | Branch | Description |
|---|---|---|
| C1 | `experiment/c1-baseline` | Unmodified pipeline + Eco-CI only |
| C2 | `experiment/c2-pip-cache` | + dependency caching |
| C3 | `experiment/c3-consolidation` | + workflow consolidation (no cache) |
| C4 | `experiment/c4-combined` | + caching + consolidation + path filters |

GitHub Actions runs on the **remote GitHub fork** of each project. The experiment branches live there. This folder tracks the measurement outputs and analysis.
