# Project 03: Retrofit (Java) — CI/CD Carbon Emissions Study

## What This Is

[Retrofit](https://github.com/lysine-dev/retrofit) (43k+ stars, Apache-2.0) is the Java cross-language parallel (Section 3.2.3): a type-safe HTTP client, matching the anchor's domain. Checked out externally at `2.12.0`; no fork. Note: the repository moved from `square/retrofit` to `lysine-dev/retrofit` (verified as the same, actively-maintained project — see the bibliography entry).

## The Four Configurations

Workflow files: `.github/workflows/p03-retrofit-c{1,2,3,4}-*.yml` (repo root).

Retrofit's own CI defines five jobs (jvm, android, robovm, website, publish); only `jvm` is reproduced, since the others need an Android emulator, a macOS runner, or publishing secrets (Section 3.2.1). The measured command is narrowed to `./gradlew :retrofit:test` (core library tests only) rather than the full `./gradlew build`, which also runs a per-JDK-version compatibility suite that failed intermittently on an unrelated toolchain-provisioning issue. Nothing to consolidate, so C1 and C3 are structurally identical.

| Config | File | What changes |
|---|---|---|
| C1 — Baseline | `p03-retrofit-c1-tests.yml` | No caching |
| C2 — Caching | `p03-retrofit-c2-tests.yml` | + `cache: gradle` on setup-java |
| C3 — Consolidation | `p03-retrofit-c3-consolidated.yml` | Structurally identical to C1 |
| C4 — Combined | `p03-retrofit-c4-combined.yml` | Same caching as C2 |

## Status

All four configurations validated (one clean run each) on 23 August 2026. Full n=30 protocol not yet run.

## Reproducing

```bash
set -a && source ../.env && set +a
python3 ../project-01-httpie-cli/scripts/trigger_runs.py --branch main --workflow p03-retrofit-c1-tests.yml --runs 30
python3 ../project-01-httpie-cli/scripts/collect_results.py
```
