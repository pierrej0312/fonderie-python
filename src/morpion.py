#Morpion
import random

def creer_grille():
        return[[" " for j in range (3)] for i in range(3)]

def affichage_grille(grille) :
    print("    0   1   2")
    for i in range(3) :
        print(i, " ", " | ".join(grille[i]))
        if i<2 :
            print("   ---+---+---")

# grille = creer_grille()
# affichage_grille(grille)

def placer_symbole(grille, ligne, colonne, symbole) :
    if not(0 <= ligne < 3 and 0 <= colonne < 3) :
        return False
    
    if grille[ligne][colonne] != " " :
        return False
    
    grille[ligne][colonne] = symbole
    
    return True

def Verif_victoire(grille, symbole):
    #Verification des lignes
    for i in range(3) :
        if grille[i][0] == grille[i][1] == grille[i][2] == symbole :
            return True
        
    #Verification des colonnes
    for j in range(3) :
        if grille[0][j] == grille[1][j] == grille[2][j] == symbole :
            return True
        
    #Verification diagolane principale
    for k in range(3) :
        if grille[0][0] == grille[1][1] == grille[2][2] == symbole :
            return True
    
    #Verification diagonale secondaire
    for l in range(3) :
        if grille[0][2] == grille [1][1] == grille [2][0] == symbole :
            return True

    return False

def grille_pleine(grille) :
    
    for ligne in grille :
        for case in ligne :
            if case == " " :
                return False
    
    return True

#Je code CHATGPT pour atomiser les joueurs
def cases_libres(grille) :
    libre = []
    
    for i in range(3) :
        for j in range(3) :
            if grille[i][j] == " " :
                libre.append((i,j))
    return libre

def coup_gagnant(grille, symbole):
    coups = []

    for ligne, colonne in cases_libres(grille):

        grille[ligne][colonne] = symbole

        if Verif_victoire(grille, symbole):
            coups.append((ligne, colonne))

        grille[ligne][colonne] = " "

    return coups

#IA DE niveau 0 :
def ia_lvl_0(grille) :
    libres = cases_libres(grille)
    
    if libres :
        return random.choice(libres)
    
    return None

#IA de niveau 1 (offensive)
def ia_lvl_1(grille, symbole="O") :
    coup = coup_gagnant(grille, symbole)
    if coup :
        return random.choice(coup)
    
    return ia_lvl_0(grille)

def ia_lvl_2(grille, symbole="O") :
    adversaire = "X" if symbole =="O" else "O"
    
    #Chercher une victoire immédiate
    coup = coup_gagnant(grille, symbole)
    if coup :
        return random.choice(coup)
    
    coups_surs = []
    for ligne, colonne in cases_libres(grille) :
        #Simulation du coup par l'IA
        grille[ligne][colonne] = symbole
        
        #Verifier si l'adversaire peut gagner
        menace = coup_gagnant(grille, adversaire)
        
        #annulation coup
        grille[ligne][colonne] = " "
        
        if menace is None :
            coups_surs.append((ligne, colonne))
    #Jouer parmi les coups gagnants sans danger
    if coups_surs :
        return random.choice(coups_surs)
    
    #Si la défaite est inévitable au prochain tour
    return ia_lvl_0(grille)

def trouver_fourchettes(grille, symbole):
    fourchettes = []

    for ligne, colonne in cases_libres(grille):

        grille[ligne][colonne] = symbole

        if len(coup_gagnant(grille, symbole)) >= 2:
            fourchettes.append((ligne, colonne))

        grille[ligne][colonne] = " "

    return fourchettes

def MinMax(grille, maximisation, profondeur = 0) :
    #Cas de base
    if Verif_victoire(grille, "O") :
        return 10 - profondeur
    if Verif_victoire(grille, "X") :
        return profondeur - 10
    if grille_pleine(grille) : 
        return 0
    if maximisation :
        meilleur_score = -float("inf")
        
        for lignes, colonnes in cases_libres(grille) :
            grille[lignes][colonnes] ="O"
            score = MinMax(grille, False, profondeur+1)
            grille[lignes][colonnes] = " "
            meilleur_score = max(meilleur_score, score)
        return meilleur_score
    
    else :
        meilleur_score = float("inf")
        
        for ligne, colonne in cases_libres(grille) :
            grille[ligne][colonne] ="X"
            score = MinMax(grille, True, profondeur+1)
            grille[ligne][colonne]=" "
            meilleur_score = min(meilleur_score, score)
        return meilleur_score
    
