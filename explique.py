# Créer une base de données 'sudoku' et implimenter un programme python (avec pygame et d'autres packages de python)
# Le sudoku se joue sur une grille de 9x9, elle-même divisée en neuf sous-grilles
# de 3x3. L'objectif du jeu est de remplir toute la grille avec des chiffres de 1 à 9,
# sans répéter aucun chiffre dans la même ligne, la même colonne ou la même
# sous-grille.
# Bien que le jeu puisse sembler intimidant au premier abord, il existe de
# nombreuses techniques et stratégies pour résoudre les grilles de Sudoku,
# allant de la simple élimination des possibilités à un raisonnement logique
# plus complexe.

# Étant intrigué par ce fameux jeu, et voulant faire honneur à Euler, à Garns et à
# Kaji, vous décidez de développer un outil de résolution de Sudoku !

# Après avoir fait une recherche longue sur les nombreuses techniques de
# résolution existantes, vous testez les stratégies suivantes :
# 1. La méthode de la force brute : il vérifie toutes les combinaisons de
# chiffres possible de 1 à 9 jusqu'à ce qu'une solution du sudoku soit
# trouvée.
# 2. La méthode du Backtracking : il fonctionne en choisissant une case
# vide et en essayant tous les chiffres possibles de 1 à 9. Si un chiffre entre
# en conflit avec les règles du Sudoku, l'algorithme revient, par
# récursivité, à la case précédemment remplie et essaie le chiffre suivant. 
# Ce processus est répété jusqu'à ce que le Sudoku soit résolu.
# Le code doit être propre et orienté objet. 

# Vous devrez étudier la complexité algorithmique de 2 méthodes et temps d'exécution.
# Comparez ces deux critères sous forme de tableau. Quelles sont vos
# observations ? Concluez sur l'algorithme le plus performant parmi les 2
# étudiés. Cette analyse doit être proprement rédigée dans un fichier de type Markdown.

# Votre programme doit prendre en input le nom d’un fichier, contenant la
# grille de Sudoku à résoudre, vous avez à votre disposition 5 exemples de Sudoku de pour différentes
# difficultés qu'il faudra bien sûr résoudre, accessibles ci-contre : 
# exemple 1:
# _729___3_
# __1__6_8_
# ____4__6_
# 96___41_8
# _487_5_96
# __56_8__3
# ___4_2_1_
# 85__6_327
# 1__85____

# exemple 2:
# 7__92_4__
# ______7__
# __4__8312
# 4____25__
# 2___1___3
# __85____4
# 8432__6__
# __5______
# __2_64__5

# exemple 3:
# __9_85_63
# _7_96____
# 5_1__4___
# __67_3__4
# _4_21_39_
# 8___9__57
# 9845__6__
# __7649_3_
# 61__2__4_

# exemple 4:
# 3______8_
# 1__6_3__2
# 56_______
# _8_1__97_
# ___5_____
# 2_9__4___
# __1___62_
# _______43
# _7__5_1__

# exemple 5:
# __9_6____
# ___3___1_
# _45_1___6
# _____82__
# _61_3___5
# 7________
# 9___4____
# _742__5__
# 3_______7

# Affichage...
# Le résultat doit être affiché sur votre terminal, en s’assurant qu’il soit
# possible de distinguer les valeurs présentes à l’origine dans la grille de celles
# ajoutées par l’algorithme.
# Fiers de votre outil, vous faites un second affichage, plus esthétique de votre
# outil, à l'aide de la librairie Pygame.