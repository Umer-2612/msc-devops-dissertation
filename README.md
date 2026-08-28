# MSc DevOps Dissertation

**Title:** Greening the Pipeline: An Empirical Comparison of CI/CD Refinement Strategies and Their Carbon Impact Across Open-Source Projects

**Student:** Umer Karachiwala · L00196895 · ATU Donegal, Ireland
**GitHub:** https://github.com/Umer-2612/msc-devops-dissertation

---

## What This Is

This repository contains the full dissertation writeup and the complete replication package for the underlying experiment.

```
msc-devops-dissertation/
├── dissertation/
│   ├── DISSERTATION.md               ← the dissertation (single source of truth)
│   └── DevOps_Disseration_Umer.pdf   ← final ATU submission-template copy (kept in sync manually)
├── experiments/                       ← one folder per studied project
│   ├── project-01-httpie-cli/         ← HTTPie CLI (Python) — anchor project
│   ├── project-02-got/                ← got (JavaScript)
│   ├── project-03-retrofit/           ← Retrofit (Java)
│   ├── project-04-resty/              ← resty (Go)
│   └── project-05-gson/               ← Gson (Java, size-axis)
├── references/
│   ├── bibliography.md                ← full Harvard-style reference list
│   └── papers/                        ← PDFs of cited and background-reading papers
├── .github/workflows/                 ← the 24 instrumented CI/CD pipelines under study
└── README.md                          ← this file
```

## How the Experiment Works

`.github/workflows/` holds 24 workflow files, named `p{01-05}-{project}-c{1-4}-{type}.yml`. Each one checks out one of the five real, external open-source projects above at a pinned tag, runs that project's own native test command (`make test`, `npm test`, `./gradlew test`, `go test`, `mvn test`), and wraps every stage in Eco-CI energy measurement. The four configurations per project (C1 baseline, C2 caching, C3 consolidation, C4 combined) are the independent variable; energy in joules, converted to SCI carbon figures, is the dependent variable. Full methodology is in `dissertation/DISSERTATION.md`, Chapters 3–4.

## Research Questions

**RQ1:** What carbon reduction does each strategy (caching, consolidation, path filtering) produce compared to an unrefined baseline?

**RQ2:** Is that saving consistent across projects of different languages and sizes, or does it vary?

**RQ3:** Which strategy produces the largest measured carbon reduction relative to implementation effort?

## Status

The full n = 30 data-collection protocol is complete across all five projects (720 of 720 runs dispatched, 719 producing usable data). All statistical analysis, figures, and the full writeup are in `dissertation/DISSERTATION.md`. See that file's Chapter 5 for results, Chapter 6 for discussion, and Appendix A/B for the audit trail and reproducibility procedure.

## Key Files

| File | What it contains |
|---|---|
| `dissertation/DISSERTATION.md` | The complete dissertation: all chapters, references, and appendices |
| `references/bibliography.md` | Full reference list in Harvard format |
| `references/papers/` | PDF copies of cited and background-reading papers |
| `experiments/project-01-httpie-cli/analysis/full_analysis.py` | Canonical statistical analysis script (source of every number in Chapter 5) |
| `experiments/project-01-httpie-cli/analysis/energy_analysis.ipynb` | Notebook mirror of the same analysis |
| `experiments/project-01-httpie-cli/scripts/collect_results.py` | Downloads Eco-CI artifacts from GitHub Actions and builds `raw_data.csv` |
| `experiments/project-01-httpie-cli/RESEARCH_LOG.md` | Audit trail: every bug found and fixed during data collection |
