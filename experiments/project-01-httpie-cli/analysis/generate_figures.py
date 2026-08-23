#!/usr/bin/env python3
"""Generate the real Chapter 5 figures from the full n=30 dataset."""
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path

FIGURES_DIR = Path(__file__).resolve().parent.parent / 'results' / 'figures'
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({'figure.dpi': 150, 'font.family': 'DejaVu Sans',
                      'axes.spines.top': False, 'axes.spines.right': False})

df = pd.read_csv(Path(__file__).resolve().parent.parent / 'results' / 'raw_data.csv')
df['energy_joules'] = pd.to_numeric(df['energy_joules'], errors='coerce')
df = df.dropna(subset=['energy_joules', 'config', 'project'])

CONFIG_ORDER = ['C1', 'C2', 'C3', 'C4']
CONFIG_COLOURS = {'C1': '#4e79a7', 'C2': '#f28e2b', 'C3': '#59a14f', 'C4': '#e15759'}
PROJECT_ORDER = ['httpie', 'got', 'retrofit', 'resty', 'gson']
PROJECT_LABELS = {'httpie': 'HTTPie (Python)', 'got': 'got (JavaScript)',
                   'retrofit': 'Retrofit (Java)', 'resty': 'resty (Go)', 'gson': 'Gson (Java, size-axis)'}
GRID_INTENSITY = {'Ireland': 345, 'Germany': 350, 'Norway': 25, 'USA': 386, 'Singapore': 408}


def run_totals_for(project, config):
    sub = df[(df['project'] == project) & (df['config'] == config)]
    workflows = sorted(sub['workflow'].unique())
    if len(workflows) == 1:
        return sub.groupby('run_id')['energy_joules'].sum().values
    per_workflow_totals = []
    for wf in workflows:
        wf_sub = sub[sub['workflow'] == wf]
        totals = wf_sub.groupby('run_id')['energy_joules'].sum().sort_index()
        per_workflow_totals.append(totals)
    n = min(len(t) for t in per_workflow_totals)
    aligned = [t.iloc[-n:].values for t in per_workflow_totals]
    return np.sum(aligned, axis=0)


totals_by = {(p, c): run_totals_for(p, c) for p in PROJECT_ORDER for c in CONFIG_ORDER}

# Figure 5.1 — mean energy per config, one panel per project
fig, axes = plt.subplots(1, 5, figsize=(20, 4), sharey=False)
for ax, project in zip(axes, PROJECT_ORDER):
    means = [totals_by[(project, c)].mean() for c in CONFIG_ORDER]
    sds = [totals_by[(project, c)].std(ddof=1) for c in CONFIG_ORDER]
    ax.bar(CONFIG_ORDER, means, yerr=sds, capsize=4,
           color=[CONFIG_COLOURS[c] for c in CONFIG_ORDER], edgecolor='white', linewidth=0.8, width=0.6)
    ax.set_title(PROJECT_LABELS[project], fontsize=10, fontweight='bold')
    ax.set_ylabel('Mean total energy per run (J)', fontsize=9)
    ax.tick_params(labelsize=8)
fig.suptitle('Figure 5.1: Mean total energy per run, by configuration and project (n=30, error bars = ±1 SD)',
             fontsize=11, fontweight='bold', y=1.03)
fig.tight_layout()
fig.savefig(FIGURES_DIR / 'fig5_1_mean_energy_by_project.png', bbox_inches='tight')
plt.close(fig)
print('Saved fig5_1')

# Figure 5.2 — box plots
fig, axes = plt.subplots(1, 5, figsize=(20, 4), sharey=False)
for ax, project in zip(axes, PROJECT_ORDER):
    data = [totals_by[(project, c)] for c in CONFIG_ORDER]
    bp = ax.boxplot(data, tick_labels=CONFIG_ORDER, patch_artist=True,
                     medianprops={'color': 'black', 'linewidth': 1.5},
                     flierprops={'marker': 'o', 'markersize': 3, 'alpha': 0.5})
    for patch, c in zip(bp['boxes'], CONFIG_ORDER):
        patch.set_facecolor(CONFIG_COLOURS[c])
        patch.set_alpha(0.75)
    ax.set_title(PROJECT_LABELS[project], fontsize=10, fontweight='bold')
    ax.set_ylabel('Total energy per run (J)', fontsize=9)
    ax.tick_params(labelsize=8)
fig.suptitle('Figure 5.2: Per-run energy distribution underlying the Wilcoxon comparisons (n=30)',
             fontsize=11, fontweight='bold', y=1.03)
fig.tight_layout()
fig.savefig(FIGURES_DIR / 'fig5_2_energy_boxplot_by_project.png', bbox_inches='tight')
plt.close(fig)
print('Saved fig5_2')

# Figure 5.3 — cross-project % change, C4 vs C1
pct_changes = []
for project in PROJECT_ORDER:
    c1 = totals_by[(project, 'C1')]
    c4 = totals_by[(project, 'C4')]
    pct_changes.append((c4.mean() - c1.mean()) / c1.mean() * 100)

fig, ax = plt.subplots(figsize=(8, 4.5))
colors = ['#e15759' if p > 0 else '#59a14f' for p in pct_changes]
bars = ax.bar([PROJECT_LABELS[p] for p in PROJECT_ORDER], pct_changes, color=colors, edgecolor='white', width=0.6)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_ylabel('% change in mean energy, C4 vs C1', fontsize=10)
ax.set_title('Figure 5.3: Percentage energy change (C4 vs C1) by project', fontsize=11, fontweight='bold')
ax.tick_params(axis='x', labelsize=8, rotation=20)
for bar, pct in zip(bars, pct_changes):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (1 if pct > 0 else -2.5),
            f'{pct:+.1f}%', ha='center', fontsize=9)
fig.tight_layout()
fig.savefig(FIGURES_DIR / 'fig5_3_pct_change_by_project.png', bbox_inches='tight')
plt.close(fig)
print('Saved fig5_3')

# Figure 5.6 — 5-region SCI, C2 vs C4
fig, axes = plt.subplots(1, 5, figsize=(21, 4.5), sharey=False)
regions = list(GRID_INTENSITY.keys())
x = np.arange(len(regions))
width = 0.38
for ax, project in zip(axes, PROJECT_ORDER):
    c2_mean_kWh = totals_by[(project, 'C2')].mean() / 3_600_000
    c4_mean_kWh = totals_by[(project, 'C4')].mean() / 3_600_000
    c2_vals = [c2_mean_kWh * GRID_INTENSITY[r] for r in regions]
    c4_vals = [c4_mean_kWh * GRID_INTENSITY[r] for r in regions]
    ax.bar(x - width/2, c2_vals, width, label='C2', color=CONFIG_COLOURS['C2'])
    ax.bar(x + width/2, c4_vals, width, label='C4', color=CONFIG_COLOURS['C4'])
    ax.set_xticks(x)
    ax.set_xticklabels(regions, rotation=45, ha='right', fontsize=8)
    ax.set_ylabel('SCI (gCO2eq/run)', fontsize=9)
    ax.set_title(PROJECT_LABELS[project], fontsize=10, fontweight='bold')
    ax.legend(fontsize=8)
fig.suptitle('Figure 5.6: SCI per run across five grid regions, C2 vs C4, by project (n=30 means)',
             fontsize=11, fontweight='bold', y=1.03)
fig.tight_layout()
fig.savefig(FIGURES_DIR / 'fig5_6_sci_five_region.png', bbox_inches='tight')
plt.close(fig)
print('Saved fig5_6')

print('\nAll figures saved to', FIGURES_DIR)
