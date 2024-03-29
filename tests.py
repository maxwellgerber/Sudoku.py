from sudoku import SudokuSolver
import unittest
from timeit import default_timer as timer

class TestIndexHelperMethods(unittest.TestCase):
  
  def test_to_square_identifier(self):
    solver = SudokuSolver()
    self.assertEqual(solver.to_square_identifier(0), 0)
    self.assertEqual(solver.to_square_identifier(4), 3)
    self.assertEqual(solver.to_square_identifier(8), 6)
    self.assertEqual(solver.to_square_identifier(37), 27)
    self.assertEqual(solver.to_square_identifier(40), 30)
    self.assertEqual(solver.to_square_identifier(44), 33)
    self.assertEqual(solver.to_square_identifier(72), 54)
    self.assertEqual(solver.to_square_identifier(76), 57)
    self.assertEqual(solver.to_square_identifier(80), 60)
    
  def test_get_square_indicies(self):
    solver = SudokuSolver()
    self.assertEqual(sorted(solver.get_square_indicies(0)), sorted((0, 1, 2, 9, 10, 11, 18, 19, 20,)))
    self.assertEqual(sorted(solver.get_square_indicies(30)), sorted((30, 31, 32, 39, 40, 41, 48, 49, 50,)))
    self.assertEqual(sorted(solver.get_square_indicies(48)), sorted((30, 31, 32, 39, 40, 41, 48, 49, 50,)))
    
  def test_get_row_indicies(self):
    solver = SudokuSolver()
    self.assertEqual(solver.get_row_indicies(43), (36, 37, 38, 39, 40, 41, 42, 43, 44))
    self.assertEqual(solver.get_row_indicies(2), (0, 1, 2, 3, 4, 5, 6, 7, 8))
    self.assertEqual(solver.get_row_indicies(80), (72, 73, 74, 75, 76, 77, 78, 79, 80))
    
  def test_get_col_indicies(self):
    solver = SudokuSolver()
    self.assertEqual(solver.get_col_indicies(0), (0, 9, 18, 27, 36, 45, 54, 63, 72))
    self.assertEqual(solver.get_col_indicies(45), (0, 9, 18, 27, 36, 45, 54, 63, 72))
    self.assertEqual(solver.get_col_indicies(33), (6, 15, 24, 33, 42, 51, 60, 69, 78))
  
  def test_to_square_identifier_5(self):
    solver = SudokuSolver(blocksize = 5)
    self.assertEqual(solver.to_square_identifier(76), 0)
    self.assertEqual(solver.to_square_identifier(359), 255)
    self.assertEqual(solver.to_square_identifier(620), 520)
    self.assertEqual(solver.to_square_identifier(146), 145)
    self.assertEqual(solver.to_square_identifier(125), 125)
    

