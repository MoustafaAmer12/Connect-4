
def string_index(index):
    return index//7,index% 7

def grid_index(i,j):
    return i*7+j
def valid(i,j):
    return not (i>5 or i<0 or j>6 or j<0)
def shift_to_grid(shift):
    if(shift==1):
        return 0,1
    elif shift==7:
        return 1,0
    elif shift==8:
        return 1,1
    elif shift==6:
        return 1,-1

def score(grid,index,p, shift,player):

    g_index= string_index(index)
    shift_margin=shift_to_grid(shift)
    counter=0
    for i in range(4):
        new_index=[g_index[0]+shift_margin[0]*i,g_index[1]+shift_margin[1]*i]
        if(valid(new_index[0], new_index[1]) and grid[grid_index(new_index[0], new_index[1])]==player):
            #print(new_index)
            counter+=1
        else:
            break

    # print(counter)
    # print("\n")
    minus_shift=[g_index[0]-shift_margin[0],g_index[1]-shift_margin[1]]
    three_shift=[g_index[0] + 3 * shift_margin[0], g_index[1] + 3 * shift_margin[1]]
    two_shift=[g_index[0] + 2 * shift_margin[0], g_index[1] + 2 * shift_margin[1]]
    if(counter==4):
        p[0]+=1
    elif (counter == 3) and (((valid(minus_shift[0], minus_shift[1]))and grid[grid_index(minus_shift[0], minus_shift[1])] == '0' and (not valid(minus_shift[0]+1,minus_shift[1]) or grid[grid_index(minus_shift[0]+1,minus_shift[1])]!='0'))
          or ((valid(three_shift[0], three_shift[1]) and grid[grid_index(three_shift[0], three_shift[1])] == '0') and (not valid(three_shift[0] + 1, three_shift[1]) or grid[grid_index(three_shift[0] + 1, three_shift[1])] != '0'))):
        p[1]+=1
    elif (counter == 2) and (((valid(minus_shift[0], minus_shift[1])) and grid[grid_index(minus_shift[0], minus_shift[1])] == '0' and (not valid(minus_shift[0] + 1, minus_shift[1]) or grid[grid_index(minus_shift[0] + 1, minus_shift[1])] != '0'))
          or ((valid(two_shift[0], two_shift[1]) and grid[grid_index(two_shift[0], two_shift[1])] == '0') and (not valid(two_shift[0] + 1, two_shift[1]) or grid[grid_index(two_shift[0] + 1, two_shift[1])] != '0'))):
        p[2]+=1


    # print(p[0])
    # print(p[1])
    # print(p[2])

def cell_score(grid, i,p):
    #print("UP")
    score(grid, i, p,7,grid[i])  #up
    #print("Right")
    score(grid, i, p, 1,  grid[i])  #right
    #print("Diagonal_Right")
    score(grid, i, p, 8, grid[i])  #diagonal_left
    #print("Diagonal_Right")
    score(grid, i, p, 6,  grid[i])  #diagonal_right


def get_score(grid):
    p1=[0,0,0]
    p2=[0,0,0]
    for i in range(42):
       if grid[i]=='1':
        cell_score(grid,i,p1)
       elif grid[i]=='2':
         cell_score(grid,i,p2)
    x=[10000,5000,1000]
    heuristic=0
    for i in range(3):
       heuristic+=x[i]*(p1[i]-p2[i])
    return heuristic

def MakeTest(Grid):
    grid=""
    for i in range(6):
        for j in range(7):
            grid+=str(Grid[i][j])

    return grid

# connect4_board = [
#     ['2', '2', '1', '1', '1', '1', '2'],
#     ['1', '1', '1', '1', '1', '1', '2'],
#     ['1', '2', '2', '1', '2', '2', '1'],
#     ['2', '1', '2', '2', '2', '1', '2'],
#     ['2', '1', '2', '2', '1', '2', '2'],
#     ['2', '1', '1', '1', '1', '2', '2']
#
# ]

# print(get_score(MakeTest(connect4_board)))  # it must print 1 0 0   # it now prints 1 1 1