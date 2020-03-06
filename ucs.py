from itertools import combinations
import random
import time
import queue
import random
from operator import mul    # or mul=lambda x,y:x*y
from fractions import Fraction
from functools import reduce

print('Enter n: ')
size = int(input())

if(size == 8):
    ll=create_matrix(8)
    ll[0][0]=1
    ll[4][1]=1
    ll[7][2]=1
    ll[5][3]=1
    ll[2][4]=1
    ll[6][5]=1
    ll[1][6]=1
    ll[3][7]=1


    print("""
1  0  0  0  0  0  0  0
0  0  0  0  0  0  1  0
0  0  0  0  1  0  0  0
0  0  0  0  0  0  0  1
0  1  0  0  0  0  0  0
0  0  0  1  0  0  0  0
0  0  0  0  0  1  0  0
0  0  1  0  0  0  0  0
    """)



def create_matrix(length):
    map = []
    for i in range(length):
        map.append(list())

    for row in range(length):
        for column in range(length):
            map[row].append(0)


    return map

def create_matrix_start(length):
    map = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[1,1,1,1]]

    return map

class State:
    def __init__(self):
        self.map = create_matrix(size)
        #print("hello")
        #print(self.map);
        self.c = 0
        self.h = 0
        self.prev = None
        self.next = None

    def show(self):
        print('---------------')
        for row in range(size):
            print(self.map[row])

    def __lt__(self, other):
        return True


def copy_list(src):
    des = create_matrix(size)
    for row in range(size):
        for column in range(size):
            des[row][column] = src[row][column]
    return des


def find_state(state, new_state):
    temp = state.prev
    while temp is not None:
        if temp.map == new_state.map:
            return True
        temp = temp.prev

    return False


def cal_sum_right_line(arr, row, column):
    sum = 0
    sum += arr[row][column]

    temp_row = row + 1
    temp_column = column + 1

    while -1 < temp_row < size and -1 < temp_column < size:
        sum += arr[temp_row][temp_column]
        temp_row += 1
        temp_column += 1

    return sum


def cal_sum_left_line(arr, row, column):
    sum = 0
    sum += arr[row][column]

    temp_row = row + 1
    temp_column = column - 1
    while -1 < temp_row < size and -1 < temp_column < size:
        sum += arr[temp_row][temp_column]
        temp_row += 1
        temp_column -= 1

    return sum


def cal_sum_row(arr, row):
    sum = 0
    for column in range(size):
        sum += arr[row][column]

    return sum


def check_rows(arr):
    for row in range(size):
        sum = cal_sum_row(arr, row)

        if sum > 1:
            return False

    return True


def check_left_line(arr):
    for row in range(size):
        sum = cal_sum_left_line(arr, row, size - 1)
        if sum > 1:
            return False

    for column in range(size):
        sum = cal_sum_left_line(arr, 0, column)
        if sum > 1:
            return False

    return True


def check_right_line(arr):
    for row in range(size):
        sum = cal_sum_right_line(arr, row, 0)
        if sum > 1:
            return False

    for column in range(size):
        sum = cal_sum_right_line(arr, 0, column)
        if sum > 1:
            return False

    return True

class Util:
    def __init__(self):
        self.current_state = State()

    def random_start_state(self):
        new_state = State()
        for i in range(size):
            row = random.randint(0, size - 1)
            new_state.map[row][i] = 1
        # new_state.map=create_matrix_start(4)
        return new_state

    def goal(self, state):
        if not check_right_line(state.map):
            return False
        if not check_left_line(state.map):
            return False
        if not check_rows(state.map):
            return False

        return True

    def action(self, state):
        neighbor_states = []
        for column in range(size):
            for row in range(size):
                if state.map[row][column] == 1:
                    # print("row {}, column {}".format(row, column))
                    adj_row = []
                    for i in range(size):
                        adj_row.append(i)
                    # print("Adjacent before: ", adj_row)
                    adj_row.remove(row)
                    # print("Adjacent after: ", adj_row)
                    for new_row in adj_row:
                        # print("*****", new_row)
                        new_state = State()
                        new_state.map = copy_list(state.map)
                        new_state.map[row][column] = 0
                        new_state.map[new_row][column] = 1

                        if not find_state(state, new_state):
                            new_state.prev = state
                            new_state.c = state.c + 1
                            neighbor_states.append(new_state)
                    #break

        return neighbor_states
class UniformCostSearch:
    def __init__(self, start_state, goal, action):
        self.goal = goal

        self.states = queue.PriorityQueue()
        self.closed= []
        self.start_state = start_state
        self.action = action
        self.states.put((start_state.c, start_state))

    def find_goal_state(self, state):
        if self.goal is not None:
            return self.goal(state)

    def push_to_queue(self, new_states):
        for state in new_states:
            # print(state," is the state", "self.closed", self.closed)
            if(state not in self.closed):
                # print("hhhhhhhhhhhhhhhhhhhhhhh")
                self.states.put((state.c, state))
            else:
                print()

    def search(self):

        (value, bs) = self.states.get()
        self.closed.append((value, bs))
        # print(self.closed)
        # print("-------------------",value, bs)
        # if( (value, bs) in self.closed):
        #     print("&&&&&&&&&&&&&&&&&&&&&&&&&&")
        #     return None
        # else:
        #     self.closed.append((value, bs))
        start = time.process_time()
        while not self.find_goal_state(bs):

            neighbor_states = self.action(bs)
            neighbor_states_new=[]
            # print([i[1] for i in self.closed],"-----------------------------------------------------------------")
            # for some_state in neighbor_states:
            #     print(some_state)
            #     if(some_state not in [i[1] for i in self.closed]):
            #         neighbor_states_new.append(some_state)
            #     else:
            #         print("&&&&&&&&&&&&&&&&&&&&&&&&&")
            #         return None
            self.push_to_queue(neighbor_states)
            if not self.states.empty():
                (value, bs1) = self.states.get()
                if(bs1 in self.closed):
                    bs= bs
                else:
                    bs= bs1
                    self.closed.append((value, bs))
                #print("value  ", value, "\nbs   ", bs.show())
            else:
                return None

        duration = time.process_time() - start
        print("duration", duration)
        # print("--==>", self.closed)
        return bs

env = Util()

env.current_state = env.random_start_state()
env.current_state.show()

for i in range(8):
    print(ll[i])
agent = UniformCostSearch(env.current_state, env.goal, env.action)
state = agent.search()

state.show()
