from datetime import datetime

from Agents.Heuristic_Lec import Heuristic_Lec
from Agents.Node import Node
from Agents.Solver import Solver

class Expectiminmax(Solver):
    def __init__(self, max_depth, heuristic):
        self.limit=max_depth
        self.grid = ""
        self.next_play = []
        self.eval_heuristic=heuristic.eval
        self.state_node_map={}    #map



    def make_state(self,grid,i,p):

        index=self.next_play[i]*7+i

        state=grid[:index]+p+grid[index+1:]
        return state

    def maximize(self,counter,state):     # computer

        if(self.state_node_map.__contains__(state)):
            return None,self.state_node_map[state][0] ,self.state_node_map[state][1]
        node=Node()
        node.type = "MAX"
        if self.limit-counter==0:
            node.value=self.eval_heuristic(state)
            node.children=None
            self.state_node_map[state]=[node.value,node]
            return None,node.value,node



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
                node.children.append(heuristic[1])
                if heuristic[0] > maxEvaluation:
                    max_column=i
                    maxEvaluation=heuristic[0]
                    node.value=maxEvaluation
           else:
               fail_count+=1
        if fail_count==7:
            node.value = self.eval_heuristic(state)
            self.state_node_map[state] = [node.value, node]
            return None, node.value, node
        self.state_node_map[state] = [node.value, node]
        return max_column,node.value,node


    def minimize(self,counter,state):     # human

        if (self.state_node_map.__contains__(state)):
            return None, self.state_node_map[state][0], self.state_node_map[state][1]
        node = Node()
        node.type = "MIN"
        if self.limit - counter == 0:
            node.value = self.eval_heuristic(state)
            node.children = None
            self.state_node_map[state] = [node.value, node]
            return None, node.value, node

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
                node.children.append(heuristic[1])
                if heuristic[0] < min_evaluation:
                    min_column = i
                    min_evaluation = heuristic[0]
                    node.value=min_evaluation
           else:
               fail_count+=1

        if fail_count==7:
            node.value=self.eval_heuristic(state)
            self.state_node_map[state] = [node.value, node]
            return None,node.value,node
        self.state_node_map[state] = [node.value, node]
        return min_column, node.value,node


    def chance(self,counter, state, i):      #chance node

        if (self.state_node_map.__contains__(state)):
            return  self.state_node_map[state][0], self.state_node_map[state][1]
        node = Node()
        node.type = "EXPECTATION"
        if self.limit - counter == 0:
            node.value = self.eval_heuristic(state)
            node.children = None
            self.state_node_map[state] = [node.value, node]
            return node.value, node

        heuristic=0
        if (counter-1)%4==1:   #Maximizing
            if (self.next_play[i] != -1):
                x=self.make_state(state, i, '1')
                self.next_play[i] -= 1
                data=self.minimize(counter+1, x)
                heuristic += 0.6 * data[1]
                node.children.append(data[2])
                self.next_play[i] += 1
            if (i - 1 >= 0 and self.next_play[i - 1] != -1):
                x=self.make_state(state, i - 1, '1')
                self.next_play[i-1] -= 1
                data = self.minimize(counter + 1, x)
                heuristic += 0.2 * data[1]
                node.children.append(data[2])
                self.next_play[i-1] += 1
            if (i + 1 <= 6 and self.next_play[i + 1] != -1):
                x=self.make_state(state, i + 1, '1')
                self.next_play[i+1] -= 1
                data = self.minimize(counter + 1, x)
                heuristic += 0.2 * data[1]
                node.children.append(data[2])
                self.next_play[i+1] += 1

            node.value=heuristic
            return node.value,node

        elif (counter-1)%4==3:     # minimizing
            if (self.next_play[i] != -1):
                x=self.make_state(state, i, '2')
                self.next_play[i] -= 1
                data = self.maximize(counter + 1, x)
                heuristic += 0.6 * data[1]
                node.children.append(data[2])
                self.next_play[i] += 1
            if (i - 1 >= 0 and self.next_play[i - 1] != -1):
                x=self.make_state(state, i - 1, '2')
                self.next_play[i-1] -= 1
                data = self.maximize(counter + 1, x)
                heuristic += 0.2 * data[1]
                node.children.append(data[2])
                self.next_play[i-1] += 1
            if (i + 1 <= 6 and self.next_play[i + 1] != -1):
                x=self.make_state(state, i + 1, '2')
                self.next_play[i+1] -= 1
                data = self.maximize(counter + 1, x)
                heuristic += 0.2 * data[1]
                node.children.append(data[2])
                self.next_play[i+1] += 1

            node.value=heuristic
            return node.value,node

        return 0

    def play(self, currentState):
        self.grid = ""
        self.next_play = [-1, -1, -1, -1, -1, -1, -1]
        self.state_node_map={}
        for i in range(6):
            for j in range(7):
                if (currentState[i][j] == '0'):
                    self.next_play[j] = max(self.next_play[j], i)
                self.grid += currentState[i][j]

        print(self.grid)
        print(self.next_play)

        return self.maximize(1, self.grid)



# if __name__ == "__main__":
#     st_time = datetime.now()
#     minmax = Expectiminmax(9, heuristic=Heuristic_Lec())
#     col, score = minmax.play([
# ['0', '0', '0', '0', '0', '0', '0'] ,
# ['0', '0', '0', '0', '0', '0', '0'] ,
# ['0', '0', '0', '0', '0', '0', '0'] ,
# ['0', '0', '0', '0', '0', '0', '0'] ,
# ['0', '0', '0', '0', '0', '0', '0'] ,
# ['0', '0', '0', '0', '0', '0', '0']
# ])
#     print(col)
#     print((datetime.now() - st_time).total_seconds())


if __name__ == "__main__":
     st_time = datetime.now()
     connect4_board = [
        ['0', '0', '0', '0', '0', '0', '0'] ,
        ['0', '0', '0', '0', '0', '0', '0'] ,
        ['0', '0', '0', '0', '0', '0', '0'] ,
        ['0', '0', '0', '0', '0', '0', '0'] ,
        ['0', '0', '0', '0', '0', '0', '0'] ,
        ['0', '0', '0', '0', '0', '0', '0']
        ]

     global_next_play=[5,5,5,5,5,5,5]
     expecti=Expectiminmax(8,heuristic=Heuristic_Lec())
     while sum(global_next_play)!=-7:
            st_time = datetime.now()
            print("computer turn:")
            mmm=expecti.play(connect4_board)
            col=mmm[0]
            print("I  choose column : "+str(col))
            print("\n My heuristic is \n")
            print(mmm[1])
            connect4_board[global_next_play[col]][col]='1'
            index=global_next_play[col]*7+col
            global_next_play[col]-=1

            for i in range(6):
                print(connect4_board[i])
            print((datetime.now() - st_time).total_seconds())
            print("\n")
            x=input("enter a column :")
            connect4_board[global_next_play[int(x)]][int(x)]='2'
            index = global_next_play[int(x)] * 7 + int(x)
            global_next_play[int(x)]-=1

            for i in range(6):
                print(connect4_board[i])

