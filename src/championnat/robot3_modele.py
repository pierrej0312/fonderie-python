"""Votre robot de combat · génération 3, réseau de neurones. Auteur : (votre prénom ou un pseudo)

Le cerveau de ce robot est un réseau de neurones entraîné en combattant dans le labo des neurones (stratégie d'évolution) : il a joué des
milliers de combats et a gardé ce qui fait gagner. Collez la ligne « CERVEAU = {...} » exportée par le labo à la place
de « CERVEAU = None ». La stratégie fait le calcul couche par couche, avec la fonction neurone.
"""
import regles

CERVEAU = None

ECHELLES = [1000, 100, 100, 100, 100, 1000, 1000, 1, 1, 1, 1, 1, 1, 10, 1, 1, 1, 1, 1]


def neurone(entrees, poids, biais):
    return sum(e * p for e, p in zip(entrees, poids)) + biais


def caracteristiques(etat):
    """Les dix-neuf nombres que voit le robot : les mêmes qu'à l'entraînement, dans le même ordre."""
    adv = etat["adversaire"]
    phase = adv["phase"]
    return [etat["distance"], etat["moi"]["vie"], adv["vie"], etat["moi"]["energie"], adv["energie"],
            etat["moi"]["bord_derriere"], adv["bord_derriere"],
            1 if phase == "preparation" else 0, 1 if phase == "frappe" else 0, 1 if phase == "recuperation" else 0,
            1 if phase == "garde" else 0, 1 if phase == "garde_basse" else 0, 1 if phase == "sonne" else 0, adv["reste"],
            *[1 if adv["action"] == coup else 0 for coup in ["direct", "crochet", "coup_bas", "projection", "special"]]]


def cout(action):
    if action in regles.COUPS:
        return regles.COUPS[action]["energie"]
    return regles.ESQUIVE["energie"] if action == "esquive" else 0


def strategie(etat):
    if CERVEAU is None:
        return "garde"
    valeurs = [x / e for x, e in zip(caracteristiques(etat), ECHELLES)]
    couches = CERVEAU["couches"]
    for numero, couche in enumerate(couches):
        valeurs = [neurone(valeurs, poids, biais) for poids, biais in couche]
        if numero < len(couches) - 1:
            valeurs = [max(0, v) for v in valeurs]              # ReLU sur les couches cachées
    # l'action la mieux notée parmi celles que le robot peut payer
    possibles = [i for i, a in enumerate(CERVEAU["actions"]) if cout(a) <= etat["moi"]["energie"]]
    meilleure = max(possibles, key=lambda i: valeurs[i])
    return CERVEAU["actions"][meilleure]
