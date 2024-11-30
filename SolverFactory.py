from Agents import Minmax, AlphaBeta, Expectiminmax

class SolverFactory:
    def __init__(self, max_depth: int):
        self.max_depth = max_depth
    
    def create_solver(self, algorithm: str, heuristic: str):
        heuristic = self.create_heuristic(heuristic)
        if algorithm == "Minmax":
            return Minmax(self.max_depth, heuristic)
        elif algorithm == "Alpha-beta Pruning":
            return AlphaBeta(self.max_depth, heuristic)
        elif algorithm == "Expectiminmax":
            return Expectiminmax(self.max_depth, heuristic)
        else:
            raise ValueError("Algorithm Should be one of 3 defined values")
        
    def create_heuristic(self, heuristic):
        pass