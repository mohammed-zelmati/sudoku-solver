import pygame
import random
import time  # Pour mesurer le temps
from typing import List, Optional, Tuple

class Sudoku:
    def __init__(self, screen: pygame.Surface, initial_grid: Optional[List[List[int]]] = None):
        self.original_grid = initial_grid or [[0]*9 for _ in range(9)]
        self.grid = [row.copy() for row in self.original_grid]
        self.screen = screen
        self.messages: List[str] = []
        self.selected_cell: Optional[Tuple[int, int]] = None

    def solve_backtracking(self, grid: List[List[int]], visualize: bool = False) -> bool:
        """
        Résout la grille de Sudoku par backtracking non optimisé
        Args:
            grid: Grille 9x9 à résoudre
            visualize: Si True, montre les étapes de résolution
        Returns:
            bool: True si une solution est trouvée, False sinon
        """
        # Trouver une case vide
        empty = self.find_empty(grid)
        if not empty:
            return True  # Plus de case vide = grille résolue
        
        row, col = empty
        
        # Essayer chaque nombre de 1 à 9
        for num in range(1, 10):
            # Vérifier si le nombre peut être placé
            if self.is_valid(grid, row, col, num):
                # Placer le nombre
                grid[row][col] = num
                
                # Visualisation optionnelle
                if visualize:
                    self.draw_grid()
                    pygame.display.flip()
                    pygame.time.wait(50)  # Pause pour voir l'évolution
                    
                # Continuer récursivement
                if self.solve_backtracking(grid, visualize):
                    return True
                    
                # Si échec, retirer le nombre (backtrack)
                grid[row][col] = 0
                
        return False  # Aucune solution trouvée

    def find_empty(self, grid: List[List[int]]) -> Optional[Tuple[int, int]]:
        """Trouve la première case vide dans la grille"""
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, grid: List[List[int]], row: int, col: int, num: int) -> bool:
        """Vérifie si placer 'num' à la position (row, col) est valide"""
        return (
            self.valid_row(grid, row, num) and
            self.valid_col(grid, col, num) and
            self.valid_square(grid, row - row % 3, col - col % 3, num)
        )

    def valid_row(self, grid: List[List[int]], row: int, num: int) -> bool:
        """Vérifie si 'num' n'est pas déjà dans la ligne"""
        return num not in grid[row]

    def valid_col(self, grid: List[List[int]], col: int, num: int) -> bool:
        """Vérifie si 'num' n'est pas déjà dans la colonne"""
        return all(row[col] != num for row in grid)

    def valid_square(self, grid: List[List[int]], start_row: int, start_col: int, num: int) -> bool:
        """Vérifie si 'num' n'est pas déjà dans le carré 3x3"""
        for i in range(3):
            for j in range(3):
                if grid[start_row + i][start_col + j] == num:
                    return False
        return True
    
    def show_message(self, message: str) -> None:
        self.messages.append(message)

    def draw_messages(self) -> None:
        font = pygame.font.SysFont("Arial", 20)
        y = 470
        for msg in self.messages[-5:]:
            text = font.render(msg, True, (255, 0, 0))
            self.screen.blit(text, (10, y))
            y += 25

    def reset_grid(self) -> None:
        self.grid = [[0] * 9 for _ in range(9)]
        self.messages = []

    def generate_grid(self, difficulty: str) -> None:
        self.original_grid = self.create_sudoku_grid()
        self.grid = [row.copy() for row in self.original_grid]
        difficulty_levels = {"facile": 40, "moyen": 50, "difficile": 60, "très_difficile": 70, "expert": 80}
        self.remove_numbers(difficulty_levels.get(difficulty, 40))

    def create_sudoku_grid(self) -> List[List[int]]:
        grid = [[0] * 9 for _ in range(9)]
        self.solve_backtracking(grid)
        return grid
    
    def remove_numbers(self, count: int) -> None:
        attempts = 0
        while attempts < count:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.grid[row][col] != 0:
                self.grid[row][col] = 0
                attempts += 1

    def handle_click(self, pos: Tuple[int, int]) -> None:
        x, y = pos
        if 0 <= x < 450 and 0 <= y < 450:
            self.selected_cell = (y // 50, x // 50)

    def handle_key(self, key: int) -> None:
        if not self.selected_cell:
            return
        row, col = self.selected_cell
        if self.original_grid[row][col] != 0:
            return
        if pygame.K_1 <= key <= pygame.K_9:
            num = key - pygame.K_0
            if self.is_valid(self.grid, row, col, num):
                self.grid[row][col] = num
            else:
                self.show_message("Mouvement invalide !")
        elif key in (pygame.K_DELETE, pygame.K_BACKSPACE):
            self.grid[row][col] = 0

    def draw_grid(self) -> None:
        self.screen.fill((255, 255, 255))
        for i in range(9):
            for j in range(9):
                rect = pygame.Rect(j*50, i*50, 50, 50)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
                if self.grid[i][j] != 0:
                    color = (0, 0, 255) if self.original_grid[i][j] == 0 else (0, 0, 0)
                    font = pygame.font.SysFont("Arial", 36)
                    text = font.render(str(self.grid[i][j]), True, color)
                    self.screen.blit(text, (j*50 + 15, i*50 + 5))

        for i in range(0, 10, 3):
            pygame.draw.line(self.screen, (0, 0, 0), (i*50, 0), (i*50, 450), 3)
            pygame.draw.line(self.screen, (0, 0, 0), (0, i*50), (450, i*50), 3)

        if self.selected_cell:
            row, col = self.selected_cell
            pygame.draw.rect(self.screen, (255, 100, 100), (col*50, row*50, 50, 50), 3)
