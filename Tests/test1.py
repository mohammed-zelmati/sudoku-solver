import itertools
import time

def verifier_solution(grille):
    # Vérifie si une solution respecte les règles du Sudoku
    for ligne in grille:
        if len(set(ligne)) != 9:  # Vérifie l'unicité des chiffres dans une ligne
            return False
    for colonne in range(9):
        if len(set(grille[i][colonne] for i in range(9))) != 9:  # Vérifie l'unicité des chiffres dans une colonne
            return False
    for bloc_ligne in range(0, 9, 3):
        for bloc_colonne in range(0, 9, 3):
            bloc = [grille[i][j] for i in range(bloc_ligne, bloc_ligne + 3) for j in range(bloc_colonne, bloc_colonne + 3)]
            if len(set(bloc)) != 9:  # Vérifie l'unicité des chiffres dans un bloc 3x3
                return False
    return True

def force_brute_sudoku(grille_initiale):
    # Transforme les cases vides (0) en espaces pour exploration
    cases_vides = [(i, j) for i in range(9) for j in range(9) if grille_initiale[i][j] == 0]
    
    chiffres_possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    combinaisons = itertools.product(chiffres_possibles, repeat=len(cases_vides))
    
    for combinaison in combinaisons:
        grille = [ligne[:] for ligne in grille_initiale]
        for index, (i, j) in enumerate(cases_vides):
            grille[i][j] = combinaison[index]
        if verifier_solution(grille):
            return grille
    return None

# Exemple d'une grille simple avec des cases vides
grille = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Mesurer le temps d'exécution
debut = time.time()
solution = force_brute_sudoku(grille)
fin = time.time()

if solution:
    print("Solution trouvée :")
    for ligne in solution:
        print(ligne)
else:
    print("Aucune solution trouvée.")

print(f"Temps d'exécution : {fin - debut:.2f} secondes")