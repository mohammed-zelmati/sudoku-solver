import pygame
import mysql.connector
import time

class Sudoku:
    def __init__(self, screen, grid):
        self.grid = grid
        self.size = 9
        self.screen = screen

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

    def to_pygame(self):
        self.screen.fill((255, 255, 255))
        font = pygame.font.SysFont("Arial", 40)
        black = (0, 0, 0)
        grey = (200, 200, 200)

        for row in range(self.size):
            for col in range(self.size):
                x = col * 50
                y = row * 50
                pygame.draw.rect(self.screen, black, (x, y, 50, 50), 2)
                if self.grid[row][col] != 0:
                    text = font.render(str(self.grid[row][col]), True, black)
                    self.screen.blit(text, (x + 15, y + 10))

        for i in range(1, self.size):
            if i % 3 == 0:
                pygame.draw.line(self.screen, black, (i * 50, 0), (i * 50, 450), 5)
                pygame.draw.line(self.screen, black, (0, i * 50), (450, i * 50), 5)
            else:
                pygame.draw.line(self.screen, grey, (i * 50, 0), (i * 50, 450), 1)
                pygame.draw.line(self.screen, grey, (0, i * 50), (450, i * 50), 1)

        pygame.display.update()

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

    def solve_brute_force(self):
        start_time = time.time()
        if self._solve_brute_force():
            print("Grille résolue avec succès par force brute !")
        else:
            print("Impossible de résoudre la grille par force brute.")
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Temps nécessaire (force brute) : {elapsed_time:.6f} secondes")
        return self.grid

    def _solve_brute_force(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    for num in range(1, self.size + 1):
                        if self.is_valid(row, col, num):
                            self.grid[row][col] = num
                            if self._solve_brute_force():
                                return True
                            self.grid[row][col] = 0
                    return False
        return True

    def solve_backtracking(self):
        start_time = time.time()
        success = self._solve_backtracking()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Temps nécessaire (backtracking) : {elapsed_time:.6f} secondes")
        return success

    def _solve_backtracking(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.grid[row][col] == 0:
                    for num in range(1, self.size + 1):
                        if self.is_valid(row, col, num):
                            self.grid[row][col] = num
                            if self._solve_backtracking():
                                return True
                            self.grid[row][col] = 0
                    return False
        return True

    def is_valid(self, row, col, num):
        for i in range(self.size):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False
        return True

    def print_grid(self):
        for row in self.grid:
            print(" ".join(str(cell) if cell != 0 else '_' for cell in row))
