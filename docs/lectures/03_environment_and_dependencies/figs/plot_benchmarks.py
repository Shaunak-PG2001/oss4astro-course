"""Replot OpenTeams' April 2026 results; run with Python and matplotlib.

Source: https://openteams.com/engineering-blog/benchmark-python-package-managers/
Rocky Linux 8.10, x86_64, 56 cores; median of two runs; ~25 direct
ML dependencies (~200 transitive). Warm installs recreate environments using
cached packages. Conda-family tools use conda-forge/PyPI; others use PyPI
 equivalents. Lockfile generation is a resolution proxy, not resolver-only time.
Tool versions: uv 0.11.7, Pixi 0.67.0, Poetry 2.3.4, Mamba 2.5.0,
pip 25.3, Conda 26.1.1. Only reported results are plotted.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 16})
fig, axes = plt.subplots(1, 2, figsize=(14, 4.5))
series = [
    ("Dependency resolution\n(lockfile generation)", ["uv", "Pixi", "Poetry"],
     [0.5, 19.5, 30.5], 38, [0, 10, 20, 30]),
    ("Package installation\n(warm cache)",
     ["uv", "Pixi", "Poetry", "Mamba", "pip", "Conda"],
     [2.1, 21.8, 86.6, 104.8, 163.5, 163.6], 202, [0, 50, 100, 150]),
]
for ax, (title, names, times, limit, ticks) in zip(axes, series):
    ax.barh(names, times, color=["#7738df" if n == "uv" else "#65778b" for n in names],
            height=0.58, zorder=3)
    ax.invert_yaxis()
    ax.set_xlim(0, limit)
    ax.set_xticks(ticks)
    ax.set_xlabel("Elapsed time (s) · lower is better", fontsize=15, labelpad=10)
    ax.set_title(title, fontsize=19, fontweight="bold", pad=15)
    ax.grid(axis="x", color="#e5e7eb", zorder=0)
    ax.tick_params(axis="both", length=0, pad=8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for label in ax.get_yticklabels():
        if label.get_text() == "uv":
            label.set_color("#7738df")
            label.set_fontweight("bold")
    for row, value in enumerate(times):
        ax.text(value + limit * 0.018, row, f"{value:.1f}", va="center",
                fontsize=16, fontweight="bold" if row == 0 else "normal")
fig.subplots_adjust(left=0.075, right=0.98, bottom=0.19, top=0.79, wspace=0.27)
fig.savefig(Path(__file__).with_name("package-manager-benchmarks.png"), dpi=180,
            facecolor="white")
plt.close(fig)
