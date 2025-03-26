# Comparaison des algorithmes de résolution de Sudoku

## Observations
- La méthode de la force brute est très inefficace pour des grilles complexes.
- Le backtracking est plus performant car il suit une logique de réduction des possibilités.

## Conclusion
L'algorithme de backtracking est plus performant pour résoudre des grilles de Sudoku, particulièrement celles avec un niveau de difficulté élevé.

## Voici un tableau pour comparer les deux algorithmes :

| Algorithme  | Complexité temporelle   | Complexité spatiale | Observations              |
|-------------|-------------------------|---------------------|---------------------------|
| Force brute | O(9^81)                 | Faible              | Inefficace pour des       |
|             |                         |                     | grilles complexes         |
|-------------|-------------------------|---------------------|---------------------------|
| Backtracking| O(9^m), m < 81          | Faible              | Plus rapide et efficace   |

### Calcul du temps de méthode de la Force brute:

Nombre total de combinaisons : Une grille de Sudoku 9x9 possède 81 cases. Si toutes les cases sont vides, on a potentiellement (9^81) combinaisons possibles à explorer. Cela correspond à environ (1.96 * 10^77) combinaisons, cela donne :
### 1.96 * 10^77 = 19600000000000000000000000000000000000000000000000000000000000000000000000000000000
 Ce chiffre est très, très grand, illustrant à quel point l'approche par Force brute pour résoudre une grille de Sudoku devient impraticable à cause du nombre de combinaisons possibles. 

Supposons qu'un ordinateur peut tester 1 milliard (soit (10^9)) de combinaisons par seconde. C'est une hypothèse optimiste pour montrer l'ampleur du problème.
Sachant qu'une année contient (31,536,000) secondes, le temps maximum en années serait :  
#### Temps d'années = 1.96 * 10^68/(31,536,000 * 10^9) Ce qui donne environ (6.23 * 10^60) années.



       