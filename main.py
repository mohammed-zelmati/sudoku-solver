import pygame
import time  # Pour mesurer le temps
from typing import Tuple
from sudoku import Sudoku

class SudokuUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 550))
        pygame.display.set_caption("Sudoku")
        self.clock = pygame.time.Clock()
        self.sudoku = Sudoku(self.screen)
        self.buttons = {
            "menu": pygame.Rect(470, 20, 120, 40),
            "solve": pygame.Rect(470, 70, 120, 40),
            "reset": pygame.Rect(470, 120, 120, 40)
        }
        self.menu_buttons = {
            "facile": pygame.Rect(470, 70, 120, 40),
            "moyen": pygame.Rect(470, 120, 120, 40),
            "difficile": pygame.Rect(470, 170, 120, 40),
            "très_difficile": pygame.Rect(470, 220, 120, 40),
            "expert": pygame.Rect(470, 270, 120, 40)
        }
        self.show_menu = False

    def draw_button(self, rect: pygame.Rect, text: str, color: Tuple[int, int, int], hover: bool = False) -> None:
        pygame.draw.rect(self.screen, (255, 200, 200) if hover else color, rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
        font = pygame.font.SysFont("Arial", 20)
        text_surface = font.render(text, True, (0, 0, 0))
        self.screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2, 
                                       rect.y + (rect.height - text_surface.get_height()) // 2))

    def run(self) -> None:
        running = True
        while running:
            self.clock.tick(30)
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.sudoku.handle_key(event.key)

            self.sudoku.draw_grid()
            self.draw_interface(mouse_pos)
            pygame.display.flip()

    def handle_mouse(self, pos: Tuple[int, int]) -> None:
        if pos[0] < 450 and pos[1] < 450:
            self.sudoku.handle_click(pos)
            self.show_menu = False
            return
        if self.buttons["menu"].collidepoint(pos):
            self.show_menu = not self.show_menu
        elif self.buttons["solve"].collidepoint(pos) and not self.show_menu:
            start_time = time.time()  # Début de la mesure du temps
            if self.sudoku.solve_backtracking(self.sudoku.grid):
                end_time = time.time()  # Fin de la mesure du temps
                elapsed_time = end_time - start_time
                self.sudoku.show_message(f"Solution trouvée en {elapsed_time:.3f} secondes")
            else:
                self.sudoku.show_message("Aucune solution !")
        elif self.buttons["reset"].collidepoint(pos) and not self.show_menu:
            self.sudoku.reset_grid()
            self.sudoku.show_message("Grille réinitialisée")

        if self.show_menu:
            for level, rect in self.menu_buttons.items():
                if rect.collidepoint(pos):
                    self.sudoku.generate_grid(level)
                    self.sudoku.show_message(f"Grille {level} générée!")
                    self.show_menu = False
                    break

    def draw_interface(self, mouse_pos: Tuple[int, int]) -> None:
        for key, rect in self.buttons.items():
            hover = rect.collidepoint(mouse_pos) and (key != "menu" or not self.show_menu)
            self.draw_button(rect, key.capitalize(), (200, 200, 200), hover)
        
        if self.show_menu:
            for key, rect in self.menu_buttons.items():
                hover = rect.collidepoint(mouse_pos)
                self.draw_button(rect, key.capitalize(), (200, 200, 200), hover)
        
        self.sudoku.draw_messages()

if __name__ == "__main__":
    ui = SudokuUI()
    ui.run()
    pygame.quit()