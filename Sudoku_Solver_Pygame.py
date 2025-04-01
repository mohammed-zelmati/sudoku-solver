import pygame
import sys
import random
import time
from itertools import product
from enum import Enum, auto

# Initialize Pygame
pygame.init()

# --- Theme System ---
class Theme(Enum):
    """Theme options for the game"""
    LIGHT = auto()
    DARK = auto()
    BLUE = auto()

class ThemeManager:
    """Manages color themes for the game"""
    def __init__(self):
        self.themes = {
            Theme.LIGHT: {
                'background': (255, 255, 255),
                'grid_lines': (0, 0, 0),
                'grid_lines_minor': (200, 200, 200),
                'text': (0, 0, 0),
                'preset_text': (70, 70, 70),
                'user_text': (0, 128, 0),
                'selection': (0, 120, 215),
                'bubble_bg': (240, 240, 240),
                'bubble_border': (0, 0, 0),
                'button_bg': (230, 230, 230),
                'button_hover': (210, 210, 210),
                'button_text': (0, 0, 0),
                'timer_text': (70, 70, 70),
                'invalid': (255, 0, 0)
            },
            Theme.DARK: {
                'background': (30, 30, 30),
                'grid_lines': (200, 200, 200),
                'grid_lines_minor': (100, 100, 100),
                'text': (255, 255, 255),
                'preset_text': (200, 200, 200),
                'user_text': (100, 255, 100),
                'selection': (0, 160, 255),
                'bubble_bg': (50, 50, 50),
                'bubble_border': (200, 200, 200),
                'button_bg': (60, 60, 60),
                'button_hover': (80, 80, 80),
                'button_text': (255, 255, 255),
                'timer_text': (200, 200, 200),
                'invalid': (255, 80, 80)
            },
            Theme.BLUE: {
                'background': (225, 235, 255),
                'grid_lines': (30, 50, 100),
                'grid_lines_minor': (120, 140, 190),
                'text': (30, 50, 100),
                'preset_text': (50, 70, 120),
                'user_text': (0, 100, 200),
                'selection': (0, 160, 255),
                'bubble_bg': (210, 220, 240),
                'bubble_border': (30, 50, 100),
                'button_bg': (190, 210, 240),
                'button_hover': (170, 190, 220),
                'button_text': (30, 50, 100),
                'timer_text': (50, 70, 120),
                'invalid': (220, 60, 60)
            }
        }
        self.current_theme = Theme.LIGHT

    def switch_theme(self, theme):
        """Switch to a new theme"""
        self.current_theme = theme

    def get_color(self, color_name):
        """Retrieve a color from the current theme"""
        return self.themes[self.current_theme][color_name]

