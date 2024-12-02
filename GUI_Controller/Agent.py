from GUI_Controller.Side import Side
from SolverFactory import SolverFactory

class Agent(Side):
    def __init__(self, color, sound, depth, solver, heuristic):
        super().__init__(color, sound)
        self.solver = SolverFactory(depth).create_solver(solver, heuristic)