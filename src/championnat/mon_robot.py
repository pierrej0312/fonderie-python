"""Votre robot de combat. Auteur : (votre prénom ou un pseudo)

Votre robot est la fonction strategie(etat). Le moteur l'appelle à chaque instant où votre robot est libre
(10 fois par seconde au plus) ; elle renvoie une action :
"attendre", "avancer", "reculer", "garde", "garde_basse", "direct", "crochet", "coup_bas", "projection", "esquive"
ou "special". Les coups, leurs temps de préparation, leur portée, leur coût en énergie et ce que bloque chaque garde
sont dans regles.py.

Ce que contient etat (un exemple) :
    etat["distance"]                    140    cm entre les deux robots
    etat["moi"]["vie"]                  100
    etat["moi"]["energie"]               50    un coup coûte de l'énergie ; elle revient de 1 par instant
    etat["moi"]["bord_derriere"]        350    cm jusqu'aux cordes derrière vous
    etat["adversaire"]["action"]   "crochet"   ce qu'il fait : un coup, "garde", "garde_basse", "avancer",
                                               "reculer", "esquive", "sonne" ou "rien"
    etat["adversaire"]["phase"] "preparation"  "preparation", "frappe", "recuperation", "sonne", "garde",
                                               "garde_basse"... ou "libre"
    etat["adversaire"]["reste"]           3    instants avant la fin de sa phase
    etat["adversaire"]["vie"], ["energie"], ["bord_derriere"]
    etat["dernier_coup_adversaire"] "direct"   le dernier coup qu'il a lancé (None au début)
    etat["temps"]                       12.3   secondes depuis le début
"""


def strategie(etat):
    if etat["distance"] <= 160:
        return "direct"
    return "avancer"
