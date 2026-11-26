"""Fabrique les données d'entraînement du robot 2 : des centaines de combats entre les robots d'entraînement.

    python donnees_apprentissage.py            écrit decisions.csv (une ligne par décision d'un robot)

Chaque ligne : ce que le robot voyait (les dix-neuf nombres d'apprentissage.py), l'action qu'il a choisie, et l'issue
du combat pour lui (gagne, perdu, egalite). Pour apprendre « ce que font les gagnants », on garde les lignes gagne.
Vos combats joués au clavier (bouton « Télécharger mes combats » du jeu) ont les mêmes colonnes : on peut les ajouter.

Pour varier les situations, les robots d'entraînement jouent parfois un coup au hasard (10 % ou 25 % des décisions).
Graine fixe : le fichier est le même à chaque fois.
"""
import csv

import regles as R
from apprentissage import CARACTERISTIQUES, caracteristiques
from moteur import combattre
from robots_entrainement import REFERENCES, Hasard, peut

COLONNES = ["combat_id", "tick", "robot", "adversaire", *CARACTERISTIQUES, "action", "valide", "issue", "fin", "joueur"]


def espionne(strategie, bruit, hasard, carnet):
    """Enveloppe une stratégie : note chaque décision (ce que voyait le robot, l'action) ; joue parfois au hasard."""
    def jouer(etat):
        if hasard.suivant() < bruit:
            possibles = [a for a in R.ACTIONS if peut(etat, a)]
            action = possibles[int(hasard.suivant() * len(possibles))]
        else:
            action = strategie(etat)
        carnet.append((etat["tick"], caracteristiques(etat), action))
        return action
    return jouer


def produire(chemin="decisions.csv", graines=6):
    hasard = Hasard(R.TICKS_PAR_SECONDE * 2026)
    lignes, n = [], 0
    noms = list(REFERENCES)
    for bruit in (0.0, 0.10, 0.25):
        for g in range(graines if bruit else 1):
            for na in noms:
                for nb in noms:
                    carnet_a, carnet_b = [], []
                    cid = f"{na}-vs-{nb}-b{int(bruit * 100)}-{g}"
                    r = combattre(espionne(REFERENCES[na], bruit, hasard, carnet_a), espionne(REFERENCES[nb], bruit, hasard, carnet_b), na, nb, cid)
                    n += 1
                    issue = {"a": ("gagne", "perdu"), "b": ("perdu", "gagne"), "egalite": ("egalite", "egalite")}[r["vainqueur"]]
                    valides = {(l["tick"], c): l[f"valide_{c}"] for l in r["journal"] for c in ("a", "b")}
                    for cote, carnet, nom, autre, iss in (("a", carnet_a, na, nb, issue[0]), ("b", carnet_b, nb, na, issue[1])):
                        for tick, c, action in carnet:
                            lignes.append([cid, tick, nom, autre, *c, action, valides[(tick, cote)], iss, r["fin"], 0])
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(COLONNES)
        w.writerows(lignes)
    return n, len(lignes)


if __name__ == "__main__":
    combats, decisions = produire()
    print(f"{combats} combats, {decisions} décisions : decisions.csv")
