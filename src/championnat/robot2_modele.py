"""Votre robot de combat · génération 2, machine learning. Auteur : (votre prénom ou un pseudo)

Les règles de ce robot ne sont pas écrites à l'intuition : elles viennent d'un arbre de décision entraîné sur les
décisions des robots d'entraînement qui ont gagné (notebook robot2_arbre.ipynb). La fonction arbre_en_code(arbre)
écrit l'arbre en if / else ; collez ses lignes sous « # COLLEZ ICI ». Elles utilisent les nombres calculés au début.
"""
import regles


def strategie(etat):
    adv = etat["adversaire"]
    distance = etat["distance"]
    vie_moi, vie_adversaire = etat["moi"]["vie"], adv["vie"]
    energie_moi, energie_adversaire = etat["moi"]["energie"], adv["energie"]
    bord_moi, bord_adversaire = etat["moi"]["bord_derriere"], adv["bord_derriere"]
    adv_prepare = 1 if adv["phase"] == "preparation" else 0
    adv_frappe = 1 if adv["phase"] == "frappe" else 0
    adv_recupere = 1 if adv["phase"] == "recuperation" else 0
    adv_garde = 1 if adv["phase"] == "garde" else 0
    adv_garde_basse = 1 if adv["phase"] == "garde_basse" else 0
    adv_sonne = 1 if adv["phase"] == "sonne" else 0
    adv_reste = adv["reste"]
    # le coup que l'adversaire prépare, frappe ou finit : 1 pour ce coup, 0 pour les autres
    adv_direct = 1 if adv["action"] == "direct" else 0
    adv_crochet = 1 if adv["action"] == "crochet" else 0
    adv_coup_bas = 1 if adv["action"] == "coup_bas" else 0
    adv_projection = 1 if adv["action"] == "projection" else 0
    adv_special = 1 if adv["action"] == "special" else 0

    action = "garde"            # l'action par défaut, tant que rien n'est collé
    # COLLEZ ICI les lignes écrites par arbre_en_code(arbre) : curseur tout au début de la ligne vide
    # ci-dessous (colonne 1), sans espace devant ; les lignes collées ont déjà leur retrait.

    # sécurité : une action trop chère est refusée, et le robot perdrait l'instant
    cout = regles.COUPS[action]["energie"] if action in regles.COUPS else regles.ESQUIVE["energie"] if action == "esquive" else 0
    if cout > energie_moi:
        action = "garde"
    return action
