from board import *
import copy
import heapq


##################### SOLVE.PY Code ######################

def a_star_sort_key(e):
    return (e.depth + e.f, e.id, e.parent.id)

def a_star(init_board, hfn):
    """
    Run the A_star search algorithm given an initial board and a heuristic function.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns an empty list and -1.

    :param init_board: The initial starting board.
    :type init_board: Board
    :param hfn: The heuristic function.
    :type hfn: Heuristic
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """
    start_state = State(init_board, hfn, hfn(init_board), 0, None)
    # frontier = [(start_state.depth + start_state.f, start_state, start_state.id, start_state.id)]
    frontier = [start_state]
    explored = []
    while frontier:
        # curr_tuple = frontier.pop(0)
        # curr_state = curr_tuple[1]
        # if explored.count(curr_state) == 0:
        #     explored.append(curr_state)
        #     if (is_goal(curr_state)):
        #         return (get_path(curr_state), curr_state.depth)
        #     for s in get_successors(curr_state):
        #         frontier.append((s.depth + s.f, s, s.id, curr_state.id))
        #     frontier.sort(key=a_star_sort_key)


        curr_state = frontier.pop(0)
        if explored.count(curr_state) == 0:
            explored.append(curr_state)
            if (is_goal(curr_state)):
                return (get_path(curr_state), curr_state.depth)
            for s in get_successors(curr_state):
                frontier.append(s)
            frontier.sort(key=a_star_sort_key)

    return ([], -1)


def state_sort(s):
    return s.id

def dfs(init_board):
    """
    Run the DFS algorithm given an initial board.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns an empty list and -1.

    :param init_board: The initial board.
    :type init_board: Board
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """
    start_state = State(init_board, zero_heuristic, 0, 0, None)
    frontier = [start_state]
    explored = []
    while frontier:
        curr_state = frontier.pop(-1)
        if explored.count(curr_state) == 0:
            explored.append(curr_state)
            if (is_goal(curr_state)):
                return (get_path(curr_state), curr_state.depth)
            successors = get_successors(curr_state)
            successors.sort(reverse=True, key=state_sort)
            frontier.extend(successors)
    return ([], -1)


#################### Helper Functions of get_successor ##################### 

def check_coord(x, y, board):
    """
    Return True if (x, y) is valid to be moved to on board. Otherwise, False.

    :param x: The x coordinate on board.
    :type state: int
    :param y: The y coordinate on board.
    :type state: int
    :param board: The board we are checking
    :type state: Board
    :return: if the position on board is safe to move to
    :rtype: Boolean
    """
    return x >= 0 and y >= 0 and x < board.size and y < board.size and board.grid[x][y] == '.'

def generate_child_state(state, car_var_coord, car_num):
    """
    Return a State containing the successor state of the given state by moving the 
        car numbered car_num to car_var_coord

    :param state: The current state.
    :type state: State
    :param car_var_coord: The var_coord the car is going to change to
    :type state: int
    :param car_num: The position of the car in the cars list
    :type state: int
    :return: The successor state.
    :rtype: State
    """
    car_list = copy.deepcopy(state.board.cars)
    car_list[car_num].var_coord = car_var_coord
    new_board = Board(state.board.name + "1", state.board.size, car_list)
    new_state = State(new_board, state.hfn, state.hfn(new_board), state.depth + 1, state)
    return new_state

#################### Helper Functions of get_successor END ##################### 


def get_successors(state):
    """
    Return a list containing the successor states of the given state.
    The states in the list may be in any arbitrary order.

    :param state: The current state.
    :type state: State
    :return: The list of successor states.
    :rtype: List[State]
    """


    successors = []
    for i in range(len(state.board.cars)):
        car_var_coord = state.board.cars[i].var_coord
        car_fixed_coord = state.board.cars[i].fix_coord
        car_length = state.board.cars[i].length
        if state.board.cars[i].orientation == 'v':
            # move forward
            while (check_coord(car_var_coord - 1, car_fixed_coord, state.board)):
                car_var_coord -= 1;
                successors.append(generate_child_state(state, car_var_coord, i))

            # move backward
            car_var_coord = state.board.cars[i].var_coord
            while (check_coord(car_var_coord + car_length, car_fixed_coord, state.board)):
                car_var_coord += 1;
                successors.append(generate_child_state(state, car_var_coord, i))
        else:
            # move forward
            while (check_coord(car_fixed_coord, car_var_coord - 1, state.board)):
                car_var_coord -= 1;
                successors.append(generate_child_state(state, car_var_coord, i))
            # move backward
            car_var_coord = state.board.cars[i].var_coord
            while (check_coord(car_fixed_coord, car_var_coord + car_length, state.board)):
                car_var_coord += 1;
                successors.append(generate_child_state(state, car_var_coord, i))
    return successors






## Week One
def is_goal(state):
    """
    Returns True if the state is the goal state and False otherwise.

    :param state: the current state.
    :type state: State
    :return: True or False
    :rtype: bool
    """
    GOALPOS = 4
    for c in state.board.cars:
        if c.is_goal is True:
            return c.var_coord == GOALPOS
    return False

