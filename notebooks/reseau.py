"""dessiner_reseau(modele, entrees) : dessine un réseau de neurones entraîné par scikit-learn.

Un rond par neurone, un trait par poids : orange si le poids est positif, bleu s'il est négatif (comme dans le labo des neurones),
d'autant plus épais que le poids est grand. Accepte un MLPRegressor ou un pipeline qui se termine par un MLPRegressor.
"""
import matplotlib.pyplot as plt


def dessiner_reseau(modele, entrees=None):
    reseau = modele[-1] if hasattr(modele, "steps") else modele      # dans un pipeline, le réseau est la dernière étape
    tailles = [reseau.coefs_[0].shape[0]] + [poids.shape[1] for poids in reseau.coefs_]
    plus_grand = max(abs(p) for poids in reseau.coefs_ for ligne in poids for p in ligne)

    def place(couche, i):                                             # neurones centrés verticalement
        return couche, (tailles[couche] - 1) / 2 - i

    fig, ax = plt.subplots(figsize=(7.7, 6), dpi=150)
    for couche, poids in enumerate(reseau.coefs_):
        for i, ligne in enumerate(poids):
            for j, p in enumerate(ligne):
                (x1, y1), (x2, y2) = place(couche, i), place(couche + 1, j)
                ax.plot([x1, x2], [y1, y2], color="tab:orange" if p > 0 else "tab:blue",
                        linewidth=0.3 + 4 * abs(p) / plus_grand, zorder=1)
    for couche, n in enumerate(tailles):
        for i in range(n):
            x, y = place(couche, i)
            ax.scatter(x, y, s=300, color="white", edgecolors="black", zorder=2)
    if entrees:
        for i, nom in enumerate(entrees):
            ax.text(-0.15, place(0, i)[1], nom, ha="right", va="center")
    ax.text(len(tailles) - 1 + 0.15, 0, "prévision", ha="left", va="center")
    ax.set_title(f"Réseau {' → '.join(str(t) for t in tailles)} · orange : poids positif, bleu : négatif")
    ax.axis("off")
    plt.show()
