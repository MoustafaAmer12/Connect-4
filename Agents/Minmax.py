from Agents.Solver import Solver
from Agents.Heuristic_Lec import Heuristic_Lec
import sys
from datetime import datetime

class Minmax(Solver):
    count = 1
    def __init__(self, max_depth, heuristic):
        super().__init__(max_depth, heuristic)

    def play(self, state):
        self.state = state

        for j in range(7):
            self.plays_av[j] = 0
            for i in range(6):
                if self.state[j + 7 * i] != '0':
                    break
                self.plays_av[j] += 1
        
        print(self.plays_av)
        current_state = str(self.state)
        av_moves = list(self.plays_av)
        return self.minmax(0, True, current_state, av_moves)

    def minmax(self, counter, maximizer, state, av_moves):
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
                _, score = self.minmax(counter + 1, False, new_state, av_moves)
                av_moves[i] += 1
                if score > max_score:
                    max_score = score
                    play_col = i
            # print("Score: ", max_score)
            # self.print_state(state)
            return play_col, max_score

        else:
            min_score = sys.maxsize
            for i in self.neighbours:
                if av_moves[i] == 0:
                    continue
                av_moves[i] -= 1
                new_state = state[:i + 7 * av_moves[i]] + player + state[i + 7 * av_moves[i] + 1:]
                _, score = self.minmax(counter + 1, True, new_state, av_moves)
                av_moves[i] += 1
                if score < min_score:
                    min_score = score
                    play_col = i
            # print("Score: ", min_score)
            # self.print_state(state)
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
    minmax = Minmax(8, heuristic=Heuristic_Lec())
    game = [['0','0','1','1','1','0','0'], ['0','0','2','2','2','0','0'], ['0','0','1','1','1','0','0'], ['0','0','2','2','2','0','0'], ['0','0','1','1','1','0','0'], ['0','1','2','2','2','0','2']]
    col, score = minmax.play("".join(str(game[i][j]) for i in range(len(game)) for j in range(len(game[0]))))
    print(col)
    print((datetime.now() - st_time).total_seconds())