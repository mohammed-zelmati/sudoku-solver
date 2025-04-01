import time
import copy
from itertools import product

class SudokuGrid:
    def __init__(self, grid):
        self.grid = grid

    def print_grid(self):
        for row in self.grid:
            print(" ".join(str(cell) for cell in row))

    def is_valid_grid(self):
        """Validate entire grid (for brute force check)."""
        for i in range(9):
            row = [num for num in self.grid[i] if num != 0]
            col = [self.grid[j][i] for j in range(9) if self.grid[j][i] != 0]
            if len(set(row)) != len(row) or len(set(col)) != len(col):
                return False

        for box_row in range(3):
            for box_col in range(3):
                block = []
                for i in range(3):
                    for j in range(3):
                        num = self.grid[box_row * 3 + i][box_col * 3 + j]
                        if num != 0:
                            block.append(num)
                if len(set(block)) != len(block):
                    return False
        return True

    def is_valid(self, row, col, num):
        if num in self.grid[row]:
            return False
        if num in [self.grid[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == num:
                    return False
        return True

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def solve_backtracking(self):
        empty = self.find_empty()
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if self.solve_backtracking():
                    return True
                self.grid[row][col] = 0
        return False

    def find_empty_cells(self):
        return [(i, j) for i in range(9) for j in range(9) if self.grid[i][j] == 0]

    def solve_true_brute_force(self):
        """True brute force: generate every possible combo."""
        empty_cells = self.find_empty_cells()
        total_empty = len(empty_cells)
        possibilities = product(range(1, 10), repeat=total_empty)
        checked = 0
        for combo in possibilities:
            temp_grid = copy.deepcopy(self.grid)
            for idx, (i, j) in enumerate(empty_cells):
                temp_grid[i][j] = combo[idx]
            checked += 1
            if SudokuGrid(temp_grid).is_valid_grid():
                print(f"\n✅ Valid Solution Found after checking {checked} combinations.")
                self.grid = temp_grid
                return True
            if checked % 100000 == 0:
                print(f"Checked {checked} combinations... still searching...")

        print(f"\n❌ No valid solution found after checking {checked} combinations.")
        return False

def import_grid(filename):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if ' ' in line:
                row = [int(num) if num != '_' else 0 for num in line.split()]
            else:
                row = [int(char) if char != '_' else 0 for char in line]
            if len(row) != 9:
                raise ValueError(f"Each row must have 9 numbers. Found {len(row)}: {row}")
            grid.append(row)
    if len(grid) != 9:
        raise ValueError(f"Grid must have 9 rows. Found {len(grid)} rows.")
    return grid

def print_solution(original, solved):
    for i in range(9):
        for j in range(9):
            if original[i][j] == 0:
                print(f"\033[92m{solved[i][j]}\033[0m", end=" ")
            else:
                print(solved[i][j], end=" ")
        print()

if __name__ == "__main__":
    # ⚠ Replace this with your test file path if needed
    filename = "exemple1.txt"
    try:
        original_grid = import_grid(filename)
    except ValueError as ve:
        print("Error loading grid:", ve)
        exit(1)

    print("\nOriginal Grid:")
    SudokuGrid(original_grid).print_grid()

    # ✅ Backtracking Solver (optimized)
    sudoku_back = SudokuGrid([row[:] for row in original_grid])
    start_bt = time.time()
    back_success = sudoku_back.solve_backtracking()
    end_bt = time.time()

    if back_success:
        print("\n✅ Solution with Backtracking (Optimized):")
        print_solution(original_grid, sudoku_back.grid)
        print(f"⏱ Backtracking Execution Time: {end_bt - start_bt:.4f} seconds")
    else:
        print("\n❌ Backtracking Solver Failed to find a solution.")

    # ✅ True Brute Force Solver (dumb full combinations)
    sudoku_brute = SudokuGrid([row[:] for row in original_grid])
    start_bf = time.time()
    brute_success = sudoku_brute.solve_true_brute_force()
    end_bf = time.time()

    if brute_success:
        print("\n✅ Solution with True Brute Force (Full Search):")
        print_solution(original_grid, sudoku_brute.grid)
        print(f"⏱ True Brute Force Execution Time: {end_bf - start_bf:.4f} seconds")
    else:
        print("\n❌ True Brute Force Solver Failed to find a solution.")
