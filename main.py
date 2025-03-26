import pygame
from sudoku import Sudoku


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Sudoku Solver")

    grid = [[0 for _ in range(9)] for _ in range(9)]
    sudoku = Sudoku(screen, grid)

    grid_id = int(input("Choisir la grille à résoudre entre 1 et 5 : "))
    sudoku.load_grid_from_db(grid_id)

    if sudoku.grid is None:
        print("Impossible de charger la grille.")
        pygame.quit()
        return

    print("Grille chargée :")
    sudoku.print_grid()

    solve_choice = input("Voulez-vous résoudre la grille ? (O/N) : ").strip().lower()
    if solve_choice == 'o':
        method = input("Choisissez la méthode (1: Force brute, 2: Backtracking) : ")
        
        if method == '1':
            if sudoku.solve_brute_force():
                print("Grille résolue :")
                sudoku.print_grid()
                sudoku.to_pygame()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
        elif method == '2':
            if sudoku.solve_backtracking():
                print("Grille résolue :")
                sudoku.print_grid()
                sudoku.to_pygame()
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
        else:
            print("Méthode invalide.")

    pygame.quit()

if __name__ == "__main__":
    main()