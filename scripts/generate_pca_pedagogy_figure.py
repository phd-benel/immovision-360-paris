"""
Figure pédagogique : plan PCA (7D -> 2D) avec deux scénarios — séparation visible vs nuage homogène.
Dépendances : numpy, matplotlib uniquement.
Usage : python scripts/generate_pca_pedagogy_figure.py
Sortie : Figures/Fig_pca_interpretation.png
"""
from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np

RNG = np.random.default_rng(2026)


def pca_project_2d(X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Centrage + SVD : projection sur les 2 premières composantes."""
    X = np.asarray(X, dtype=float)
    Xc = X - X.mean(axis=0)
    _, _, vt = np.linalg.svd(Xc, full_matrices=False)
    # Composantes principales = colonnes de Vt.T
    components = vt.T[:, :2]
    Z = Xc @ components
    # Variance expliquée approximative (pour affichage)
    var = np.var(Xc @ vt.T[:, 0]) + np.var(Xc @ vt.T[:, 1])
    total = np.sum(np.var(Xc, axis=0))
    ratio = var / total if total > 0 else 0.0
    return Z, np.array([ratio, ratio])  # simplifié pour l'affichage


def main() -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "Figures", "Fig_pca_interpretation.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2))
    fig.patch.set_facecolor("#fafafa")
    fig.suptitle(
        "ACP (PCA) : passer de plusieurs colonnes à un plan en 2D — deux lectures possibles",
        fontsize=13,
        fontweight="bold",
        y=1.02,
    )

    # --- Gauche : deux groupes séparés dans l'espace des features (ex. profils différents) ---
    n_a, n_b = 90, 110
    dim = 7
    shift = np.array([2.8, 1.5, 1.2, 1.0, 0.9, 0.8, 0.7])
    A = RNG.normal(0, 0.85, (n_a, dim))
    B = RNG.normal(0, 0.85, (n_b, dim)) + shift
    X = np.vstack([A, B])
    Z, _ = pca_project_2d(X)
    lab = np.array([0] * n_a + [1] * n_b)

    ax = axes[0]
    ax.scatter(
        Z[lab == 0, 0],
        Z[lab == 0, 1],
        alpha=0.65,
        c="#2563eb",
        s=36,
        label="Groupe A (ex. « profil 1 »)",
        edgecolors="white",
        linewidths=0.3,
    )
    ax.scatter(
        Z[lab == 1, 0],
        Z[lab == 1, 1],
        alpha=0.65,
        c="#059669",
        s=36,
        label="Groupe B (ex. « profil 2 »)",
        edgecolors="white",
        linewidths=0.3,
    )
    ax.set_xlabel("Première composante (PC1)")
    ax.set_ylabel("Deuxième composante (PC2)")
    ax.set_title(
        "Scénario 1 — Deux nuages séparés\n"
        "(les points se regroupent en deux zones : interprétation « deux familles » possible)",
        fontsize=10,
        loc="left",
    )
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.set_facecolor("#ffffff")

    # --- Droite : un seul mélange (pas de structure en deux clusters) ---
    Y = RNG.normal(0, 1, (220, dim))
    W, _ = pca_project_2d(Y)
    ax = axes[1]
    ax.scatter(W[:, 0], W[:, 1], alpha=0.45, c="#64748b", s=32, edgecolors="white", linewidths=0.2)
    ax.set_xlabel("Première composante (PC1)")
    ax.set_ylabel("Deuxième composante (PC2)")
    ax.set_title(
        "Scénario 2 — Un seul nuage sans coupure nette\n"
        "(forcer « deux clusters » serait artificiel : l'ACP ne crée pas des groupes, elle projette)",
        fontsize=10,
        loc="left",
    )
    ax.grid(True, alpha=0.25, linestyle="--")
    ax.set_facecolor("#ffffff")

    plt.tight_layout()
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=fig.patch.get_facecolor())
    plt.close(fig)
    print(f"Écrit : {out}")


if __name__ == "__main__":
    main()
