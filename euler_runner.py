import fileinput
from sudoku import SudokuSolver

solver = SudokuSolver(blocksize = 3)

def puzzle_from_str(string):
  puzzle = []
  for char in string:
    puzzle.append(int(char))
  return puzzle

def compute(total, puzzle):
  if puzzle: # Darn first case
    print(puzzle)
    ans = solver(puzzle)
    num = ans[0]*100 + ans[1]*10 + ans[2]
    total += num
  return total

if __name__ == "__main__":
  string = ""
  total = 0
  for i, line in enumerate(fileinput.input()):
    if i % 10 == 0:
      puzzle = puzzle_from_str(string)
      total = compute(total, puzzle)
      string = ""
    else:
      string += "".join(line.split())
  puzzle = puzzle_from_str(string)
  total = compute(total, puzzle)
  print("The answer is {}".format(total))
  