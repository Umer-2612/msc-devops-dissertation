#!/usr/bin/env python3
"""
Full statistical analysis for Chapter 5, run against the real n=30 dataset.
Handles HTTPie's split C1/C2 (3 separate workflow files) by pairing runs
across tests/code-style/coverage in chronological order to reconstruct one
total-energy-per-cycle figure, comparable to C3/C4's single consolidated
workflow and to every other project's single-workflow configs.
"""
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv(Path(__file__).resolve().parent.parent / 'results' / 'raw_data.csv')
df['energy_joules'] = pd.to_numeric(df['energy_joules'], errors='coerce')
df['duration_seconds'] = pd.to_numeric(df['duration_seconds'], errors='coerce')
df = df.dropna(subset=['energy_joules', 'duration_seconds', 'config', 'project'])

CONFIG_ORDER = ['C1', 'C2', 'C3', 'C4']
PROJECT_ORDER = ['httpie', 'got', 'retrofit', 'resty', 'gson']
GRID_INTENSITY = {'Ireland': 345, 'Germany': 350, 'Norway': 25, 'USA': 386, 'Singapore': 408}
BONFERRONI_ALPHA = 0.05 / 3


def cliffs_delta(a, b):
    a, b = np.array(a), np.array(b)
    greater = sum(1 for ai in a for bi in b if ai > bi)
    lesser = sum(1 for ai in a for bi in b if ai < bi)
    return (greater - lesser) / (len(a) * len(b))


def interpret_delta(d):
    ad = abs(d)
    if ad < 0.147: return 'negligible'
    if ad < 0.330: return 'small'
    if ad < 0.474: return 'medium'
    return 'large'


def run_totals_for(project, config):
    """Return an array of total-energy-per-cycle values, correctly paired
    across split workflow files where applicable (HTTPie C1/C2)."""
    sub = df[(df['project'] == project) & (df['config'] == config)]
    workflows = sorted(sub['workflow'].unique())

    if len(workflows) == 1:
        # single workflow file already represents one full cycle per run_id
        return sub.groupby('run_id')['energy_joules'].sum().values

    # multiple workflow files (HTTPie C1/C2: tests, code-style, coverage) ->
    # pair by chronological run order within each file, align on the most
    # recent N runs common to all three (drops early pre-protocol validation runs)
    per_workflow_totals = []
    for wf in workflows:
        wf_sub = sub[sub['workflow'] == wf]
        totals = wf_sub.groupby('run_id')['energy_joules'].sum().sort_index()
        per_workflow_totals.append(totals)

    n = min(len(t) for t in per_workflow_totals)
    aligned = [t.iloc[-n:].values for t in per_workflow_totals]
    return np.sum(aligned, axis=0)


print("=" * 90)
print("TABLE 5.x: Descriptive statistics, total energy per CI run (all stages combined)")
print("=" * 90)
descriptive = {}
for project in PROJECT_ORDER:
    print(f"\n--- {project} ---")
    for config in CONFIG_ORDER:
        totals = run_totals_for(project, config)
        if len(totals) == 0:
            continue
        descriptive[(project, config)] = totals
        print(f"  {config}: n={len(totals):2d}  mean={totals.mean():9.2f} J  "
              f"median={np.median(totals):9.2f} J  sd={totals.std(ddof=1):8.2f} J")

print("\n" + "=" * 90)
print("SHAPIRO-WILK NORMALITY TESTS (total energy per run, per project/config)")
print("=" * 90)
for (project, config), totals in descriptive.items():
    if len(totals) < 3:
        continue
    stat, p = stats.shapiro(totals)
    print(f"  {project:10s} {config}: W={stat:.4f}  p={p:.4f}  {'NORMAL' if p > 0.05 else 'non-normal'}")

print("\n" + "=" * 90)
print("WILCOXON SIGNED-RANK TESTS vs C1 (Bonferroni alpha = {:.4f})".format(BONFERRONI_ALPHA))
print("=" * 90)
wilcoxon_results = {}
for project in PROJECT_ORDER:
    c1 = descriptive.get((project, 'C1'))
    if c1 is None:
        continue
    print(f"\n--- {project} (n_C1={len(c1)}) ---")
    for config in ['C2', 'C3', 'C4']:
        cx = descriptive.get((project, config))
        if cx is None:
            continue
        n = min(len(c1), len(cx))
        try:
            stat, p = stats.wilcoxon(c1[:n], cx[:n])
        except ValueError:
            stat, p = stats.mannwhitneyu(c1, cx, alternative='two-sided')
        d = cliffs_delta(c1, cx)
        pct = (cx.mean() - c1.mean()) / c1.mean() * 100
        sig = p < BONFERRONI_ALPHA
        wilcoxon_results[(project, config)] = dict(stat=stat, p=p, d=d, pct=pct, sig=sig,
                                                     effect=interpret_delta(d), n_c1=len(c1), n_cx=len(cx))
        print(f"  {config} vs C1: n={n:2d}  stat={stat:9.2f}  p={p:.5f}  "
              f"sig={'YES' if sig else 'no':3s}  pct_change={pct:+6.2f}%  "
              f"cliffs_d={d:+.4f} ({interpret_delta(d)})")

print("\n" + "=" * 90)
print("SCI SCORES, FIVE GRID REGIONS (mean energy per run)")
print("=" * 90)
sci_rows = []
for (project, config), totals in descriptive.items():
    mean_kWh = totals.mean() / 3_600_000
    row = {'project': project, 'config': config, 'n': len(totals), 'mean_J': round(totals.mean(), 2)}
    for region, intensity in GRID_INTENSITY.items():
        row[region] = round(mean_kWh * intensity, 6)
    sci_rows.append(row)
sci_df = pd.DataFrame(sci_rows)
pd.set_option('display.width', 200)
print(sci_df.to_string(index=False))

print("\n" + "=" * 90)
print("CROSS-PROJECT SUMMARY (RQ2): % change and effect size, C4 vs C1")
print("=" * 90)
for project in PROJECT_ORDER:
    r = wilcoxon_results.get((project, 'C4'))
    if r:
        print(f"  {project:10s}: {r['pct']:+7.2f}%  cliffs_d={r['d']:+.4f} ({r['effect']:10s})  sig={'YES' if r['sig'] else 'no'}")

print("\n" + "=" * 90)
print("CONSOLIDATION CHECK (C1 vs C3) - should be ~0% for got/retrofit/resty/gson")
print("=" * 90)
for project in PROJECT_ORDER:
    r = wilcoxon_results.get((project, 'C3'))
    if r:
        print(f"  {project:10s}: {r['pct']:+7.2f}%  cliffs_d={r['d']:+.4f} ({r['effect']:10s})  sig={'YES' if r['sig'] else 'no'}")
