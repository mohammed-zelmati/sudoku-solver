import pygame
import mysql.connector
import time
import os
from typing import List, Optional, Tuple

class Sudoku:
    def __init__(self, screen: pygame.Surface, initial_grid: Optional[List[List[int]]] = None):
        self.original_grid = initial_grid or [[0]*9 for _ in range(9)]
        self.grid = [row.copy() for row in self.original_grid]
        self.screen = screen
        self.messages: List[str] = []
        self.selected_cell: Optional[Tuple[int, int]] = None
        self.db_connected = False

        try:
            self.db = mysql.connector.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "sudoku")
            )
            self.cursor = self.db.cursor()
            self.db_connected = True
        except mysql.connector.Error as err:
            self.show_error(f"Erreur de connexion à la base de données : {err}")

    def show_error(self, message: str) -> None:
        self.messages.append(f"ERREUR: {message}")

    def show_message(self, message: str) -> None:
        self.messages.append(message)

    def draw_messages(self) -> None:
        font = pygame.font.SysFont("Arial", 20)
        y = 500
        for msg in self.messages[-5:]:
            text = font.render(msg, True, (255, 0, 0))
            self.screen.blit(text, (10, y))
            y += 25

    def load_grid_from_db(self, grid_id: int) -> bool:
        if not self.db_connected:
            self.show_error("Pas de connexion à la base de données")
            return False

        try:
            self.cursor.execute("SELECT grid FROM grilles WHERE id = %s", (grid_id,))
            if result := self.cursor.fetchone():
                grid_data = result[0].split('\n')
                if len(grid_data) != 9 or any(len(row) != 9 for row in grid_data):
                    raise ValueError("Format de grille invalide")
                
                self.original_grid = [
                    [int(cell) if cell.isdigit() else 0 
                    for cell in row.strip()
                ] for row in grid_data]
                self.reset_grid()
                return True
            return False
        except Exception as e:
            self.show_error(str(e))
            return False

    def reset_grid(self) -> None:
        self.grid = [row.copy() for row in self.original_grid]

    def solve_backtracking(self) -> bool:
        start = time.time()
        solved = self._solve_backtracking()
        elapsed = time.time() - start
        self.show_message(f"Résolu en {elapsed:.4f}s par backtracking")
        return solved

    def _solve_backtracking(self) -> bool:
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if self._solve_backtracking():
                    return True
                self.grid[row][col] = 0
        return False

    def find_empty(self) -> Optional[Tuple[int, int]]:
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, row: int, col: int, num: int) -> bool:
        return (
            self.valid_row(row, num) and
            self.valid_col(col, num) and
            self.valid_square(row - row%3, col - col%3, num)
        )

    def valid_row(self, row: int, num: int) -> bool:
        return num not in self.grid[row]

    def valid_col(self, col: int, num: int) -> bool:
        return all(row[col] != num for row in self.grid)

    def valid_square(self, start_row: int, start_col: int, num: int) -> bool:
        for i in range(3):
            for j in range(3):
                if self.grid[start_row+i][start_col+j] == num:
                    return False
        return True

    def handle_click(self, pos: Tuple[int, int]) -> None:
        x, y = pos
        if x < 450 and y < 450:
            self.selected_cell = (y // 50, x // 50)

    def handle_key(self, key: int) -> None:
        if not self.selected_cell:
            return
        
        row, col = self.selected_cell
        if self.original_grid[row][col] != 0:
            return

        if pygame.K_1 <= key <= pygame.K_9:
            self.grid[row][col] = key - pygame.K_0
        elif key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
            self.grid[row][col] = 0

    def draw_grid(self) -> None:
        self.screen.fill((255, 255, 255))
        
        # Dessiner les cellules
        for i in range(9):
            for j in range(9):
                rect = pygame.Rect(j*50, i*50, 50, 50)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)
                
                if self.grid[i][j] != 0:
                    color = (0, 0, 255) if self.original_grid[i][j] == 0 else (0, 0, 0)
                    font = pygame.font.SysFont("Arial", 40)
                    text = font.render(str(self.grid[i][j]), True, color)
                    self.screen.blit(text, (j*50 + 15, i*50 + 5))

        # Dessiner les bordures épaisses
        for i in range(0, 10, 3):
            pygame.draw.line(self.screen, (0, 0, 0), (i*50, 0), (i*50, 450), 4)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i*50), (450, i*50), 4)

        # Dessiner la sélection
        if self.selected_cell:
            row, col = self.selected_cell
            pygame.draw.rect(self.screen, (255, 0, 0), (col*50, row*50, 50, 50), 3)

    def __del__(self):
        if self.db_connected:
            self.cursor.close()
            self.db.close()

class SudokuUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 650))
        pygame.display.set_caption("Sudoku Solver")
        self.clock = pygame.time.Clock()
        self.sudoku = Sudoku(self.screen)
        self.buttons = {
            "load": pygame.Rect(460, 20, 120, 40),
            "solve": pygame.Rect(460, 80, 120, 40),
            "reset": pygame.Rect(460, 140, 120, 40)
        }

    def draw_button(self, rect: pygame.Rect, text: str, color: Tuple[int, int, int]) -> None:
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(text, True, (0, 0, 0))
        self.screen.blit(text, (rect.x + 10, rect.y + 10))

    def run(self) -> None:
        running = True
        while running:
            self.clock.tick(30)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.sudoku.handle_key(event.key)

            self.screen.fill((255, 255, 255))
            self.sudoku.draw_grid()
            self.draw_interface()
            pygame.display.update()

    def handle_mouse(self, pos: Tuple[int, int]) -> None:
        # Gestion clic sur la grille
        if pos[0] < 450 and pos[1] < 450:
            self.sudoku.handle_click(pos)
            return

        # Gestion boutons
        if self.buttons["load"].collidepoint(pos):
            if self.sudoku.load_grid_from_db(1):
                self.sudoku.show_message("Grille chargée !")
        elif self.buttons["solve"].collidepoint(pos):
            if self.sudoku.solve_backtracking():
                self.sudoku.show_message("Solution trouvée !")
            else:
                self.sudoku.show_message("Aucune solution !")
        elif self.buttons["reset"].collidepoint(pos):
            self.sudoku.reset_grid()
            self.sudoku.show_message("Grille réinitialisée")

    def draw_interface(self) -> None:
        # Dessiner les boutons
        self.draw_button(self.buttons["load"], "Charger grille", (200, 200, 200))
        self.draw_button(self.buttons["solve"], "Résoudre", (200, 200, 200))
        self.draw_button(self.buttons["reset"], "Réinitialiser", (200, 200, 200))
        
        # Afficher les messages
        self.sudoku.draw_messages()

if __name__ == "__main__":
    ui = SudokuUI()
    ui.run()
    pygame.quit()