def ia_minmax(grille) :
    meilleur_score = -float("inf")
    meilleur_coup = []
    
    for ligne, colonne in cases_libres(grille) :
        grille[ligne][colonne] = "O"
        score = MinMax(grille, False, 1)
        grille[ligne][colonne] = " "
        
        if score > meilleur_score :
            meilleur_score = score
            meilleur_coup = [(ligne, colonne)]
        elif score == meilleur_score :
            meilleur_coup.append((ligne, colonne))
    
    if meilleur_coup :
        return random.choice(meilleur_coup)
    
    return None

def coups_sans_fourchette(grille, symbole="O") :
    adversaire = "X" if symbole =="O" else "O"
    coups_surs = []
    
    for ligne, colonne in cases_libres(grille) :
        grille[ligne][colonne] = symbole
        danger = False
        
        for i, j in cases_libres(grille) :
            grille[i][j] = adversaire
            if Verif_victoire(grille, adversaire) :
                danger = True
            elif not coup_gagnant(grille, symbole) :
                if len(coup_gagnant(grille, adversaire)) >= 2 :
                    danger = True
            grille [i][j] = " "
            if danger :
                break
        grille[ligne][colonne] = " "
        
        if not danger :
            coups_surs.append((ligne, colonne))
    return coups_surs

def ia_lvl_3(grille, symbole="O") :
    adversaire = "X" if symbole=="O" else "O"
    
    #1. Gagner immédiatemment
    coup = coup_gagnant(grille, symbole)
    if coup : 
        return random.choice(coup)
    
    #2. Bloquer une victoire adverse 
    coup = coup_gagnant(grille, adversaire)
    if coup :
        return random.choice(coup)
    
    #3. Créer une fourchette
    fourchette = trouver_fourchettes(grille, symbole)
    if fourchette :
        return random.choice(fourchette)
    
    #4. Empêcher les fourchettes adverses
    coups_surs = coups_sans_fourchette(grille, symbole)
    if coups_surs : 
        return random.choice(coups_surs)

    #5. Revenir à la stratégie de niveau inférieur
    return ia_lvl_2(grille, symbole)

def coins_libres(grille) : 
    coins =[(0,0), (0,2),(2,0),(2,2)]
    return[(i,j) for i, j in coins if grille[i][j] == " "]

def coins_opposes(grille, adversaire) :
    coins =[(0,0), (0,2),(2,0),(2,2)]
    dispos = []
    
    for i, j in coins : 
        if grille[i][j] == adversaire :
            if grille[2-i][2-j] == " ":
                dispos.append((2-i,2-j))
    return dispos

def ia_lvl_4(grille, symbole = "O") :
    adversaire = "X" if symbole=="O" else "O"
    
    #1. Gagner
    coup = coup_gagnant(grille, symbole)
    
    if coup :
        return random.choice(coup)
    
    #2. Bloquer 
    coup = coup_gagnant(grille, adversaire)
    if coup :
        return random.choice(coup)
    
    #3. Créer une fourchette 
    fourchette = trouver_fourchettes(grille, symbole)
    if fourchette :
        return random.choice(fourchette)
    #4. Sélectionner les coups sans danger
    coups_surs = coups_sans_fourchette(grille, symbole)
    if not coups_surs :
        return ia_lvl_2(grille, symbole)
    
    #5. Privilégier le centre 
    if (1,1) in coups_surs :
        return(1,1)
    #6. Privilégier les coins opposés 
    for coup in coins_opposes(grille, adversaire) :
        if coup in coups_surs :
            return coup
    
    #7. Privilégier les coins libres :
    coins = [coup for coup in coins_libres(grille) if coup in coups_surs]
    if coins :
        return random.choice(coins)
    
    #8. Jouer un autre coup sûr
    return random.choice(coups_surs)
    
def jouer_ia(grille, niveau, symbole="O") :
    
    premier_coup = not any(symbole in ligne for ligne in grille)
    grille_vide = len(cases_libres(grille)) == 9

    #MinMax doit pouvoir choisir librement
    if niveau == 5 : 
       return ia_minmax(grille)
    
    #Ouverture stratégiques 
    if niveau >=2 and grille_vide :
        return random.choice(coins_libres(grille))
    if niveau >=2 and premier_coup and grille[1][1] == " " :
        return(1,1)
    
    #Selection du niveau
    if niveau == 0 :
        return ia_lvl_0(grille)
    elif niveau == 1 :
        return ia_lvl_1(grille, symbole)
    elif niveau == 2 : 
        return ia_lvl_2(grille, symbole)
    elif niveau == 3 :
        return ia_lvl_3(grille, symbole)
    elif niveau == 4 : 
        return ia_lvl_4(grille, symbole)
    else :
        raise ValueError("Niveau de difficulté inconnu...")

