# Sudoku Deluxe

## 🧩 Project Overview

**Sudoku Deluxe** is an interactive, fully responsive, and stylish Sudoku game built with **Python and Pygame**. This project goes beyond classic solvers by adding:

- 🎨 **Dynamic Themes** (Light, Dark, Blue)
- 💬 **Tutorial Bubbles** to guide the player
- 🧠 **Manual Entry Mode** with real-time feedback
- 🧪 **Cheating Options** using both **Backtracking** and simulated **Brute Force** solving methods
- ⏱️ **In-game Timer**, helpful icons, and responsive scaling for different screen sizes

It’s designed as an educational and visually engaging Sudoku experience.

---

## 🧠 Algorithms Used

### 1. **Backtracking Solver**
- Efficient recursive method
- Fills empty cells one-by-one and backtracks if a constraint is violated
- Real-world practical solver

### 2. **Simulated Brute Force Solver**
- Placeholder: currently mirrors backtracking for demo purposes
- Meant to simulate exhaustive solving logic for comparison

> Future versions could implement real brute force using `itertools.product` for full contrast

---

## 💻 Technologies

- **Python 3.12+**
- **Pygame** for all rendering and input
- **OOP Architecture** for readability and scalability
- **Time module** for tracking solving performance

---

## 🚀 Features

| Feature                | Description                                                  |
|------------------------|--------------------------------------------------------------|
| 🧩 Responsive UI       | Auto-resizes grid and font for any screen size              |
| 🌈 Themes              | Toggle between Light, Dark, and Blue                        |
| 💬 Tutorial Bubbles    | Dynamic hints to guide the player                           |
| ⌨️ Manual Play         | Select cells, enter 1–9, and get feedback                   |
| 🔍 Solver Shortcuts    | Press `B` for backtracking, `C` for brute force             |
| ❓ Help & Reset        | Buttons for help cycling, theme toggling, and restarting    |
| ⏱ Timer               | Tracks total game time                                       |

---

## 🎮 Controls

| Key / Action         | Effect                          |
|----------------------|----------------------------------|
| `1–9`                | Enter number in selected cell   |
| `B`                  | Solve with backtracking         |
| `C`                  | Solve with brute force          |
| `T`                  | Switch theme                    |
| `R`                  | Restart the game                |
| `H`                  | Toggle tutorial bubbles         |
| `ESC`                | Quit                            |
| Mouse Click          | Select cell                     |

---

## 📂 File Structure

```
├── sudoku_game.py         # Main game script
├── assets/                # Optional: Add icons, sound files
└── README.md              # This file
```

---

## 🧪 Sample Performance Output

| Method        | Time (Example Puzzle) |
|---------------|------------------------|
| Backtracking  | 0.0134s                |
| Brute Force   | 0.0141s (simulated)    |

> These values vary by puzzle difficulty.

---

## 🔧 How to Run

1. Install dependencies:
```bash
pip install pygame
```
2. Run the game:
```bash
python sudoku_game.py
```
3. Enjoy the most deluxe Sudoku experience in Python!

---

## 🙌 Credits & Inspiration

Inspired by classic Sudoku solvers, this project adds a modern twist with UX-first design. Tutorial bubbles, themes, and humor are designed to make the experience more fun, especially in coding bootcamps or student showcases.

---

Have fun solving Sudoku — manually, intelligently, or by cheating 😎
