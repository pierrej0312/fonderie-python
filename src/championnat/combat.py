"""Faites combattre votre robot (mon_robot.py) contre les robots d'entraînement.

    python combat.py                         bilan contre les six robots d'entraînement, en A puis en B
    python combat.py mur                     un combat contre mur : les moments forts, et combat.json à revoir en 3D
    python combat.py mur --journal mur.csv   le même, et son journal en CSV (une ligne par instant)
    python combat.py --robot robot2.py       un autre fichier que mon_robot.py (robots 2 et 3)

Pour voir le combat en 3D : ouvrez le jeu en ligne, page « Le championnat des robots », bouton « Revoir un combat »,
et choisissez combat.json.
"""
import importlib.util
import sys
from pathlib import Path

import regles as R
from moteur import combattre, ecrire_journal, ecrire_rejeu
from robots_entrainement import adversaires

EFFETS = {"touche": "touche", "contre": "touche en contre", "bloque": "est bloqué", "esquive": "est esquivé", "rate": "frappe dans le vide"}


def charger(chemin="mon_robot.py"):
    """Charge la fonction strategie d'un fichier .py."""
    spec = importlib.util.spec_from_file_location("robot_joueur", chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "strategie"):
        sys.exit(f"{chemin} ne contient pas de fonction strategie(etat).")
    return module.strategie


def raconter(resultat, nom_a, nom_b):
    """Les moments forts : chaque coup qui frappe, chaque action refusée, la fin."""
    print(f"A = {nom_a}   B = {nom_b}")
    refus = {"a": 0, "b": 0}
    for l in resultat["journal"]:
        for cote, nom in (("a", nom_a), ("b", nom_b)):
            if not l[f"valide_{cote}"]:
                refus[cote] += 1
                if refus[cote] <= 3:
                    print(f"{l['tick'] / R.TICKS_PAR_SECONDE:5.1f} s  {nom} : « {l[f'decision_{cote}']} » refusé ({l[f'raison_{cote}']})")
            effet = l[f"effet_{cote}"]
            if effet:
                coup = "le " + l[f"action_{cote}"] if effet == "rate" else f"son {l[f'action_{cote}'] or 'coup'}"
                d = f", {l[f'degats_{cote}']} de dégâts" if l[f"degats_{cote}"] else ""
                print(f"{l['tick'] / R.TICKS_PAR_SECONDE:5.1f} s  {nom} : {coup} {EFFETS[effet]}{d}   (vie A {l['vie_a']}, B {l['vie_b']})")
    for cote, nom in (("a", nom_a), ("b", nom_b)):
        if refus[cote] > 3:
            print(f"        {nom} : {refus[cote]} actions refusées en tout")
    fin = resultat["journal"][-1]
    qui = {"a": f"A ({nom_a})", "b": f"B ({nom_b})", "egalite": "égalité"}[resultat["vainqueur"]]
    comment = "K.-O." if resultat["fin"] == "ko" else f"fin du temps, vie {fin['vie_a']} contre {fin['vie_b']}"
    print(f"Résultat : {qui} ({comment}, {fin['tick'] / R.TICKS_PAR_SECONDE:.1f} s).")


def bilan(ma_strategie):
    print(f"{'adversaire':<10}  {'vous en A':<26}  {'vous en B':<26}")
    victoires = 0
    for nom in adversaires():
        r1 = combattre(ma_strategie, adversaires()[nom], "vous", nom)
        r2 = combattre(adversaires()[nom], ma_strategie, nom, "vous")
        f1, f2 = r1["journal"][-1], r2["journal"][-1]
        en_a = {"a": "gagné", "b": "perdu", "egalite": "égalité"}[r1["vainqueur"]] + f" ({f1['vie_a']} à {f1['vie_b']})"
        en_b = {"b": "gagné", "a": "perdu", "egalite": "égalité"}[r2["vainqueur"]] + f" ({f2['vie_b']} à {f2['vie_a']})"
        victoires += (r1["vainqueur"] == "a") + (r2["vainqueur"] == "b")
        print(f"{nom:<10}  {en_a:<26}  {en_b:<26}")
    print(f"Victoires : {victoires} sur {2 * len(adversaires())}. Revoyez un combat : python combat.py <adversaire>")


if __name__ == "__main__":
    dossier = Path(__file__).resolve().parent
    args = sys.argv[1:]
    fichier = "mon_robot.py"
    if "--robot" in args:
        i = args.index("--robot")
        fichier = args[i + 1]
        del args[i:i + 2]
    ma_strategie = charger(dossier / fichier)
    if not args or args[0].startswith("--"):
        bilan(ma_strategie)
    else:
        nom = args[0]
        if nom not in adversaires():
            sys.exit(f"Pas de robot d'entraînement nommé {nom}. Choisissez parmi : {', '.join(adversaires())}")
        resultat = combattre(ma_strategie, adversaires()[nom], "vous", nom)
        raconter(resultat, "vous", nom)
        ecrire_rejeu(resultat, "vous", nom, dossier / "combat.json")
        print("Combat enregistré dans combat.json : revoyez-le en 3D dans le jeu en ligne (bouton « Revoir un combat »).")
        if "--journal" in args:
            chemin = args[args.index("--journal") + 1]
            ecrire_journal(resultat["journal"], chemin)
            print(f"Journal de {len(resultat['journal'])} instants enregistré : {chemin}")
