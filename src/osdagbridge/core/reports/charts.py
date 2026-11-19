"""Charts derived from the same values displayed in report tables."""

import math
import os

from . import styles


def _number(value):
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) and result >= 0 else None


def _plot():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return plt


def figure_tex(name, caption):
    return (r"\begin{figure}[H]" + "\n" + r"\centering" + "\n"
            + r"\includegraphics[width=0.88\textwidth]{assets/" + name + "}" + "\n"
            + r"\caption{" + caption + "}" + "\n" + r"\end{figure}" + "\n")


def write_utilization_chart(values, asset_dir):
    """Show governing UR for each member family; unavailable data stays N/A."""
    labels = ["Steel Plate Girders", "Concrete Deck Slab", "Cross Bracing", "End Diaphragms"]
    available = [_number(values.get(label)) for label in labels]
    if not any(value is not None for value in available):
        return ""
    plt = _plot()
    fig, ax = plt.subplots(figsize=(9, 4.1))
    positions = list(range(len(labels)))
    ax.bar(positions, [v or 0 for v in available],
           color=[styles.CHART_FAIL_COLOR if v is not None and v > 1 else styles.CHART_PASS_COLOR
                  if v is not None else "#DDDDDD" for v in available], width=0.62)
    ax.axhline(1.0, color=styles.CHART_FAIL_COLOR, linestyle="--", linewidth=1.6,
               label="UR = 1.0 threshold")
    for x, value in enumerate(available):
        ax.text(x, (value or 0) + 0.035, f"{value:.2f}" if value is not None else "N/A",
                ha="center", va="bottom", fontsize=9)
    ax.set_xticks(positions, labels, rotation=12, ha="right")
    ax.set_ylim(0, max(1.2, max((v or 0) for v in available) * 1.18))
    ax.set_ylabel("Utilization Ratio (Demand / Capacity)")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    os.makedirs(asset_dir, exist_ok=True)
    fig.savefig(os.path.join(asset_dir, "utilization_summary.png"), dpi=180)
    plt.close(fig)
    return figure_tex("utilization_summary.png", "Governing utilization ratio by member family. N/A indicates unavailable design data.")


def write_quantity_charts(quantities, asset_dir):
    """Write separate plots so different physical units never share an axis."""
    girder = _number(quantities.get("steel_girders_wt_total"))
    bracing_parts = [_number(quantities.get(k)) for k in
                     ("bracing_top_wt_total", "bracing_bot_wt_total", "bracing_diag_wt_total")]
    bracing = sum(v for v in bracing_parts if v is not None) if any(v is not None for v in bracing_parts) else None
    diaphragm = _number(quantities.get("end_diaphragm_wt_total"))
    concrete = _number(quantities.get("concrete_deck_vol_total"))
    rebar = _number(quantities.get("rebar_deck_wt_total"))
    parts = []
    plt = _plot()
    if any(v is not None for v in (girder, bracing, diaphragm)):
        fig, ax = plt.subplots(figsize=(8, 3.6))
        labels = ["Girders", "Cross Bracing", "End Diaphragms"]
        vals = [girder, bracing, diaphragm]
        ax.bar(labels, [v or 0 for v in vals], color=styles.CHART_NEUTRAL_COLOR)
        for x, v in enumerate(vals):
            ax.text(x, (v or 0) + max(0.02, max((n or 0) for n in vals) * 0.02),
                    f"{v:.2f}" if v is not None else "N/A", ha="center")
        ax.set_ylim(0, max(0.2, max((v or 0) for v in vals) * 1.2))
        ax.set_ylabel("Structural steel (MT)")
        fig.tight_layout()
        os.makedirs(asset_dir, exist_ok=True)
        fig.savefig(os.path.join(asset_dir, "steel_quantities.png"), dpi=180)
        plt.close(fig)
        parts.append(figure_tex("steel_quantities.png", "Structural steel quantities by member family (MT)."))
    if concrete is not None or rebar is not None:
        fig, axes = plt.subplots(1, 2, figsize=(8, 3.2))
        for ax, label, value, unit, color in zip(
            axes, ("Deck concrete", "Deck reinforcement"), (concrete, rebar),
            (r"Volume (m$^3$)", "Weight (MT)"),
            (styles.CHART_NEUTRAL_COLOR, styles.CHART_PASS_COLOR)):
            ax.bar([label], [value or 0], color=color, width=0.5)
            ax.text(0, (value or 0) + max(0.02, (value or 0) * 0.03),
                    f"{value:.2f}" if value is not None else "N/A", ha="center")
            ax.set_ylim(0, max(0.2, (value or 0) * 1.2))
            ax.set_ylabel(unit)
        fig.tight_layout()
        os.makedirs(asset_dir, exist_ok=True)
        fig.savefig(os.path.join(asset_dir, "deck_quantities.png"), dpi=180)
        plt.close(fig)
        parts.append(figure_tex("deck_quantities.png", "Concrete deck volume and reinforcement steel weight, shown on separate axes."))
    return "\n".join(parts)
