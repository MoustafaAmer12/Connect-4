def score(grid,index,p, shift,player):
    counter=0
    for i in range(4):
        if(index+i*shift<=41 and grid[index+i*shift]==player):
            counter+=1
        else:
            break
    if(counter==4):
        p[0]+=1
    elif(counter==3 and grid[index-shift]!=player) and (grid[index-shift]=='0' or(index+3*shift<41 and grid[index+3*shift]=='0')):
        p[1]+=1
    elif(counter==2 and grid[index-shift]!=player) and (grid[index-shift]=='0' or(index+2*shift<41 and grid[index+2*shift]=='0')):
        p[2]+=1




def cell_score(grid, i,p):

    score(grid, i, p,7,grid[i])  #up
    score(grid, i, p, 1,  grid[i])  #left
    score(grid, i, p, 8, grid[i])  #diagonal_left
    score(grid, i, p, 6,  grid[i])  #diagonal_right


def get_score(grid):
    p1=[0,0,0]
    p2=[0,0,0]
    for i in range(42):
       if grid[i]=='1':
        cell_score(grid,i,p1)
       elif grid[i]=='2':
         cell_score(grid,i,p2)
    x=[1000,800,100]
    heuristic=0
    for i in range(3):
       # print(p1[i]-p2[i])
       heuristic+=x[i]*(p1[i]-p2[i])

    return heuristic

def MakeTest(Grid):
    grid=""
    for i in range(6):
        for j in range(7):
            grid+=str(Grid[i][j])

    return grid

connect4_board = [
    ['2', '1', '2', '2', '1', '2', '2'],
    ['2', '1', '2', '1', '1', '2', '2'],
    ['2', '2', '1', '1', '2', '1', '2'],
    ['2', '1', '2', '1', '1', '1', '2'],
    ['2', '1', '1', '1', '1', '1', '2'],
    ['1', '2', '1', '2', '1', '1', '2']
]

get_score(MakeTest(connect4_board))  # it must print 1 0 0   # it now prints 1 1 1