class TestSudokuSolver(unittest.TestCase):
  
  def test_is_solved(self):
    solver = SudokuSolver()
    sol1 = [4, 8, 3, 9, 2, 1, 6, 5, 7, 9, 6, 7, 3, 4, 5, 8, 2, 1, 2, 5, 1, 8, 7, 6, 4, 9, 3, 5, 4, 8, 1, 3, 2, 9, 7, 6, 7, 2, 9, 5, 6, 4, 1, 3, 8, 1, 3, 6, 7, 9, 8, 2, 4, 5, 3, 7, 2, 6, 8, 9, 5, 1, 4, 8, 1, 4, 2, 5, 3, 7, 6, 9, 6, 9, 5, 4, 1, 7, 3, 8, 2]
    sol2 = [2, 4, 5, 9, 8, 1, 3, 7, 6, 1, 6, 9, 2, 7, 3, 5, 8, 4, 8, 3, 7, 5, 6, 4, 2, 1, 9, 9, 7, 6, 1, 2, 5, 4, 3, 8, 5, 1, 3, 4, 9, 8, 6, 2, 7, 4, 8, 2, 7, 3, 6, 9, 5, 1, 3, 9, 1, 6, 5, 7, 8, 4, 2, 7, 2, 8, 3, 4, 9, 1, 6, 5, 6, 5, 4, 8, 1, 2, 7, 9, 3]
    self.assertTrue(solver.is_solved(sol1))
    self.assertTrue(solver.is_solved(sol2))
    sol1[2] = 4
    self.assertFalse(solver.is_solved(sol1))
  
  def test_9x9(self):
    # Courtesy of Project Euler #96
    puzzle1 = [0, 0, 3, 0, 2, 0, 6, 0, 0, 9, 0, 0, 3, 0, 5, 0, 0, 1, 0, 0, 1, 8, 0, 6, 4, 0, 0, 0, 0, 8, 1, 0, 2, 9, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 6, 7, 0, 8, 2, 0, 0, 0, 0, 2, 6, 0, 9, 5, 0, 0, 8, 0, 0, 2, 0, 3, 0, 0, 9, 0, 0, 5, 0, 1, 0, 3, 0, 0]
    sol1 = [4, 8, 3, 9, 2, 1, 6, 5, 7, 9, 6, 7, 3, 4, 5, 8, 2, 1, 2, 5, 1, 8, 7, 6, 4, 9, 3, 5, 4, 8, 1, 3, 2, 9, 7, 6, 7, 2, 9, 5, 6, 4, 1, 3, 8, 1, 3, 6, 7, 9, 8, 2, 4, 5, 3, 7, 2, 6, 8, 9, 5, 1, 4, 8, 1, 4, 2, 5, 3, 7, 6, 9, 6, 9, 5, 4, 1, 7, 3, 8, 2]
    puzzle2 = [2, 0, 0, 0, 8, 0, 3, 0, 0, 0, 6, 0, 0, 7, 0, 0, 8, 4, 0, 3, 0, 5, 0, 0, 2, 0, 9, 0, 0, 0, 1, 0, 5, 4, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 2, 7, 0, 6, 0, 0, 0, 3, 0, 1, 0, 0, 7, 0, 4, 0, 7, 2, 0, 0, 4, 0, 0, 6, 0, 0, 0, 4, 0, 1, 0, 0, 0, 3]
    sol2 = [2, 4, 5, 9, 8, 1, 3, 7, 6, 1, 6, 9, 2, 7, 3, 5, 8, 4, 8, 3, 7, 5, 6, 4, 2, 1, 9, 9, 7, 6, 1, 2, 5, 4, 3, 8, 5, 1, 3, 4, 9, 8, 6, 2, 7, 4, 8, 2, 7, 3, 6, 9, 5, 1, 3, 9, 1, 6, 5, 7, 8, 4, 2, 7, 2, 8, 3, 4, 9, 1, 6, 5, 6, 5, 4, 8, 1, 2, 7, 9, 3]
    solver = SudokuSolver()
    self.assertEqual(solver(puzzle1), sol1)
    self.assertEqual(solver(puzzle2), sol2)
    
  def test_16x16(self):
    solver = SudokuSolver(blocksize = 4)
    puzzle1 = [0,15,0,1,0,2,10,14,12,0,0,0,0,0,0,0,0,6,3,16,12,0,8,4,14,15,1,0,2,0,0,0,14,0,9,7,11,3,15,0,0,0,0,0,0,0,0,0,4,13,2,12,0,0,0,0,6,0,0,0,0,15,0,0,0,0,0,0,14,1,11,7,3,5,10,0,0,8,0,12,3,16,0,0,2,4,0,0,0,14,7,13,0,0,5,15,11,0,5,0,0,0,0,0,0,9,4,0,0,6,0,0,0,0,0,0,13,0,16,5,15,0,0,12,0,0,0,0,0,0,0,0,9,0,1,12,0,8,3,10,11,0,15,0,2,12,0,11,0,0,14,3,5,4,0,0,0,0,9,0,6,3,0,4,0,0,13,0,0,11,9,1,0,12,16,2,0,0,10,9,0,0,0,0,0,0,12,0,8,0,6,7,12,8,0,0,16,0,0,10,0,13,0,0,0,5,0,0,5,0,0,0,3,0,4,6,0,1,15,0,0,0,0,0,0,9,1,6,0,14,0,11,0,0,2,0,0,0,10,8,0,14,0,0,0,13,9,0,4,12,11,8,0,0,2,0]
    solution1 = [8,15,11,1,6,2,10,14,12,7,13,3,16,9,4,5,10,6,3,16,12,5,8,4,14,15,1,9,2,11,7,13,14,5,9,7,11,3,15,13,8,2,16,4,12,10,1,6,4,13,2,12,1,9,7,16,6,10,5,11,3,15,8,14,9,2,6,15,14,1,11,7,3,5,10,16,4,8,13,12,3,16,12,8,2,4,6,9,11,14,7,13,10,1,5,15,11,10,5,13,8,12,3,15,1,9,4,2,7,6,14,16,1,4,7,14,13,10,16,5,15,6,8,12,9,2,3,11,13,7,16,5,9,6,1,12,2,8,3,10,11,14,15,4,2,12,8,11,7,16,14,3,5,4,6,15,1,13,9,10,6,3,14,4,10,15,13,8,7,11,9,1,5,12,16,2,15,1,10,9,4,11,5,2,13,16,12,14,8,3,6,7,12,8,4,3,16,7,2,10,9,13,14,6,15,5,11,1,5,11,13,2,3,8,4,6,10,1,15,7,14,16,12,9,7,9,1,6,15,14,12,11,16,3,2,5,13,4,10,8,16,14,15,10,5,13,9,1,4,12,11,8,6,7,2,3]
    self.assertEqual(solver(puzzle1), solution1)
    self.assertTrue(solver.is_solved(solution1))
    
  def test_25x25(self):
    solver = SudokuSolver(blocksize = 5)
    ## Takes forever to run
    puzzle = [0,0,12,6,0,0,7,0,18,0,5,24,0,10,1,0,0,4,0,0,0,0,0,0,0,2,0,19,0,13,0,0,0,10,0,0,0,0,0,0,0,0,18,5,0,0,0,0,0,1,0,0,0,0,0,0,0,22,0,0,0,0,3,0,2,0,0,14,12,0,16,8,25,0,0,0,16,0,0,0,2,23,0,0,13,12,22,0,0,0,21,15,19,3,0,0,0,0,14,0,23,0,24,0,0,0,0,0,25,8,4,0,16,19,21,0,0,7,0,0,0,3,12,0,9,0,4,0,2,0,0,0,0,0,0,0,10,0,24,12,17,16,0,0,0,5,0,0,0,0,0,0,9,0,0,6,25,0,0,0,8,0,5,3,0,0,0,0,0,0,20,0,0,18,19,15,0,10,11,0,0,0,18,12,19,0,0,0,0,0,0,0,23,0,0,7,0,0,4,0,0,0,0,0,0,0,0,14,0,22,0,0,18,16,20,0,6,11,13,0,0,0,0,0,0,0,22,0,25,0,0,1,17,5,4,7,0,0,14,0,8,3,21,0,0,11,0,0,0,6,0,20,13,15,0,0,0,0,0,0,9,0,0,2,0,25,0,1,8,0,0,5,0,21,0,0,1,0,0,0,0,16,10,0,7,0,0,4,20,0,0,9,0,0,14,0,24,0,17,0,25,2,5,0,0,0,0,0,13,0,0,0,0,0,22,0,0,0,0,0,19,1,8,0,0,0,0,7,21,0,0,12,0,2,17,0,0,0,18,6,16,0,0,15,0,0,13,0,10,0,8,10,18,12,16,9,0,0,0,5,0,0,0,0,19,0,0,17,0,21,0,15,0,0,22,0,8,0,0,15,0,3,0,6,0,21,0,0,7,0,18,14,5,0,1,0,0,0,0,0,0,0,0,19,0,1,0,16,11,0,0,0,10,22,25,15,0,0,0,0,0,0,21,0,0,0,3,1,0,21,0,0,4,0,0,0,0,2,0,13,0,24,25,0,0,14,0,0,6,0,0,0,0,0,0,0,0,15,0,12,14,0,6,17,24,0,0,0,0,0,0,0,13,0,0,0,5,23,16,4,0,13,24,7,2,0,9,0,0,15,3,0,22,0,0,0,0,0,0,8,0,0,25,20,2,0,19,0,0,0,0,1,0,0,0,0,21,3,0,0,12,0,0,0,0,16,12,0,5,0,11,21,0,23,0,0,15,0,0,0,0,19,9,0,0,0,0,0,25,10,0,0,0,0,9,20,22,7,4,0,3,0,14,25,18,0,11,0,0,0,0,0,1,0,15,24,0,6,0,22,8,0,25,14,0,10,11,0,9,0,20,1,16,0,7,0,23,0,0,13,14,13,21,1,0,0,5,0,0,0,6,0,22,0,23,10,0,0,0,2,0,0,18,7,11]
    # solution = solver(puzzle)
    # self.assertTrue(solver.is_solved(solution))
    
