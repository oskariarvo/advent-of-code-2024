from problem_solver import ProblemSolver

# Basic test cases
# Works
solver = ProblemSolver(0, 0, 9)
solver.instruction(2, 6, 0)
print("Register B:", solver.B)

#Works
solver = ProblemSolver(10, 0, 0)
solver.program([5, 0, 5, 1, 5, 4])

#Works
solver = ProblemSolver(2024, 0, 0)
solver.program([0, 1, 5, 4, 3, 0])
print("Register A:", solver.A)

#Works
solver = ProblemSolver(0, 29, 0)
solver.program([1, 7])
print("Register B:", solver.B)

#Works
solver = ProblemSolver(0, 2024, 43690)
solver.program([4, 0])
print("Register B:", solver.B)

print("\n")

# Bigger test cases
#Works
solver = ProblemSolver(729, 0, 0)
solver.program([0, 1, 5, 4, 3, 0])

#Works
solver = ProblemSolver(0, 0, 0)
solver.find_A([0,3,5,4,3,0])

print("\n")

# Reddit test cases
#Works
solver = ProblemSolver(0, 0, 0)
solver.find_A([2,4,1,0,7,5,1,5,0,3,4,5,5,5,3,0])

#Works
solver = ProblemSolver(202797954918051, 0, 0)
solver.program([2,4,1,0,7,5,1,5,0,3,4,5,5,5,3,0])

#Works
solver = ProblemSolver(0, 0, 0)
solver.find_A([2,4,1,3,7,5,0,3,1,4,4,4,5,5,3,0])

#Works
solver = ProblemSolver(266926175730705, 0, 0)
solver.program([2,4,1,3,7,5,0,3,1,4,4,4,5,5,3,0])