## Week One
def get_path(state):
    """
    Return a list of states containing the nodes on the path 
    from the initial state to the given state in order.

    :param state: The current state.
    :type state: State
    :return: The path.
    :rtype: List[State]
    """
    curr_state = state
    los = []
    while curr_state is not None:
        los.append(curr_state)
        curr_state = curr_state.parent
    los.reverse()
    return los

## Week One
def blocking_heuristic(board):
    """
    Returns the heuristic value for the given board
    based on the Blocking Heuristic function.

    Blocking heuristic returns zero at any goal board,
    and returns one plus the number of cars directly
    blocking the goal car in all other states.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """

    EXIT_MOVE = 1
    COORD_Y = 2

    count = EXIT_MOVE
    for pos in range(board.size):
        curr_block = board.grid[COORD_Y][pos]
        if curr_block == '>':
            count = EXIT_MOVE
            if pos == board.size - 1:
                return 0
        elif curr_block != '.':
            count += 1
    return count





########## Week Three ########

def get_list_of_blocked_x(board):
    """
    find a list of x axis coodinates that blocking the goal car

    :param board: The current board.
    :type board: Board
    :return: a list of x axis coodinates that blocking the goal car
    :rtype: List[Int]
    """
    COORD_Y = 2
    lox = []
    for pos in range(board.size):
        curr_block = board.grid[COORD_Y][pos]
        if curr_block == '>':
            lox = []
        elif curr_block != '.':
            lox.append(pos)
    return lox
    


def is_car_blocking_xy(car, x, y):
    """
    Determines if the car blocks (x, y) coordinate
    
    :requires: the car has to be vertical
    :param car: The current car.
    :type car: Car
    :return: True if car blocks (x, y). Otherwise, false
    :rtype: Boolean
    """
    if car.orientation == 'v':
        if car.fix_coord == x:
            if y >= car.var_coord and y <= car.length + car.var_coord - 1:
                return True
    return False



def get_list_of_blocking_cars(cars, list_of_blocked_x):
    COORD_Y = 2
    loc = []
    for i in range(len(cars)):
        for x in list_of_blocked_x:
            if is_car_blocking_xy(cars[i], x, COORD_Y):
                loc.append(cars[i])
    return loc


def is_car_blocked(car, board):
    """
    Determines if the car is also blocked on board, which mean it can
    not move away within one step

    :param car: The car blocks the goal car.
    :type car: Car
    :param board: The current board
    :type car: Board
    :return: True if car cannot move away. Otherwise, false
    :rtype: Boolean
    """
    COORD_Y = 2
    is_blocked = False

    car_var_coord = car.var_coord
    car_fixed_coord = car.fix_coord
    car_length = car.length

    while (check_coord(car.var_coord - 1, car.fix_coord, board)):
        car.var_coord -= 1;
        if is_car_blocking_xy(car, car.fix_coord, COORD_Y) is False:
            car.var_coord = car_var_coord
            return False

    car.var_coord = car_var_coord
    while (check_coord(car.var_coord + car_length, car_fixed_coord, board)):
        car.var_coord += 1;
        if is_car_blocking_xy(car, car.fix_coord, COORD_Y) is False:
            car.var_coord = car_var_coord
            return False
    car.var_coord = car_var_coord
    return True



def advanced_heuristic_version_two(board):
    """
    An advanced heuristic of your own choosing and invention.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """

    list_of_blocked_x = get_list_of_blocked_x(board)
    list_of_blocking_cars = get_list_of_blocking_cars(board.cars, list_of_blocked_x)
    count = 0
    for i in range(len(list_of_blocking_cars)):
        if (is_car_blocked(list_of_blocking_cars[i], board)):
            count += 1;
        count += 1
    if count != 0:
        count += 1
    return count


def is_car_blocked_version_two(x, board):
    """
    Determines if the car is also blocked on board, which mean it can
    not move away within one step

    :param car: The car blocks the goal car.
    :type car: Car
    :param board: The current board
    :type car: Board
    :return: True if car cannot move away. Otherwise, false
    :rtype: Boolean
    """
    COORD_Y = 2

    pos_head = COORD_Y;
    pos_tail = COORD_Y;

    while (board.grid[pos_head][x] != '^'):
        pos_head -= 1;
    while (board.grid[pos_tail][x] != 'v'):
        pos_tail += 1;

    car_length = pos_tail - pos_head + 1

    while (pos_head - 1 >= 0 and board.grid[pos_head - 1][x] == '.'):
        pos_head -= 1

    while (pos_tail + 1 < board.size and board.grid[pos_tail + 1][x] == '.'):
        pos_tail += 1

    head_blocked = (pos_head + car_length - 1) >= COORD_Y
    tail_blocked = (pos_tail - car_length + 1) <= COORD_Y
    return head_blocked and tail_blocked


def advanced_heuristic(board):
    """
    An advanced heuristic of your own choosing and invention.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """
    if board.grid[2][board.size - 1] == '>':
        return 0
    list_of_blocked_x = get_list_of_blocked_x(board)
    count = 1
    for x in list_of_blocked_x:
        if is_car_blocked_version_two(x, board) is True:
            count += 1;
        count += 1
    return count



##################### END ######################
