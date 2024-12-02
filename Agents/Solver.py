class Solver:
    def __init__(self, max_depth, heuristic,alg_player):
        self.max_depth = max_depth
        self.eval_heuristic = heuristic.eval
        self.state = "0"*42
        self.plays_av = [6] * 7
        self.neighbours = [3, 2, 4, 1, 5, 0, 6]
        self.p1 = '1'
        self.p2 = '2'
        self.alg_player = alg_player
        
    # To Be Overriden
    def play(self):
        pass