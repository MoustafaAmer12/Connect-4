from Agents.Heuristic import Heuristic

class Heuristic_Lec(Heuristic):
    def __init__(self):
        super().__init__()
        
    @staticmethod
    def string_index(index):
        return index//7,index% 7

    @staticmethod
    def grid_index(i,j):
        return i*7+j
    
    @staticmethod
    def valid(i,j):
        return not (i>5 or i<0 or j>6 or j<0)
    
    @staticmethod
    def shift_to_grid(shift):
        if(shift==1):
            return 0,1
        elif shift==7:
            return 1,0
        elif shift==8:
            return 1,1
        elif shift==6:
            return 1,-1
    

    def score(self, index, p, shift, player):
        g_index= self.string_index(index)
        shift_margin= self.shift_to_grid(shift)
        counter=0
        for i in range(4):
            new_index=[g_index[0]+shift_margin[0]*i,g_index[1]+shift_margin[1]*i]
            if(self.valid(new_index[0], new_index[1]) and self.state[self.grid_index(new_index[0], new_index[1])]==player):
                counter+=1
            else:
                break

        minus_shift=[g_index[0]-shift_margin[0],g_index[1]-shift_margin[1]]
        three_shift=[g_index[0] + 3 * shift_margin[0], g_index[1] + 3 * shift_margin[1]]
        two_shift=[g_index[0] + 2 * shift_margin[0], g_index[1] + 2 * shift_margin[1]]
        if(counter==4):
            p[0]+=1
        elif (counter == 3) and (((self.valid(minus_shift[0], minus_shift[1]))and self.state[self.grid_index(minus_shift[0], minus_shift[1])] == '0' and (not self.valid(minus_shift[0]+1,minus_shift[1]) or self.state[self.grid_index(minus_shift[0]+1,minus_shift[1])]!='0')) 
                                 or ((self.valid(three_shift[0], three_shift[1]) and self.state[self.grid_index(three_shift[0], three_shift[1])] == '0') and (not self.valid(three_shift[0] + 1, three_shift[1]) or self.state[self.grid_index(three_shift[0] + 1, three_shift[1])] != '0'))):
            p[1]+=1
        elif (counter == 2) and (((self.valid(minus_shift[0], minus_shift[1])) and self.state[self.grid_index(minus_shift[0], minus_shift[1])] == '0' and (not self.valid(minus_shift[0] + 1, minus_shift[1]) or self.state[self.grid_index(minus_shift[0] + 1, minus_shift[1])] != '0'))
          or ((self.valid(two_shift[0], two_shift[1]) and self.state[self.grid_index(two_shift[0], two_shift[1])] == '0') and (not self.valid(two_shift[0] + 1, two_shift[1]) or self.state[self.grid_index(two_shift[0] + 1, two_shift[1])] != '0'))):
            p[2]+=1

    def cell_score(self, i,p):
        self.score(i, p, 7,self.state[i])  #up
        self.score(i, p, 1,  self.state[i])  #left
        self.score(i, p, 8, self.state[i])  #diagonal_left
        self.score(i, p, 6,  self.state[i])  #diagonal_right


    def eval(self, state):
        self.state = state
        p1=[0,0,0]
        p2=[0,0,0]
        for i in range(42):
            if self.state[i]=='1':
                self.cell_score(i, p1)
            elif self.state[i]=='2':
                self.cell_score(i, p2)

        x=[10000,5000,1000]
        heuristic=0
        
        for i in range(3):
            heuristic += x[i]*(p1[i]-p2[i])

        return heuristic


if __name__ == '__main__':
    def MakeTest(grid):
        state = ""
        for i in range(6):
            for j in range(7):
                state += str(grid[i][j])
        return state

    connect4_board = [
        ['2', '1', '2', '2', '1', '2', '2'],
        ['2', '1', '2', '1', '1', '2', '2'],
        ['2', '2', '1', '1', '2', '1', '2'],
        ['2', '1', '2', '1', '1', '1', '2'],
        ['2', '1', '1', '1', '1', '1', '2'],
        ['1', '2', '1', '2', '1', '1', '2']
    ]

    heuristic = Heuristic_Lec()
    print(heuristic.eval(MakeTest(connect4_board)))