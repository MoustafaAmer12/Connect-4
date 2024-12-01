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
limit=4
next_play=[5,5,5,5,5,5,5]
game_counter=0

def make_state(grid,i,p):

    index=next_play[i]*7+i

    state=grid[:index]+p+grid[index+1:]
    return state

def maximize(counter,state):     # computer


    if limit-counter==0 or game_counter==42:
        return None,score.get_score(state)


    max_column = -1
    for i in range(7):
        if next_play[i]!=-1:
            max_column=i
            break

    maxEvaluation = -1000000  # large negative

    for i in range(7):
       if next_play[i]!=-1:
            heuristic=chance(counter+1,state,i)

            if heuristic > maxEvaluation:
                max_column=i
                maxEvaluation=heuristic

    return max_column,maxEvaluation


def minimize(counter,state):     # human

    if limit-counter==0 or game_counter==42:
       return None,score.get_score(state)

    min_column = -1
    min_evaluation=1000000
    for i in range(7):           #set to first un inhabitant position
        if (state[next_play[i]*7+i]=='0'):
            min_column = i
            break
    for i in range(7):

       if next_play[i]!=-1 :
            heuristic = chance(counter+1,state,i)
            if heuristic < min_evaluation:
                min_column = i
                min_evaluation = heuristic

    return min_column, min_evaluation


def chance(counter, state, i):      #chance node
    global game_counter
    if limit-counter==0:
        return score.get_score(state)
    heuristic=0
    if (counter-1)%4==1:   #Maximizing
        if (next_play[i] != -1):
            x=make_state(state, i, '1')
            next_play[i] -= 1
            game_counter+=1
            heuristic += 0.6 * minimize(counter+1, x)[1]
            next_play[i] += 1
            game_counter-=1
        if (i - 1 >= 0 and next_play[i - 1] != -1):
            x=make_state(state, i - 1, '1')
            next_play[i-1] -= 1
            game_counter+=1
            heuristic += 0.2 * minimize(counter+1,x)[1]
            next_play[i-1] += 1
            game_counter-=1
        if (i + 1 <= 6 and next_play[i + 1] != -1):
            x=make_state(state, i + 1, '1')
            next_play[i+1] -= 1
            game_counter+=1
            heuristic += 0.2 * minimize(counter+1,x)[1]
            next_play[i+1] += 1
            game_counter-=1

        #print(heuristic)
        return heuristic

    elif (counter-1)%4==3:     # minimizing
        if (next_play[i] != -1):
            x=make_state(state, i, '2')
            next_play[i] -= 1
            game_counter+=1
            heuristic += 0.6 * maximize(counter + 1, x)[1]
            next_play[i] += 1
            game_counter-=1
        if (i - 1 >= 0 and next_play[i - 1] != -1):
            x=make_state(state, i - 1, '2')
            next_play[i-1] -= 1
            game_counter+=1
            heuristic += 0.2 * maximize(counter + 1, x)[1]
            next_play[i-1] += 1
            game_counter-=1
        if (i + 1 <= 6 and next_play[i + 1] != -1):
            x=make_state(state, i + 1, '2')
            next_play[i+1] -= 1
            game_counter+=1
            heuristic += 0.2 * maximize(counter + 1, x)[1]
            next_play[i+1] += 1
            game_counter-=1


        return heuristic

    return 0


while sum(next_play)!=-7:
    print("computer turn:")
    mmm=maximize(1,grid)
    col=mmm[0]
    print("I  choose column : "+str(col))
    print("\n My heuristic is \n")
    print(mmm[1])
    connect4_board[next_play[col]][col]='1'
    index=next_play[col]*7+col
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

