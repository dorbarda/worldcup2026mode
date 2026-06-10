"""Score matrix, derived markets, and heatmap rendering (M4).

Given a fixture's goal expectations ``(lam, mu)`` and the Dixon-Coles ``rho``,
:func:`score_matrix` produces the 9x9 exact-score probability grid (0-8 goals
each side, the 9+ tail folded into the 8-bucket).

**Order of operations (fixed, do not reorder):**

1. independent Poisson outer product on a wide grid (captures the tail),
2. apply the Dixon-Coles tau factor to the four low-score cells,
3. aggregate the 9+ tail mass into the 8-bucket (last row / last column),
4. renormalize so the matrix sums to exactly 1.0 -- **renormalization is last.**

The matrix-sums-to-1 invariant holds to machine precision (tested at 1e-9).
"""

from __future__ import annotations

import numpy as np
from scipy.stats import poisson

from .model import dixon_coles_tau

MAX_GOALS = 8  # grid is 0..MAX_GOALS inclusive -> (MAX_GOALS+1) square
_TAIL = 30  # wide grid for the independent Poisson before tail aggregation


def score_matrix(
    lam: float,
    mu: float,
    rho: float,
    max_goals: int = MAX_GOALS,
    tail: int = _TAIL,
) -> np.ndarray:
    """Dixon-Coles exact-score matrix. Rows = home goals, cols = away goals."""
    # 1. independent Poisson on a wide grid
    g = np.arange(tail + 1)
    px = poisson.pmf(g, lam)
    py = poisson.pmf(g, mu)
    P = np.outer(px, py)  # P[x, y]

    # 2. Dixon-Coles tau on the four low-score cells
    P[0, 0] *= dixon_coles_tau(0, 0, lam, mu, rho)
    P[0, 1] *= dixon_coles_tau(0, 1, lam, mu, rho)
    P[1, 0] *= dixon_coles_tau(1, 0, lam, mu, rho)
    P[1, 1] *= dixon_coles_tau(1, 1, lam, mu, rho)

    # 3. aggregate the 9+ tail into the max_goals bucket
    n = max_goals + 1
    M = np.zeros((n, n))
    M[: max_goals, : max_goals] = P[: max_goals, : max_goals]
    M[max_goals, : max_goals] = P[max_goals:, : max_goals].sum(axis=0)  # home tail
    M[: max_goals, max_goals] = P[: max_goals, max_goals:].sum(axis=1)  # away tail
    M[max_goals, max_goals] = P[max_goals:, max_goals:].sum()           # both tails

    # 4. renormalize LAST so the grid sums to exactly 1
    M /= M.sum()
    return M


# --------------------------------------------------------------------------- #
# Derived markets
# --------------------------------------------------------------------------- #
def derived_markets(M: np.ndarray) -> dict:
    """1X2, Over/Under 2.5, BTTS, and the top-5 exact scores from a matrix."""
    n = M.shape[0]
    idx = np.arange(n)
    home_goals = idx[:, None]
    away_goals = idx[None, :]
    total = home_goals + away_goals

    p_home = float(M[home_goals > away_goals].sum())
    p_draw = float(np.trace(M))
    p_away = float(M[home_goals < away_goals].sum())

    p_over = float(M[total >= 3].sum())
    p_under = float(M[total <= 2].sum())

    btts_yes = float(M[1:, 1:].sum())
    btts_no = 1.0 - btts_yes

    flat = [((i, j), float(M[i, j])) for i in range(n) for j in range(n)]
    flat.sort(key=lambda t: t[1], reverse=True)
    top5 = flat[:5]

    return {
        "p_home": p_home,
        "p_draw": p_draw,
        "p_away": p_away,
        "p_over_2_5": p_over,
        "p_under_2_5": p_under,
        "btts_yes": btts_yes,
        "btts_no": btts_no,
        "top5_scores": top5,
    }


def most_likely_score(M: np.ndarray) -> tuple[int, int]:
    """The modal (most probable) exact score."""
    i, j = np.unravel_index(int(np.argmax(M)), M.shape)
    return int(i), int(j)


# --------------------------------------------------------------------------- #
# Heatmap rendering (green -> red gradient, reference style)
# --------------------------------------------------------------------------- #
def render_matrix(
    M: np.ndarray,
    home: str,
    away: str,
    lam: float | None = None,
    mu: float | None = None,
    ax=None,
    max_display: int = 6,
):
    """Render a score matrix as a green->red heatmap table.

    Displays goals 0..``max_display`` for readability (the full 0..8 grid still
    sums to 1; the displayed sub-grid is a view). Returns the matplotlib Axes.
    """
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    if ax is None:
        _, ax = plt.subplots(figsize=(6.5, 6))

    d = max_display + 1
    sub = M[:d, :d]
    cmap = LinearSegmentedColormap.from_list("greenred", ["#1a9850", "#ffffbf", "#d73027"])

    ax.imshow(sub, cmap=cmap, vmin=0, vmax=sub.max())
    ax.set_xticks(range(d))
    ax.set_yticks(range(d))
    ax.set_xticklabels(range(d))
    ax.set_yticklabels(range(d))
    ax.set_xlabel(f"{away} goals")
    ax.set_ylabel(f"{home} goals")

    title = f"{home} vs {away}"
    if lam is not None and mu is not None:
        title += f"   (λ {lam:.2f} / {mu:.2f})"
    ax.set_title(title)

    for i in range(d):
        for j in range(d):
            ax.text(j, i, f"{sub[i, j] * 100:.1f}", ha="center", va="center",
                    fontsize=8, color="black")
    ax.set_xticks(np.arange(-0.5, d, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, d, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1)
    ax.tick_params(which="minor", length=0)
    return ax
