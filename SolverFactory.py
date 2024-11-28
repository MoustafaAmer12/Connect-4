from Agents import Minmax, AlphaBeta, Expectiminmax

class SolverFactory:
    def __init__(self, max_depth: int, algorithm: str, heuristic:str):
        self.max_depth = max_depth
        self.heuristic = self.create_heuristic(heuristic)
        self.solver = self.create_solver(algorithm)
    
    def create_solver(self, algorithm: str):
        if algorithm == "Minmax":
            return Minmax(self.max_depth, self.heuristic)
        elif algorithm == "Alpha-beta Pruning":
            return AlphaBeta(self.max_depth, self.heuristic)
        elif algorithm == "Expectiminmax":
            return Expectiminmax(self.max_depth, self.heuristic)
        else:
            raise ValueError("Algorithm Should be one of 3 defined values")
        
    def create_heuristic(self, heuristic):
        pass