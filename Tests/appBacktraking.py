import pygame
import mysql.connector
import time  # Importation du module time

class Sudoku:
    def __init__(self, screen, grid):
        self.grid = grid  # Grille du Sudoku sous forme de liste de listes
        self.size = 9  # Taille de la grille
        self.screen = screen  # Écran Pygame pour afficher les erreurs

        # Tentative de connexion à la base de données
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="357321zM@.",
                database="sudoku"
            )
            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            self.afficher_erreur(f"Connexion à la base de données échouée : {err}")
            pygame.quit()
            raise SystemExit

    def afficher_erreur(self, message):
        largeur, hauteur = 400, 200
        couleur_fond = (255, 200, 200)
        couleur_bordure = (150, 0, 0)
        couleur_texte = (0, 0, 0)
        police_taille = 24

        screen_rect = self.screen.get_rect()
        boite_rect = pygame.Rect(
            (screen_rect.centerx - largeur // 2, screen_rect.centery - hauteur // 2),
            (largeur, hauteur)
        )

        pygame.draw.rect(self.screen, couleur_bordure, boite_rect, 5)
        pygame.draw.rect(self.screen, couleur_fond, boite_rect)

        font = pygame.font.Font(None, police_taille)
        texte = font.render(message, True, couleur_texte)
        texte_rect = texte.get_rect(center=boite_rect.center)
        self.screen.blit(texte, texte_rect)

        pygame.display.flip()
        pygame.time.wait(3000)

    def load_grid_from_db(self, grid_id):
        try:
            query = "SELECT grid FROM grilles WHERE id = %s"
            self.cursor.execute(query, (grid_id,))
            result = self.cursor.fetchone()

            if result:
                self.grid = [
                    [int(cell) if cell.isdigit() else 0 for cell in row]
                    for row in result[0].split("\n")
                ]
            else:
                print(f"Aucune grille trouvée avec l'ID {grid_id}.")
                self.grid = None
        except mysql.connector.Error as err:
            self.afficher_erreur(f"Erreur lors du chargement de la grille : {err}")

    def solve_backtracking(self):
        # Mesurer le temps avant de commencer
        start_time = time.time()

        # Résolution avec l'algorithme de backtracking
        success = self._solve_backtracking()

        # Mesurer le temps après avoir terminé
        end_time = time.time()

        # Calculer le temps écoulé
        elapsed_time = end_time - start_time
        print(f"Temps nécessaire pour résoudre le Sudoku avec backtraking: {elapsed_time:.6f} secondes")

        return success

    def _solve_backtracking(self):
        # Recherche une case vide
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:  # Case vide
                    for num in range(1, self.size + 1):
                        if self.is_valid(row, col, num):
                            self.grid[row][col] = num
                            if self._solve_backtracking():
                                return True
                            self.grid[row][col] = 0  # Backtrack
                    return False  # Aucun nombre valide n'a pu être trouvé pour cette case
        return True  # Sudoku résolu

    def is_valid(self, row, col, num):
        # Vérifie si le nombre peut être placé dans la case (row, col)

        # Vérifie la ligne
        for i in range(self.size):
            if self.grid[row][i] == num:
                return False

        # Vérifie la colonne
        for i in range(self.size):
            if self.grid[i][col] == num:
                return False

        # Vérifie le sous-grille 3x3
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False

        return True

    def print_grid(self):
        for row in self.grid:
            print(" ".join(str(cell) if cell != 0 else '_' for cell in row))

    def to_pygame(self):
        self.screen.fill((255, 255, 255))  # Réinitialise l'écran
        font = pygame.font.SysFont("Arial", 40)
        black = (0, 0, 0)
        grey = (200, 200, 200)

        # Afficher la grille
        for row in range(self.size):
            for col in range(self.size):
                x = col * 50
                y = row * 50
                pygame.draw.rect(self.screen, black, (x, y, 50, 50), 2)
                if self.grid[row][col] != 0:
                    text = font.render(str(self.grid[row][col]), True, black)
                    self.screen.blit(text, (x + 15, y + 10))

        # Dessiner les lignes de la grille
        for i in range(1, self.size):
            if i % 3 == 0:
                pygame.draw.line(self.screen, black, (i * 50, 0), (i * 50, 450), 5)
                pygame.draw.line(self.screen, black, (0, i * 50), (450, i * 50), 5)
            else:
                pygame.draw.line(self.screen, grey, (i * 50, 0), (i * 50, 450), 1)
                pygame.draw.line(self.screen, grey, (0, i * 50), (450, i * 50), 1)

        pygame.display.update()  # Actualiser l'écran

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Sudoku Solver")

    grid = [[0 for _ in range(9)] for _ in range(9)]
    sudoku = Sudoku(screen, grid)

    grid_id = int(input("Entrez l'ID de la grille à charger : "))
    sudoku.load_grid_from_db(grid_id)

    if sudoku.grid is None:
        print("Impossible de charger la grille.")
        pygame.quit()
        return

    print("Grille chargée :")
    sudoku.print_grid()

    solve_choice = input("Voulez-vous résoudre la grille ? (O/N) : ").strip().lower()
    if solve_choice == 'o':
        sudoku.solve_backtracking()  # Résolution avec mesure du temps
        print("Grille résolue :")
        sudoku.print_grid()

    # Affichage avec Pygame après résolution
    sudoku.to_pygame()

    pygame.quit()

if __name__ == "__main__":
    main()