# --- Tutorial Bubble System ---
class BubbleManager:
    """Manages tutorial bubbles with a playful tone"""
    def __init__(self, theme_manager, screen_width, screen_height, ui_scale):
        self.theme_manager = theme_manager
        self.message = ""
        self.visible = True
        self.timer = 0
        self.auto_hide = True
        self.update_responsive_values(screen_width, screen_height, ui_scale)
        self.tutorial_messages = [
            "Hey there! Click a cell to pick it!",
            "Press 1-9 to pop a number in there!",
            "Hit 'B' to let backtracking solve it—magic!",
            "Tap 'C' for a brute force solve—raw power!",
            "Press 'T' to switch up the vibe with themes!",
            "Toggle me with 'H' if I’m chatty!",
            "ESC to bail, 'R' to reset—your call!"
        ]
        self.current_tutorial_index = 0

    def update_responsive_values(self, screen_width, screen_height, ui_scale):
        """Adjust bubble size and position responsively"""
        self.font_size = int(20 * ui_scale)
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.padding = int(15 * ui_scale)
        self.max_width = screen_width - 2 * self.padding
        self.x = self.padding
        self.y = screen_height - int(90 * ui_scale)

    def show(self, message, duration=4000):
        """Show a bubble with a message"""
        self.message = message
        self.visible = True
        if duration > 0:
            self.timer = pygame.time.get_ticks() + duration
            self.auto_hide = True
        else:
            self.auto_hide = False

    def update(self):
        """Hide bubble when timer expires"""
        if self.visible and self.auto_hide and pygame.time.get_ticks() > self.timer:
            self.visible = False

    def toggle_visibility(self):
        """Show or hide the bubble"""
        self.visible = not self.visible

    def next_tutorial(self):
        """Cycle to the next tutorial message"""
        self.current_tutorial_index = (self.current_tutorial_index + 1) % len(self.tutorial_messages)
        self.show(self.tutorial_messages[self.current_tutorial_index], 0)

    def draw(self, screen):
        """Render the bubble with a tail"""
        if not self.visible:
            return
        text = self.font.render(self.message, True, self.theme_manager.get_color('text'))
        width = min(text.get_width() + self.padding * 2, self.max_width)
        height = text.get_height() + self.padding * 2
        pygame.draw.rect(screen, self.theme_manager.get_color('bubble_bg'), 
                 (self.x, self.y, width, height), border_radius=10)
        pygame.draw.rect(screen, self.theme_manager.get_color('bubble_border'), 
                 (self.x, self.y, width, height), 2, border_radius=10)
        tail_size = int(8 * (height / 100))
        pygame.draw.polygon(screen, self.theme_manager.get_color('bubble_bg'), 
                    [(self.x + 30, self.y + height), 
                     (self.x + 30 + tail_size * 2, self.y + height), 
                     (self.x + 30 + tail_size, self.y + height + tail_size)])
        pygame.draw.polygon(screen, self.theme_manager.get_color('bubble_border'), 
                    [(self.x + 30, self.y + height), 
                     (self.x + 30 + tail_size * 2, self.y + height), 
                     (self.x + 30 + tail_size, self.y + height + tail_size)], 2)
        text_rect = text.get_rect(center=(self.x + width // 2, self.y + height // 2))
        screen.blit(text, text_rect)

# --- Button UI Elements ---
class Button:
    """Interactive buttons for the UI"""
    def __init__(self, theme_manager, x, y, width, height, text='', icon=None, callback=None):
        self.theme_manager = theme_manager
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.icon = icon
        self.callback = callback
        self.hovered = False

    def update_responsive_values(self, ui_scale):
        """Scale button properties"""
        self.font = pygame.font.SysFont("Arial", int(16 * ui_scale))
        self.border_radius = int(5 * ui_scale)

    def is_hovered(self, mouse_pos):
        """Check if mouse is over the button"""
        return (self.x <= mouse_pos[0] <= self.x + self.width and 
                self.y <= mouse_pos[1] <= self.y + self.height)

    def handle_event(self, event):
        """Process button events"""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.is_hovered(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and self.callback:
                self.callback()
                return True
        return False

    def draw(self, screen):
        """Render the button"""
        color = self.theme_manager.get_color('button_hover') if self.hovered else self.theme_manager.get_color('button_bg')
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=self.border_radius)
        pygame.draw.rect(screen, self.theme_manager.get_color('bubble_border'), 
                         (self.x, self.y, self.width, self.height), 1, border_radius=self.border_radius)
        if self.text:
            text_surf = self.font.render(self.text, True, self.theme_manager.get_color('button_text'))
            text_rect = text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(text_surf, text_rect)

# --- Sudoku Grid Logic and Display ---
class SudokuGrid:
    """Core Sudoku game logic and rendering"""
    def __init__(self, theme_manager):
        self.theme_manager = theme_manager
        self.grid = [[0] * 9 for _ in range(9)]
        self.original = [[0] * 9 for _ in range(9)]
        self.selected = None
        self.invalid_cells = set()
        self.generate_puzzle()
        self.solving_method = None
        self.solving_time = 0

    def update_responsive_values(self, cell_size, ui_scale):
        """Adjust grid visuals responsively"""
        self.cell_size = cell_size
        self.font_size = int(cell_size * 0.6)
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.selection_animation_max = int(6 * ui_scale)
        self.selection_animation = 0
        self.selection_growing = True

    def generate_puzzle(self):
        """Create a starting Sudoku puzzle"""
        preset = [
            [5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]
        ]
        self.grid = [row[:] for row in preset]
        self.original = [row[:] for row in preset]
        self.invalid_cells.clear()
        self.solving_method = None
        self.solving_time = 0

    def draw(self, screen, offset_x, offset_y):
        """Draw the 9x9 grid with smooth visuals"""
        grid_width = self.cell_size * 9
        pygame.draw.rect(screen, self.theme_manager.get_color('background'), 
                         (offset_x, offset_y, grid_width, grid_width))
        if self.selected:
            if self.selection_growing:
                self.selection_animation += 0.3
                if self.selection_animation >= self.selection_animation_max:
                    self.selection_growing = False
            else:
                self.selection_animation -= 0.3
                if self.selection_animation <= 0:
                    self.selection_growing = True
        for i in range(10):
            thickness = 3 if i % 3 == 0 else 1
            color = self.theme_manager.get_color('grid_lines') if i % 3 == 0 else self.theme_manager.get_color('grid_lines_minor')
            pygame.draw.line(screen, color, 
                             (offset_x + i * self.cell_size, offset_y), 
                             (offset_x + i * self.cell_size, offset_y + grid_width), thickness)
            pygame.draw.line(screen, color, 
                             (offset_x, offset_y + i * self.cell_size), 
                             (offset_x + grid_width, offset_y + i * self.cell_size), thickness)
        for i in range(9):
            for j in range(9):
                cell_x = offset_x + j * self.cell_size
                cell_y = offset_y + i * self.cell_size
                if self.selected == (i, j):
                    pygame.draw.rect(screen, self.theme_manager.get_color('selection'), 
                                     (cell_x + self.selection_animation, 
                                      cell_y + self.selection_animation, 
                                      self.cell_size - 2 * self.selection_animation, 
                                      self.cell_size - 2 * self.selection_animation), 2)
                if (i, j) in self.invalid_cells:
                    pygame.draw.rect(screen, self.theme_manager.get_color('invalid'), 
                                     (cell_x + 2, cell_y + 2, self.cell_size - 4, self.cell_size - 4), 1)
                if self.grid[i][j] != 0:
                    color = self.theme_manager.get_color('preset_text') if self.original[i][j] != 0 else self.theme_manager.get_color('user_text')
                    text = self.font.render(str(self.grid[i][j]), True, color)
                    text_rect = text.get_rect(center=(cell_x + self.cell_size // 2, cell_y + self.cell_size // 2))
                    screen.blit(text, text_rect)

    def select(self, row, col):
        """Select a grid cell"""
        if 0 <= row < 9 and 0 <= col < 9:
            self.selected = (row, col)
            return True
        return False

    def insert(self, num):
        """Insert a number into the selected cell"""
        if not self.selected:
            return False
        row, col = self.selected
        if self.original[row][col] == 0:
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                self.invalid_cells.discard((row, col))
                return True
            else:
                self.grid[row][col] = num
                self.invalid_cells.add((row, col))
                return False
        return False

    def clear_selected(self):
        """Clear the selected cell"""
        if self.selected:
            row, col = self.selected
            if self.original[row][col] == 0:
                self.grid[row][col] = 0
                self.invalid_cells.discard((row, col))
                return True
        return False

    def is_valid(self, row, col, num):
        """Validate a number placement using standard sudoku rules"""
        for i in range(9):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num:
                    return False
        return True

    def is_solution(self):
        """Check if the current grid is a complete and valid solution."""
        for i in range(9):
            if sorted(self.grid[i]) != list(range(1,10)):
                return False
        for j in range(9):
            col = [self.grid[i][j] for i in range(9)]
            if sorted(col) != list(range(1,10)):
                return False
        for block_i in range(3):
            for block_j in range(3):
                block = [self.grid[i][j] for i in range(block_i*3, block_i*3+3) 
                                      for j in range(block_j*3, block_j*3+3)]
                if sorted(block) != list(range(1,10)):
                    return False
        return True

    def solve_backtracking(self):
        """Solve using backtracking (optimized)"""
        self.grid = [row[:] for row in self.original]
        self.invalid_cells.clear()
        start = time.time()
        solved = self._solve_backtracking()
        end = time.time()
        if solved:
            self.solving_method = "backtracking"
            self.solving_time = end - start
        return solved

    def _solve_backtracking(self):
        """Recursive backtracking solver"""
        empty = next(((i, j) for i in range(9) for j in range(9) if self.grid[i][j] == 0), None)
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

    def solve_brute_force(self):
        """Attempt a real brute force solution (naively iterating over all possibilities)"""
        self.grid = [row[:] for row in self.original]
        self.invalid_cells.clear()
        start = time.time()
        solved = self._solve_brute_force()
        end = time.time()
        if solved:
            self.solving_method = "brute force"
            self.solving_time = end - start
        return solved

    def _solve_brute_force(self):
        """
        A naive brute force algorithm that does not use early constraint propagation.
        Note: The total number of possibilities is astronomical for a typical puzzle.
        To avoid freezing, we use an iteration limit.
        """
        empty_positions = [(i, j) for i in range(9) for j in range(9) if self.grid[i][j] == 0]
        iteration_limit = 10**6  # adjust as needed
        counter = [0]  # mutable counter

        def brute(index):
            if counter[0] > iteration_limit:
                return False
            if index == len(empty_positions):
                return self.is_solution()
            i, j = empty_positions[index]
            for num in range(1, 10):
                self.grid[i][j] = num
                counter[0] += 1
                if brute(index + 1):
                    return True
            self.grid[i][j] = 0
            return False

        return brute(0)

# --- Game Timer ---
class GameTimer:
    """Tracks and displays game time"""
    def __init__(self, theme_manager):
        self.theme_manager = theme_manager
        self.start_time = time.time()
        self.elapsed = 0
        self.running = True

    def update_responsive_values(self, ui_scale):
        """Scale timer font"""
        self.font = pygame.font.SysFont("Arial", int(20 * ui_scale))

    def update(self):
        """Update elapsed time"""
        if self.running:
            self.elapsed = time.time() - self.start_time

    def reset(self):
        """Reset the timer"""
        self.start_time = time.time()
        self.elapsed = 0
        self.running = True

    def format_time(self):
        """Format time as MM:SS"""
        minutes = int(self.elapsed) // 60
        seconds = int(self.elapsed) % 60
        return f"{minutes:02d}:{seconds:02d}"

    def draw(self, screen, x, y):
        """Render the timer"""
        time_text = self.font.render(f"Time: {self.format_time()}", True, 
                                    self.theme_manager.get_color('timer_text'))
        screen.blit(time_text, (x, y))

# --- Main Game Class ---
class SudokuGame:
    """Manages the entire Sudoku game"""
    def __init__(self):
        # Fixed resolution: 1280x720 (change to 1920x1080 for full HD if desired)
        self.width, self.height = 1280, 720
        self.ui_scale = self.width / 900  # base scale factor
        self.screen_width = self.width
        self.screen_height = self.height

        # Initialize theme and display settings
        self.theme_manager = ThemeManager()
        self.is_fullscreen = False
        # Set up the game components without overriding the fixed resolution
        self.initialize_game()
        self.resize_display()

    def initialize_game(self):
        """Set up game components"""
        self.calculate_responsive_dimensions()
        self.sudoku = SudokuGrid(self.theme_manager)
        self.sudoku.update_responsive_values(self.cell_size, self.ui_scale)
        self.bubble = BubbleManager(self.theme_manager, self.width, self.height, self.ui_scale)
        self.bubble.show("Hey there! Click a cell to kick things off!", 0)
        self.timer = GameTimer(self.theme_manager)
        self.timer.update_responsive_values(self.ui_scale)
        self.create_buttons()

    def calculate_responsive_dimensions(self):
        """
        Compute responsive sizes relative to the fixed window size.
        Instead of overriding the window resolution, we compute the grid size
        and its offsets so the grid is centered.
        """
        grid_size = min(self.width * 0.9, self.height * 0.85)
        self.cell_size = grid_size / 9
        self.grid_offset_x = (self.width - grid_size) // 2
        self.grid_offset_y = (self.height - grid_size) // 2

    def resize_display(self):
        """Set up the display window with the fixed resolution"""
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sudoku Deluxe")

    def create_buttons(self):
        """Initialize UI buttons"""
        button_size = int(30 * self.ui_scale)
        padding = int(10 * self.ui_scale)
        button_y = self.height - button_size - padding

        # Existing buttons: Help (?), Theme (T), Restart (R)
        self.help_button = Button(self.theme_manager, padding, button_y, button_size, button_size, "?", None, lambda: self.bubble.next_tutorial())
        self.help_button.update_responsive_values(self.ui_scale)
        self.theme_button = Button(self.theme_manager, padding * 2 + button_size, button_y, button_size, button_size, "T", None, self.cycle_theme)
        self.theme_button.update_responsive_values(self.ui_scale)
        self.restart_button = Button(self.theme_manager, padding * 3 + button_size * 2, button_y, button_size, button_size, "R", None, self.restart_game)
        self.restart_button.update_responsive_values(self.ui_scale)

        # Additional buttons: Backtracking (B) and Brute Force (C)
        self.backtracking_button = Button(self.theme_manager, padding * 4 + button_size * 3, button_y, button_size, button_size, "B", None, self.solve_with_backtracking)
        self.backtracking_button.update_responsive_values(self.ui_scale)
        self.bruteforce_button = Button(self.theme_manager, padding * 5 + button_size * 4, button_y, button_size, button_size, "C", None, self.solve_with_brute_force)
        self.bruteforce_button.update_responsive_values(self.ui_scale)

    def cycle_theme(self):
        """Switch to the next theme"""
        themes = list(Theme)
        current_index = themes.index(self.theme_manager.current_theme)
        next_index = (current_index + 1) % len(themes)
        self.theme_manager.switch_theme(themes[next_index])
        theme_names = {Theme.LIGHT: "Light", Theme.DARK: "Dark", Theme.BLUE: "Blue"}
        self.bubble.show(f"Switched to {theme_names[themes[next_index]]}—looking sharp!", 2000)

    def restart_game(self):
        """Reset the game"""
        self.sudoku.generate_puzzle()
        self.timer.reset()
        self.bubble.show("Fresh start—go get 'em!", 3000)

    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_event(event)
                # Process events for all buttons
                self.help_button.handle_event(event)
                self.theme_button.handle_event(event)
                self.restart_button.handle_event(event)
                self.backtracking_button.handle_event(event)
                self.bruteforce_button.handle_event(event)
            self.timer.update()
            self.bubble.update()
            self.render()
            clock.tick(60)
        pygame.quit()
        sys.exit()

    def handle_key_event(self, event):
        """Handle keyboard inputs"""
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_r:
            self.restart_game()
        elif event.key == pygame.K_h:
            self.bubble.toggle_visibility()
        elif event.key == pygame.K_t:
            self.cycle_theme()
        elif event.key == pygame.K_b:
            self.solve_with_backtracking()
        elif event.key == pygame.K_c:
            self.solve_with_brute_force()
        elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
            if self.sudoku.clear_selected():
                self.bubble.show("Poof! Cell’s empty now!", 2000)
        elif event.unicode.isdigit():
            num = int(event.unicode)
            if 1 <= num <= 9:
                if self.sudoku.insert(num):
                    self.bubble.show(f"Nice one! {num} fits like a glove!", 2000)
                else:
                    self.bubble.show(f"Oops! {num} doesn’t vibe there—try again!", 2000)

    def handle_mouse_event(self, event):
        """Handle mouse clicks"""
        x, y = event.pos
        row = int((y - self.grid_offset_y) // self.sudoku.cell_size)
        col = int((x - self.grid_offset_x) // self.sudoku.cell_size)
        if 0 <= row < 9 and 0 <= col < 9:
            if self.sudoku.select(row, col):
                cell_value = self.sudoku.grid[row][col]
                if cell_value == 0:
                    self.bubble.show("Blank slate! Drop a number with 1-9!", 3000)
                else:
                    status = "preset" if self.sudoku.original[row][col] != 0 else "your move"
                    self.bubble.show(f"Got {cell_value} ({status})—change it up!", 3000)

    def solve_with_backtracking(self):
        """Solve using backtracking and report"""
        self.bubble.show("Backtracking time—hold tight!", 1000)
        solved = self.sudoku.solve_backtracking()
        if solved:
            self.bubble.show(f"Backtracking nailed it in {self.sudoku.solving_time:.4f}s—boom!", 3000)
        else:
            self.bubble.show("Backtracking couldn’t crack it—yikes!", 3000)

    def solve_with_brute_force(self):
        """Solve using brute force and report"""
        self.bubble.show("Brute force incoming—raw power!", 1000)
        solved = self.sudoku.solve_brute_force()
        if solved:
            self.bubble.show(f"Brute force smashed it in {self.sudoku.solving_time:.4f}s—wow!", 3000)
        else:
            self.bubble.show("Brute force flopped—oh no!", 3000)

    def render(self):
        """Draw everything on screen"""
        self.screen.fill(self.theme_manager.get_color('background'))
        self.sudoku.draw(self.screen, self.grid_offset_x, self.grid_offset_y)
        timer_x = self.width - int(120 * self.ui_scale)
        timer_y = int(10 * self.ui_scale)
        self.timer.draw(self.screen, timer_x, timer_y)
        # Draw all buttons
        self.help_button.draw(self.screen)
        self.theme_button.draw(self.screen)
        self.restart_button.draw(self.screen)
        self.backtracking_button.draw(self.screen)
        self.bruteforce_button.draw(self.screen)
        self.bubble.draw(self.screen)
        pygame.display.flip()

# --- Start the Game ---
if __name__ == "__main__":
    game = SudokuGame()
    game.run()
