"""
Génère une figure pédagogique : types de graphiques selon la nature des variables.
Usage (à la racine du projet Support) : python scripts/generate_chart_types_guide.py
Sortie : Figures/Fig_chart_types_guide.png
"""
from __future__ import annotations

import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Reproductibilité
RNG = np.random.default_rng(42)

# matplotlib ≥ 3.9 : tick_labels ; versions antérieures : labels
def _boxplot_labels_kw(labels: list[str]) -> dict:
    ver = tuple(int(x) for x in matplotlib.__version__.split(".")[:2])
    if ver >= (3, 9):
        return {"tick_labels": labels}
    return {"labels": labels}


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(root, "Figures", "Fig_chart_types_guide.png")

    fig, axes = plt.subplots(2, 3, figsize=(14.5, 9.2))
    fig.patch.set_facecolor("#fafafa")
    fig.suptitle(
        "Exemples de graphiques selon la nature des variables (données fictives)",
        fontsize=15,
        fontweight="bold",
        y=0.98,
    )

    # --- 1. Quantitative (une variable continue) — Histogramme ---
    ax = axes[0, 0]
    hist_data = RNG.gamma(shape=2.0, scale=40.0, size=600)
    ax.hist(hist_data, bins=28, color="#2563eb", edgecolor="white", linewidth=0.6, alpha=0.9)
    ax.set_title(
        "Nature : quantitative (continue)\nGraphique : histogramme",
        fontsize=10.5,
        fontweight="600",
    )
    ax.set_xlabel("Valeur")
    ax.set_ylabel("Effectif")

    # --- 2. Nominale (une variable) — Barres d'effectifs ---
    ax = axes[0, 1]
    cats = ["Partagée", "Privée", "Entière", "Hôtel"]
    counts = RNG.integers(15, 130, size=4)
    ax.bar(cats, counts, color="#059669", edgecolor="white", linewidth=0.8)
    ax.set_title(
        "Nature : catégorielle nominale\nGraphique : diagramme en barres",
        fontsize=10.5,
        fontweight="600",
    )
    ax.set_ylabel("Effectif")
    ax.tick_params(axis="x", rotation=12)

    # --- 3. Ordinale (une variable) — Barres dans l'ordre ---
    ax = axes[0, 2]
    ord_labels = ["Très lent", "Lent", "Moyen", "Rapide"]
    ord_counts = [22, 48, 95, 35]
    x = np.arange(len(ord_labels))
    ax.bar(x, ord_counts, color="#d97706", edgecolor="white", linewidth=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(ord_labels, rotation=18, ha="right", fontsize=9)
    ax.set_title(
        "Nature : ordinale (ordre métier)\nGraphique : barres ordonnées",
        fontsize=10.5,
        fontweight="600",
    )
    ax.set_ylabel("Effectif")

    # --- 4. Quantitative × quantitative — Scatter ---
    ax = axes[1, 0]
    x_sc = RNG.uniform(0, 365, 280)
    y_sc = 0.045 * x_sc + RNG.normal(0, 18, size=280)
    ax.scatter(x_sc, y_sc, alpha=0.45, s=14, c="#7c3aed", edgecolors="none")
    ax.set_title(
        "Nature : quantitative × quantitative\nGraphique : nuage de points",
        fontsize=10.5,
        fontweight="600",
    )
    ax.set_xlabel("Disponibilité (jours)")
    ax.set_ylabel("Indicateur Y")

    # --- 5. Nominale × quantitative — Boxplot ---
    ax = axes[1, 1]
    groups_nom = ["Type A", "Type B", "Type C"]
    data_box = [
        RNG.normal(48, 11, 90),
        RNG.normal(62, 14, 90),
        RNG.normal(41, 9, 90),
    ]
    bp = ax.boxplot(
        data_box,
        patch_artist=True,
        medianprops=dict(color="white", linewidth=1.5),
        **_boxplot_labels_kw(groups_nom),
    )
    for patch, col in zip(bp["boxes"], ("#dc2626", "#ea580c", "#ca8a04")):
        patch.set_facecolor(col)
        patch.set_alpha(0.65)
    ax.set_title(
        "Nature : nominale × quantitative\nGraphique : boîte à moustaches",
        fontsize=10.5,
        fontweight="600",
    )
    ax.set_ylabel("Valeur mesurée")

    # --- 6. Ordinale × quantitative — Boxplots ordonnés ---
    ax = axes[1, 2]
    levels = ["Niv. 0", "Niv. 1", "Niv. 2", "Niv. 3"]
    data_ord = [RNG.normal(32 + i * 9, 6, 70) for i in range(4)]
    bp2 = ax.boxplot(
        data_ord,
        patch_artist=True,
        medianprops=dict(color="white", linewidth=1.5),
        **_boxplot_labels_kw(levels),
    )
    for patch in bp2["boxes"]:
        patch.set_facecolor("#0891b2")
        patch.set_alpha(0.65)
    ax.set_title(
        "Nature : ordinale × quantitative\nGraphique : boîtes par niveau (ordre fixe)",
        fontsize=10.5,
        fontweight="600",
    )
    ax.set_ylabel("Score")

    for ax in axes.flat:
        ax.grid(True, alpha=0.22, linestyle="--")
        ax.set_facecolor("#ffffff")

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor=fig.patch.get_facecolor())
    plt.close(fig)
    print(f"Figure écrite : {out_path}")


if __name__ == "__main__":
    main()
