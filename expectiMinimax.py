import score

connect4_board = [
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0']
]

global_next_play=[5,5,5,5,5,5,5]
#grid='0'*42
#plyCounter=0
class expectiMinmax:

    def __init__(self,k):
        self.limit = k
        self.grid=""
        self.next_play=[]


    def make_state(self,grid,i,p):

        index=self.next_play[i]*7+i

        state=grid[:index]+p+grid[index+1:]
        return state

    def maximize(self,counter,state):     # computer


        if self.limit-counter==0:
            return None,score.get_score(state)


        max_column = -1
        for i in range(7):
            if self.next_play[i]!=-1:
                max_column=i
                break

        maxEvaluation = -1000000  # large negative
        fail_count=0
        for i in range(7):
           if self.next_play[i]!=-1:
                heuristic=self.chance(counter+1,state,i)

                if heuristic > maxEvaluation:
                    max_column=i
                    maxEvaluation=heuristic
           else:
               fail_count+=1
        if fail_count==7:
            return None,score.get_score(state)

        return max_column,maxEvaluation


    def minimize(self,counter,state):     # human

        if self.limit-counter==0 :
           return None,score.get_score(state)

        min_column = -1
        min_evaluation=1000000
        for i in range(7):           #set to first un inhabitant position
            if (self.next_play[i]!=-1):
                min_column = i
                break

        fail_count=0
        for i in range(7):

           if self.next_play[i]!=-1 :
                heuristic = self.chance(counter+1,state,i)
                if heuristic < min_evaluation:
                    min_column = i
                    min_evaluation = heuristic
           else:
               fail_count+=1

        if fail_count==7:
            return None,score.get_score(state)
        return min_column, min_evaluation


    def chance(self,counter, state, i):      #chance node

        if self.limit-counter==0 :
            return score.get_score(state)

        heuristic=0
        if (counter-1)%4==1:   #Maximizing
            if (self.next_play[i] != -1):
                x=self.make_state(state, i, '1')
                self.next_play[i] -= 1
                heuristic += 0.6 * self.minimize(counter+1, x)[1]
                self.next_play[i] += 1
            if (i - 1 >= 0 and self.next_play[i - 1] != -1):
                x=self.make_state(state, i - 1, '1')
                self.next_play[i-1] -= 1
                heuristic += 0.2 * self.minimize(counter+1,x)[1]
                self.next_play[i-1] += 1
            if (i + 1 <= 6 and self.next_play[i + 1] != -1):
                x=self.make_state(state, i + 1, '1')
                self.next_play[i+1] -= 1
                heuristic += 0.2 * self.minimize(counter+1,x)[1]
                self.next_play[i+1] += 1

            #print(heuristic)
            return heuristic

        elif (counter-1)%4==3:     # minimizing
            if (self.next_play[i] != -1):
                x=self.make_state(state, i, '2')
                self.next_play[i] -= 1
                heuristic += 0.6 * self.maximize(counter + 1, x)[1]
                self.next_play[i] += 1
            if (i - 1 >= 0 and self.next_play[i - 1] != -1):
                x=self.make_state(state, i - 1, '2')
                self.next_play[i-1] -= 1
                heuristic += 0.2 * self.maximize(counter + 1, x)[1]
                self.next_play[i-1] += 1
            if (i + 1 <= 6 and self.next_play[i + 1] != -1):
                x=self.make_state(state, i + 1, '2')
                self.next_play[i+1] -= 1
                heuristic += 0.2 * self.maximize(counter + 1, x)[1]
                self.next_play[i+1] += 1


            return heuristic

        return 0
    def solve(self,Grid):
        self.grid=""
        self.next_play=[-1,-1,-1,-1,-1,-1,-1]
        for i in range(6):
            for j in range(7):
                if(Grid[i][j]=='0'):
                    self.next_play[j]=max(self.next_play[j],i)
                self.grid+=Grid[i][j]
        print(self.grid)
        print(self.next_play)
        return self.maximize(1,self.grid)

expecti=expectiMinmax(8)
while sum(global_next_play)!=-7:
    print("computer turn:")
    mmm=expecti.solve(connect4_board)
    col=mmm[0]
    print("I  choose column : "+str(col))
    print("\n My heuristic is \n")
    print(mmm[1])
    connect4_board[global_next_play[col]][col]='1'
    index=global_next_play[col]*7+col
    #grid=grid[:index]+'1'+grid[index+1:]
    global_next_play[col]-=1

    for i in range(6):
        print(connect4_board[i])

    x=input("enter a column :")
    connect4_board[global_next_play[int(x)]][int(x)]='2'
    index = global_next_play[int(x)] * 7 + int(x)
    global_next_play[int(x)]-=1

    for i in range(6):
        print(connect4_board[i])

