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
        # self.grid = [row.copy() for row in self.original_grid]
        # Réinitialise toutes les cases de la grille à zéro (cases vides)
        self.grid = [[0] * 9 for _ in range(9)]
        self.messages = []  # Efface tous les messages

    def generate_grid(self, difficulty: str) -> None:
        self.original_grid = self.create_sudoku_grid()
        self.grid = [row.copy() for row in self.original_grid]
        difficulty_levels = {"facile": 40, "moyen": 50, "difficile": 60, "très_difficile": 70, "expert": 80}
        self.remove_numbers(difficulty_levels.get(difficulty, 40))

    def create_sudoku_grid(self) -> List[List[int]]:
        grid = [[0] * 9 for _ in range(9)]
        self.solve_backtracking(grid)
        return grid

    def solve_backtracking(self, grid: List[List[int]]) -> bool:
        empty = self.find_empty(grid)
        if not empty:
            return True
        row, col = empty
        for num in random.sample(range(1, 10), 9):  # Mélange pour plus de variété
            if self.is_valid(grid, row, col, num):
                grid[row][col] = num
                if self.solve_backtracking(grid):
                    return True
                grid[row][col] = 0
        return False

    def find_empty(self, grid: List[List[int]]) -> Optional[Tuple[int, int]]:
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, grid: List[List[int]], row: int, col: int, num: int) -> bool:
        return (
            self.valid_row(grid, row, num) and
            self.valid_col(grid, col, num) and
            self.valid_square(grid, row - row % 3, col - col % 3, num)
        )

    def valid_row(self, grid: List[List[int]], row: int, num: int) -> bool:
        return num not in grid[row]

    def valid_col(self, grid: List[List[int]], col: int, num: int) -> bool:
        return all(row[col] != num for row in grid)

    def valid_square(self, grid: List[List[int]], start_row: int, start_col: int, num: int) -> bool:
        for i in range(3):
            for j in range(3):
                if grid[start_row + i][start_col + j] == num:
                    return False
        return True

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
