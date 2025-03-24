# Comparaison des algorithmes de résolution de Sudoku

## Observations
- La méthode de la force brute est très inefficace pour des grilles complexes.
- Le backtracking est plus performant car il suit une logique de réduction des possibilités.

## Conclusion
L'algorithme de backtracking est plus performant pour résoudre des grilles de Sudoku, particulièrement celles avec un niveau de difficulté élevé.

## Voici un tableau pour comparer les deux algorithmes :
### |------------|----------------------|---------------------|---------------|
### |algorithme  | Complexité toporelle | Complexité spaciale | Observations  |
### |------------|----------------------|---------------------|---------------|
### |Force brute | $$O(9^{81})$$        | Faible              |Inefficace pour|
### |            |                      |                     |des grilles    |
### |            |                      |                     |complexes      |
### |------------|----------------------|---------------------|---------------|
### |Backtracking| $$O(9^m)$$, m < 81   | Faible              |Plus rapide et |
### |            |                      |                     | efficace      |
### |------------|----------------------|---------------------|---------------|


       