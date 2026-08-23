# Project 02: got (JavaScript/TypeScript) — CI/CD Carbon Emissions Study

## What This Is

[got](https://github.com/sindresorhus/got) (15k+ stars, MIT) is the JavaScript cross-language parallel (Section 3.2.3): an HTTP-client library, matching the anchor's domain. Checked out externally at `v15.1.0`; no fork.

## The Four Configurations

Workflow files: `.github/workflows/p02-got-c{1,2,3,4}-*.yml` (repo root).

got's own CI is already a single workflow file, so there is nothing to consolidate (Section 3.2.5): C1 and C3 are structurally identical, and only caching (C2) and the combined config (C4) represent genuine change. got also does not commit a `package-lock.json`, so caching is implemented via `actions/cache` on `~/.npm` rather than `setup-node`'s built-in `cache: npm` input.

| Config | File | What changes |
|---|---|---|
| C1 — Baseline | `p02-got-c1-tests.yml` | No caching |
| C2 — Caching | `p02-got-c2-tests.yml` | + `actions/cache` on `~/.npm` |
| C3 — Consolidation | `p02-got-c3-consolidated.yml` | Structurally identical to C1 |
| C4 — Combined | `p02-got-c4-combined.yml` | Same caching as C2 |

## Status

All four configurations validated (one clean run each) on 23 August 2026. Full n=30 protocol not yet run.

## Reproducing

```bash
set -a && source ../.env && set +a
python3 ../project-01-httpie-cli/scripts/trigger_runs.py --branch main --workflow p02-got-c1-tests.yml --runs 30
python3 ../project-01-httpie-cli/scripts/collect_results.py
```
