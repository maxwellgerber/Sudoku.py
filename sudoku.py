import math
import random

def print_blk(N):
  ## Prints properly formatted index grid for a puzzle with blocksize N
  for i in range(N):
    for j in range(N):
      for k in range(N):
        for l in range(N):
          print("{:>3} ".format(i*N**3 + j*N**2 + k*N + l), end="")
        print(" ", end="")
      print("\n", end="")
    print("\n", end="")

def memoize(f):
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)

class DeadEndException(Exception):
    ## Thrown when we need to backtrack
    pass

class SudokuSolver:
  def __init__(self, blocksize = 3):
    self.blk = blocksize
    self.inds = {}
    
  def to_square_identifier(self, n):
    ## Maps each index to the index in the top left corner of the corresponding region
    a = self.blk**3
    b = self.blk**2
    offset = n % a
    return n - (offset//b)*b - (offset%b) % self.blk
  
  def get_square_indicies(self, n):
    ## Gets indicies of all other numbers in n's square
    n = self.to_square_identifier(n)
    ans = []
    for i in range(self.blk):
      for j in range(self.blk):
        ans.append(n+i+j*self.blk**2)
    return tuple(ans)
  
  def get_row_indicies(self, n):
    ## Gets indicies of all other numbers in n's row
    n = n - n % self.blk**2
    return tuple(range(n, n+self.blk**2))
  
  def get_col_indicies(self, n):
    ## Gets indicies of all other numbers in n's col
    c = self.blk**2
    n = n - (n//c)*c
    return tuple(map(lambda x: x*c + n, range(c)))
  
  def indicies(self, n):
    ## Memoized helper function to get indicies of n's neighbors
    if n in self.inds:
      return self.inds[n]
    ans = self.inds[n] = set(self.get_row_indicies(n) + self.get_col_indicies(n) + self.get_square_indicies(n))
    ans.remove(n)
    return ans
  
  def get_untaken_numbers(self, puzzle, n):
    ## Gets all possible numbers for index n in puzzle
    untaken = set(range(1,self.blk**2+1)) # Set of all possible
    places = self.indicies(n)
    for i in places:
      if puzzle[i] != 0:
        if puzzle[i] in untaken:
          untaken.remove(puzzle[i])
    return untaken
  
  @staticmethod
  def is_complete(puzzle):
    return all(map(lambda x: x>0, puzzle))
  
  def is_solved(self, puzzle):
    for i in range(len(puzzle)):
      curr = puzzle[i]
      for position in self.indicies(i):
        if puzzle[position] == curr:
          return False
    return True
    
  def __call__(self, puzzle, verbose = False):
    return self.solve_puzzle_constrained(puzzle, verbose=verbose)
  
  def solve_puzzle_constrained(self, puzzle, verbose = False):
    # Deterministic until it can't anymore
    unfilled = set([i for i, val in enumerate(puzzle) if val == 0])
    done = False
    while not done:
      done = True
      for spot in unfilled.copy():
        possible = self.get_untaken_numbers(puzzle, spot)
        if len(possible) == 1:
          puzzle[spot] = possible.pop()
          unfilled.remove(spot)
          done = False
    return self.solve_puzzle_recursive(puzzle)
    
  def solve_puzzle_recursive(self, puzzle):
    # Seach method w/backtracing
    unfilled = [i for i, val in enumerate(puzzle) if val == 0]
    if not unfilled: # Complete- no more spots to fill
      return puzzle
      
    spot = unfilled.pop()
    possible = self.get_untaken_numbers(puzzle, spot)
    if not possible: # Square is empty but cannot put anything in it- must be in error
      raise DeadEndException
      
    for num in possible:
      puzzle[spot] = num
      try:
        return self.solve_puzzle_constrained(puzzle)
      except DeadEndException:
        for i in unfilled:
          puzzle[i] = 0
    raise DeadEndException # All other possibilites failed- must be in error
