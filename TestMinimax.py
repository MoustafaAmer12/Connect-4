import score

connect4_board = [
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0']
]

#game_counter=0
grid='0'*42
limit=8
next_play=[5,5,5,5,5,5,5]
column_score=[1,2,3,4,3,2,1]
def make_state(grid,i,p):

    index=next_play[i]*7+i

    state=grid[:index]+p+grid[index+1:]
    #print(state)
    return state

def maximize(counter,state):     # computer


    if limit-counter==0:
        return None,score.get_score(state)


    max_column = -1
    max_column_score=0
    for i in range(7):
        if(next_play[i]!=-1 and column_score[i]>max_column_score):
            max_column_score=column_score[i]
            max_column=i

    maxEvaluation = -1000000  # large negative

    for i in range(7):
       if next_play[i]!=-1:
            x=make_state(state,i,'1')
            next_play[i]-=1
            heuristic=minimize(counter+1,x)
            next_play[i]+=1
            if heuristic[1] > maxEvaluation:
                max_column=i
                maxEvaluation=heuristic[1]
    return max_column,maxEvaluation


def minimize(counter,state):     # human

    if limit-counter==0:
       return None,score.get_score(state)

    min_column = -1
    col_score=0
    min_evaluation=1000000
    for i in range(7):           #set to first un inhabitant position
        if (state[next_play[i]*7+i]=='0' and col_score<column_score[i]):
            col_score=column_score[i]
            min_column = i

    for i in range(7):
       if next_play[i]!=-1 :
            x=make_state(state,i,'2')
            next_play[i]-=1
            heuristic = maximize(counter+1,x)
            next_play[i]+=1
            if heuristic[1] < min_evaluation:
                min_column = i
                min_evaluation = heuristic[1]

    return min_column, min_evaluation




while sum(next_play)!=-7:
    print("computer turn:")
    mmm = maximize(1, grid)
    col = mmm[0]
    print("I  choose column : " + str(col))
    print("\n My heuristic is \n")
    print(mmm[1])
    connect4_board[next_play[col]][col] = '1'
    index = next_play[col] * 7 + col
    grid = grid[:index] + '1' + grid[index + 1:]
    next_play[col] -= 1

    for i in range(6):
        print(connect4_board[i])

    x = input("enter a column :")
    connect4_board[next_play[int(x)]][int(x)] = '2'
    index = next_play[int(x)] * 7 + int(x)
    grid = grid[:index] + '2' + grid[index + 1:]
    next_play[int(x)] -= 1

    for i in range(6):
        print(connect4_board[i])

