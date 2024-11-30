import score

connect4_board = [
    ['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0'] ,
['0', '0', '0', '0', '0', '0', '0']
]

grid='0'*42
limit=10
next_play=[5,5,5,5,5,5,5]

def make_state(grid,i,p):

    index=next_play[i]*7+i

    state=grid[:index]+p+grid[index+1:]
    # print(state)
    return state

def maximize(counter,state):     # computer


    if limit-counter==0:
        # print("\n state at getting heuristic \n")
        # print(state)
        # print("\n")
        return None,score.get_score(state)


    max_column = -1
    for i in range(7):
        if(state[next_play[i]*7+i]=='0'):
            max_column=i
            break
    #print(max_column)
    maxEvaluation = -1000000  # large negative

    for i in range(7):
       if next_play[i]!=-1:
            heuristic=chance(counter+1,state,i)

            if heuristic > maxEvaluation:
                max_column=i
                maxEvaluation=heuristic

    return max_column,maxEvaluation


def minimize(counter,state):     # human

    if limit-counter==0:
       # print("\n state at getting heuristic \n")
       # print(state)
       # print("\n")
       return None,score.get_score(state)

    min_column = -1
    min_evaluation=1000000
    for i in range(7):           #set to first un inhabitant position
        if (state[next_play[i]*7+i]=='0'):
            min_column = i
            break
    #print(min_column)
    for i in range(7):

       if next_play[i]!=-1 :
            heuristic = chance(counter+1,state,i)
            if heuristic < min_evaluation:
                min_column = i
                min_evaluation = heuristic

    return min_column, min_evaluation


def chance(counter,state,i):      #chance node

    if limit-counter==0:
        # print("\n state at getting heuristic \n")
        # print(state)
        # print("\n")
        return score.get_score(state)

    if (counter-1)%4==1:   #Maximizing
        heuristic=0
        if (next_play[i] != -1):
            next_play[i] -= 1
            heuristic += 0.6 * minimize(counter+1, make_state(state, i, '2'))[1]
            next_play[i] += 1
        if (i - 1 >= 0 and next_play[i - 1] != -1):
            next_play[i] -= 1
            heuristic += 0.2 * minimize(counter+1, make_state(state, i - 1, '2'))[1]
            next_play[i] += 1
        if (i + 1 <= 6 and next_play[i + 1] != -1):
            next_play[i] -= 1
            heuristic += 0.2 * minimize(counter+1, make_state(state, i + 1, '2'))[1]
            next_play[i] += 1

        return heuristic

    elif (counter-1)%4==3:     # minimizing
        heuristic = 0
        if (next_play[i] != -1):
            next_play[i] -= 1
            heuristic += 0.6 * maximize(counter + 1, make_state(state, i, '1'))[1]
            next_play[i] += 1
        if (i - 1 >= 0 and next_play[i - 1] != -1):
            next_play[i] -= 1
            heuristic += 0.2 * maximize(counter + 1, make_state(state, i - 1, '1'))[1]
            next_play[i] += 1
        if (i + 1 <= 6 and next_play[i + 1] != -1):
            next_play[i] -= 1
            heuristic += 0.2 * maximize(counter + 1, make_state(state, i + 1, '1'))[1]
            next_play[i] += 1

        return heuristic

    return 0


while sum(next_play)!=-7:
    print("computer turn:")
    mmm=maximize(1,grid)
    col=mmm[0]
    print("\n My heuristic is \n")
    print(mmm[1])
    connect4_board[next_play[col]][col]='1'
    index=next_play[col]*7+col
    #grid[next_play[col]*7+col]='1'
    grid=grid[:index]+'1'+grid[index+1:]
    next_play[col]-=1

    for i in range(6):
        print(connect4_board[i])

    x=input("enter a column :")
    connect4_board[next_play[int(x)]][int(x)]='2'
    index = next_play[int(x)] * 7 + int(x)
    grid = grid[:index] + '2' + grid[index + 1:]
    next_play[int(x)]-=1

    for i in range(6):
        print(connect4_board[i])

