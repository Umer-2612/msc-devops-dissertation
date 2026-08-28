# Project 04: resty (Go) — CI/CD Carbon Emissions Study

## What This Is

[resty](https://github.com/go-resty/resty) (11k+ stars, MIT) is the Go cross-language parallel (Section 3.2.3): a simple HTTP and REST client library, matching the anchor's domain. Checked out externally at `v2.17.2`; no fork.

## The Four Configurations

Workflow files: `.github/workflows/p04-resty-c{1,2,3,4}-*.yml` (repo root).

resty's own CI is a single workflow file with a Go version matrix (`stable`, `1.20.x`), simplified here to `stable` only to reduce runtime. Caching uses `setup-go`'s built-in `cache: true` on `go.sum`, covering both Go's module cache and build cache in one action (Section 3.2.5, Table 4.1). Nothing to consolidate, so C1 and C3 are structurally identical.

| Config | File | What changes |
|---|---|---|
| C1 — Baseline | `p04-resty-c1-tests.yml` | No caching |
| C2 — Caching | `p04-resty-c2-tests.yml` | + `cache: true` on setup-go |
| C3 — Consolidation | `p04-resty-c3-consolidated.yml` | Structurally identical to C1 |
| C4 — Combined | `p04-resty-c4-combined.yml` | Same caching as C2 |

## Status

Full n = 30 protocol complete for all four configurations. See `dissertation/DISSERTATION.md`, Chapter 5, for results.

## Reproducing

```bash
set -a && source ../.env && set +a
python3 ../project-01-httpie-cli/scripts/trigger_runs.py --branch main --workflow p04-resty-c1-tests.yml --runs 30
python3 ../project-01-httpie-cli/scripts/collect_results.py
```

`collect_results.py` queries the whole repository in one pass and writes every project's rows to `../project-01-httpie-cli/results/raw_data.csv` (see `experiments/README.md`); this project has no separate `results/` folder of its own.