def Jeu() :
    grille = creer_grille()
    joueur = random.choice(["X", "O"])

    print("0 - Aléatoire")
    print("1 - Offensive")
    print("2 - Défensive")
    print("3 - Tactique")
    print("4 - Stratégique")
    print("5 - Expert")
    
    niveau = int(input("Choisissez la difficulté : "))
    
    if joueur == "X":
        print("Vous commencez la partie !")
    else:
        print("L'ordinateur commence la partie !")
        
    if niveau not in range(6) :
        print("Niveau invalide")
        return
    
    while True : 
        affichage_grille(grille)
        if joueur == "X" :
            print("A votre tour !")
            try :
                ligne = int(input("Ligne : "))
                colonne = int(input("Colonne : "))
            except ValueError :
                print("Veuillez entrer des nombres entiers.")
                continue
        
        else :
            print ("Au tour de l'IA !")
            ligne, colonne = jouer_ia(grille, niveau, joueur)
            print (f"L'IA joue en ({ligne}, {colonne})")
            
        if not placer_symbole(grille, ligne, colonne, joueur) :
            print("Case occupée ou coordonnées invalides !")
            continue
        
        if Verif_victoire(grille, joueur) :
            affichage_grille(grille)
            print(f"Le joueur {joueur} a gagné !")
            break
        
        if grille_pleine(grille) :
            affichage_grille(grille)
            print("Match nul !")
            break
        
        joueur = "O" if joueur == "X" else "X"
        
def simuler_partie(niveau_X, niveau_O):

    grille = creer_grille()
    joueur = random.choice(["X", "O"])
    tour = 0

    while True:

        tour += 1
        niveau = niveau_X if joueur == "X" else niveau_O

        coup = jouer_ia(grille, niveau, joueur)

        print(f"Tour : {tour}")
        print(f"Joueur : {joueur}")
        print(f"Niveau : {niveau}")
        print(f"Coup proposé : {coup}")

        if not isinstance(coup, tuple) or len(coup) != 2:
            raise TypeError(f"Coup incorrect : {coup}")

        if coup not in cases_libres(grille):
            affichage_grille(grille)

            raise ValueError(
                f"L'IA {joueur} de niveau {niveau} "
                f"a proposé un coup interdit : {coup}"
            )

        ligne, colonne = coup

        placer_symbole(grille, ligne, colonne, joueur)

        if Verif_victoire(grille, joueur):
            return joueur

        if grille_pleine(grille):
            return "Nul"

        joueur = "O" if joueur == "X" else "X"
        
def tournoi(niveau_X, niveau_O, nombre_parties):

    resultats = {
        "X": 0,
        "O": 0,
        "Nul": 0
    }

    for i in range(nombre_parties):

        gagnant = simuler_partie(niveau_X, niveau_O)

        resultats[gagnant] += 1

    return resultats

def afficher_resultats(resultats):

    total = sum(resultats.values())

    if total == 0:
        return

    for joueur, nombre in resultats.items():

        pourcentage = nombre / total * 100

        print(f"{joueur} : {nombre} ({pourcentage:.2f} %)")
        
def menu_principal():

    while True:

        print("\n===== MORPION =====")
        print("1 - Jouer contre l'IA")
        print("2 - Simuler une partie entre IA")
        print("3 - Organiser un tournoi")
        print("0 - Quitter")

        choix = input("Votre choix : ")

        try:

            if choix == "1":
                Jeu()

            elif choix == "2":

                niveau_X = int(input("Niveau de X : "))
                niveau_O = int(input("Niveau de O : "))

                resultat = simuler_partie(niveau_X, niveau_O)

                print("Résultat :", resultat)

            elif choix == "3":

                niveau_X = int(input("Niveau de X : "))
                niveau_O = int(input("Niveau de O : "))
                nombre = int(input("Nombre de parties : "))

                resultats = tournoi(niveau_X, niveau_O, nombre)

                afficher_resultats(resultats)

            elif choix == "0":
                break

            else:
                print("Choix invalide.")

        except ValueError as erreur:
            print(f"Erreur : {erreur}")
            raise

if __name__ == "__main__":
    menu_principal()