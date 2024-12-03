from Agents.Heuristic_Lec import Heuristic_Lec
import sys
from datetime import datetime
from Agents.Solver import Solver

class AlphaBeta(Solver):
    count = 1
    def __init__(self, max_depth, heuristic, alg_player):
        super().__init__(max_depth, heuristic, alg_player)

    def play(self, state):
        self.grid = state
        self.state = "".join(self.grid[i][j] for i in range(len(self.grid)) for j in range(len(self.grid[0])))

        for j in range(7):
            self.plays_av[j] = 0
            for i in range(6):
                if self.grid[i][j] != '0':
                    break
                self.plays_av[j] += 1
        
        print(self.plays_av)
        current_state = str(self.state)
        av_moves = list(self.plays_av)
        maximizer = self.alg_player == '1'
        print(maximizer)
        return self.minmax(0, maximizer, current_state, av_moves)

    def minmax(self, counter, maximizer, state, av_moves, alpha = -sys.maxsize, beta=sys.maxsize):
        turn = sum(av_moves)
        if counter == self.max_depth or turn == 0:
            return None, self.eval_heuristic(state)
        if turn % 2 == 0:
            player = self.p1
        else:
            player = self.p2
        play_col = None
        if maximizer:
            max_score = -sys.maxsize - 1
            for i in self.neighbours:
                if av_moves[i] == 0:
                    continue
                av_moves[i] -= 1
                new_state = state[:i + 7 * av_moves[i]] + player + state[i + 7 * av_moves[i] + 1:]
                _, score = self.minmax(counter + 1, False, new_state, av_moves, alpha, beta)
                av_moves[i] += 1
                if score > max_score:
                    max_score = score
                    play_col = i
                alpha = max(alpha, score)
                if alpha <= beta:
                    break
            print("Score: ", max_score)
            self.print_state(state)
            return play_col, max_score

        else:
            min_score = sys.maxsize
            for i in self.neighbours:
                if av_moves[i] == 0:
                    continue
                av_moves[i] -= 1
                new_state = state[:i + 7 * av_moves[i]] + player + state[i + 7 * av_moves[i] + 1:]
                _, score = self.minmax(counter + 1, True, new_state, av_moves, alpha, beta)
                av_moves[i] += 1
                if score < min_score:
                    min_score = score
                    play_col = i
                beta = min(beta, score)
                if alpha <= beta:
                    break
            print("Score: ", min_score)
            self.print_state(state)
            return play_col, min_score

    def print_state(self, state):
        print(self.count)
        self.count += 1
        for i in range(6):
            for j in range(7):
                print(state[j + 7 * i],end=" ")
            print()
        print("_"*50)

if __name__ == "__main__":
    st_time = datetime.now()
    minmax = AlphaBeta(7, heuristic=Heuristic_Lec(), alg_player='1')
    game = [['0','0','0','0','0','0','0'], ['0','0','0','0','0','0','0'], ['0','0','0','0','0','0','0'], ['0','0','0','0','0','0','0'], ['0','0','0','0','0','0','0'], ['0','0','0','0','0','0','0']]
    col, score = minmax.play(game)
    print(col)
    print((datetime.now() - st_time).total_seconds())