"""
Figures pédagogiques : corrélation de Pearson vs Spearman, et corrélation trompeuse.
Dépendance : numpy, matplotlib uniquement.
Usage : python scripts/generate_correlation_pedagogy_figures.py
Sorties : Figures/Fig_corr_pearson_spearman.png, Figures/Fig_corr_facteur_commun.png
"""
from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np

RNG = np.random.default_rng(7)


def pearson_r(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 2:
        return float("nan")
    return float(np.corrcoef(x[m], y[m])[0, 1])


def spearman_rho(x: np.ndarray, y: np.ndarray) -> float:
    """Rangs (approximation sans gestion fine des ex-aequo — suffisant pour données continues bruitées)."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 2:
        return float("nan")
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    return float(np.corrcoef(rx, ry)[0, 1])


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fig_dir = os.path.join(root, "Figures")
    os.makedirs(fig_dir, exist_ok=True)

    fig1, axes = plt.subplots(2, 2, figsize=(13.5, 10))
    fig1.patch.set_facecolor("#fafafa")
    fig1.suptitle(
        "Pearson vs Spearman : deux façons de mesurer une association (données simulées)",
        fontsize=14,
        fontweight="bold",
        y=0.98,
    )

    x1 = RNG.normal(0, 1, 90)
    y1 = 2.2 * x1 + RNG.normal(0, 0.35, 90)
    r_p1 = pearson_r(x1, y1)
    r_s1 = spearman_rho(x1, y1)
    ax = axes[0, 0]
    ax.scatter(x1, y1, alpha=0.65, c="#2563eb", edgecolors="white", linewidths=0.3, s=38)
    ax.set_xlabel("Variable X")
    ax.set_ylabel("Variable Y")
    ax.set_title(
        "1 — Nuage « en ligne droite »\n"
        f"Pearson r = {r_p1:.2f}    Spearman rho = {r_s1:.2f}\n"
        "(les deux coefficients sont élevés : la tendance est linéaire)",
        fontsize=10,
        loc="left",
    )
    ax.grid(True, alpha=0.25, linestyle="--")

    t = np.linspace(0.5, 6, 90)
    y2 = 0.4 * t**2 + RNG.normal(0, 0.8, 90)
    r_p2 = pearson_r(t, y2)
    r_s2 = spearman_rho(t, y2)
    ax = axes[0, 1]
    ax.scatter(t, y2, alpha=0.65, c="#059669", edgecolors="white", linewidths=0.3, s=38)
    ax.set_xlabel("Variable X (ex. temps, indice)")
    ax.set_ylabel("Variable Y")
    ax.set_title(
        "2 — Y augmente toujours quand X augmente, mais suivant une courbe\n"
        f"Pearson r = {r_p2:.2f}    Spearman rho = {r_s2:.2f}\n"
        "(Spearman reste souvent plus élevé : l’ordre est respecté même sans droite)",
        fontsize=10,
        loc="left",
    )
    ax.grid(True, alpha=0.25, linestyle="--")

    x3 = np.linspace(-3, 3, 100)
    y3 = x3**2 + RNG.normal(0, 0.4, 100)
    r_p3 = pearson_r(x3, y3)
    r_s3 = spearman_rho(x3, y3)
    ax = axes[1, 0]
    ax.scatter(x3, y3, alpha=0.55, c="#d97706", edgecolors="white", linewidths=0.3, s=32)
    ax.set_xlabel("Variable X")
    ax.set_ylabel("Variable Y")
    ax.set_title(
        "3 — Relation en « U » : ni linéaire, ni monotone globale\n"
        f"Pearson r = {r_p3:.2f}    Spearman rho = {r_s3:.2f}\n"
        "(un seul nombre ne résume pas bien le dessin : regarder le graphique !)",
        fontsize=10,
        loc="left",
    )
    ax.grid(True, alpha=0.25, linestyle="--")

    ax = axes[1, 1]
    ax.axis("off")
    ax.text(
        0.5,
        0.92,
        "Rappel : que signifient r et rho ?",
        ha="center",
        fontsize=12,
        fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.05,
        0.72,
        "• Pearson (r) : mesure si les points sont proches d’une droite\n"
        "  (relation linéaire). r = +1 ou −1 = alignement fort ; r ≈ 0 = pas de droite.",
        fontsize=10,
        transform=ax.transAxes,
        va="top",
        family="sans-serif",
    )
    ax.text(
        0.05,
        0.42,
        "• Spearman (ρ, « rho ») : on remplace les valeurs par leurs rangs\n"
        "  (1er, 2e, 3e…), puis on mesure une association « en ordre ».\n"
        "  Utile pour les scores ordinaux ou les formes non droites mais monotones.",
        fontsize=10,
        transform=ax.transAxes,
        va="top",
        family="sans-serif",
    )
    ax.text(
        0.05,
        0.12,
        "Les deux indices sont entre −1 et +1, mais ne répondent pas à la même question.",
        fontsize=10,
        style="italic",
        transform=ax.transAxes,
        va="top",
        color="#334155",
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out1 = os.path.join(fig_dir, "Fig_corr_pearson_spearman.png")
    fig1.savefig(out1, dpi=200, bbox_inches="tight", facecolor=fig1.patch.get_facecolor())
    plt.close(fig1)
    print(f"Écrit : {out1}")

    fig2, ax = plt.subplots(figsize=(10, 6))
    fig2.patch.set_facecolor("#fafafa")
    age = RNG.integers(8, 19, 120)
    shoe = 2.1 * age + RNG.normal(0, 1.2, 120)
    reading = 4.0 * age + RNG.normal(0, 4, 120)
    r_pb = pearson_r(shoe, reading)
    ax.scatter(shoe, reading, alpha=0.55, c="#7c3aed", edgecolors="white", s=42)
    ax.set_xlabel("Pointure (simulée)")
    ax.set_ylabel("Score de lecture (simule)")
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.set_title(
        "Corrélation forte entre deux variables… sans lien direct de cause à effet\n"
        f"r (Pearson) ≈ {r_pb:.2f}  —  Les deux augmentent avec l’âge (variable non affichée ici)",
        fontsize=11,
        fontweight="bold",
    )
    ax.text(
        0.02,
        0.98,
        "Exemple pédagogique classique : pointure et lecture sont corrélées chez les enfants\n"
        "parce que les deux « montent » avec l’âge — pas parce que la chaussure cause la lecture.",
        transform=ax.transAxes,
        fontsize=10,
        va="top",
        bbox=dict(boxstyle="round", facecolor="#f1f5f9", edgecolor="#cbd5e1", alpha=0.95),
    )
    plt.tight_layout()
    out2 = os.path.join(fig_dir, "Fig_corr_facteur_commun.png")
    fig2.savefig(out2, dpi=200, bbox_inches="tight", facecolor=fig2.patch.get_facecolor())
    plt.close(fig2)
    print(f"Écrit : {out2}")


if __name__ == "__main__":
    main()