class test_HardProblems(unittest.TestCase):
	def test_brutal(self):
		## Swiped problem array from github.com/AChep
		problems = [
    # Copyright Arto Inkala
    # AI sudoku top 10 set 1

    # AI escargot
    """1 0 0 0 0 7 0 9 0
       0 3 0 0 2 0 0 0 8
       0 0 9 6 0 0 5 0 0
       0 0 5 3 0 0 9 0 0
       0 1 0 0 8 0 0 0 2
       6 0 0 0 0 4 0 0 0
       3 0 0 0 0 0 0 1 0
       0 4 0 0 0 0 0 0 7
       0 0 7 0 0 0 3 0 0""",
    # AI killer application
    """0 0 0 0 0 0 0 7 0
       0 6 0 0 1 0 0 0 4
       0 0 3 4 0 0 2 0 0
       8 0 0 0 0 3 0 5 0
       0 0 2 9 0 0 7 0 0
       0 4 0 0 8 0 0 0 9
       0 2 0 0 6 0 0 0 7
       0 0 0 1 0 0 9 0 0
       7 0 0 0 0 8 0 6 0""",
    # AI lucky diamond
    """1 0 0 5 0 0 4 0 0
       0 0 9 0 3 0 0 0 0
       0 7 0 0 0 8 0 0 5
       0 0 1 0 0 0 0 3 0
       8 0 0 6 0 0 5 0 0
       0 9 0 0 0 7 0 0 8
       0 0 4 0 2 0 0 1 0
       2 0 0 8 0 0 6 0 0
       0 0 0 0 0 1 0 0 2""",
    # AI worm hole
    """0 8 0 0 0 0 0 0 1
       0 0 7 0 0 4 0 2 0
       6 0 0 3 0 0 7 0 0
       0 0 2 0 0 9 0 0 0
       1 0 0 0 6 0 0 0 8
       0 3 0 4 0 0 0 0 0
       0 0 1 7 0 0 6 0 0
       0 9 0 0 0 8 0 0 5
       0 0 0 0 0 0 0 4 0""",
    # AI labyrinth
    """1 0 0 4 0 0 8 0 0
       0 4 0 0 3 0 0 0 9
       0 0 9 0 0 6 0 5 0
       0 5 0 3 0 0 0 0 0
       0 0 0 0 0 1 6 0 0
       0 0 0 0 7 0 0 0 2
       0 0 4 0 1 0 9 0 0
       7 0 0 8 0 0 0 0 4
       0 2 0 0 0 4 0 8 0""",
    # AI circles
    """0 0 5 0 0 9 7 0 0
       0 6 0 0 0 0 0 2 0
       1 0 0 8 0 0 0 0 6
       0 1 0 7 0 0 0 0 4
       0 0 7 0 6 0 0 3 0
       6 0 0 0 0 3 2 0 0
       0 0 0 0 0 6 0 4 0
       0 9 0 0 5 0 1 0 0
       8 0 0 1 0 0 0 0 2""",
    # AI squadron
    """6 0 0 0 0 0 2 0 0
       0 9 0 0 0 1 0 0 5
       0 0 8 0 3 0 0 4 0
       0 0 0 0 0 2 0 0 1
       5 0 0 6 0 0 9 0 0
       0 0 7 0 9 0 0 0 0
       0 7 0 0 0 3 0 0 2
       0 0 0 4 0 0 5 0 0
       0 0 6 0 7 0 0 8 0""",
    # AI honeypot
    """1 0 0 0 0 0 0 6 0
       0 0 0 1 0 0 0 0 3
       0 0 5 0 0 2 9 0 0
       0 0 9 0 0 1 0 0 0
       7 0 0 0 4 0 0 8 0
       0 3 0 5 0 0 0 0 2
       5 0 0 4 0 0 0 0 6
       0 0 8 0 6 0 0 7 0
       0 7 0 0 0 5 0 0 0""",
    # AI tweezers
    """0 0 0 0 1 0 0 0 4
       0 3 0 2 0 0 0 0 0
       6 0 0 0 0 8 0 9 0
       0 0 7 0 6 0 0 0 5
       9 0 0 0 0 5 0 8 0
       0 0 0 8 0 0 4 0 0
       0 4 0 9 0 0 1 0 0
       7 0 0 0 0 2 0 4 0
       0 0 5 0 3 0 0 0 7""",
    # AI broken brick
    """4 0 0 0 6 0 0 7 0
       0 0 0 0 0 0 6 0 0
       0 3 0 0 0 2 0 0 1
       7 0 0 0 0 8 5 0 0
       0 1 0 4 0 0 0 0 0
       0 2 0 9 5 0 0 0 0
       0 0 0 0 0 0 7 0 5
       0 0 9 1 0 0 0 3 0
       0 0 3 0 4 0 0 8 0"""]
       
		solver = SudokuSolver()
       
		for i, prob in enumerate(problems):
			prob = [int(i) for i in prob.split()]
			start = timer()
			solver(prob)
			end = timer()
			# print("Solved pr {} in {} seconds".format(i+1, end - start))
			self.assertTrue(end - start < 4)
			
if __name__ == "__main__":
  unittest.main()
  