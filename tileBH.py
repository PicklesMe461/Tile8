import os
import cv2
import numpy as np
import random
from tabulate import tabulate
from IPython.display import clear_output


class EightTile():
    '''
    This class implements a basic 8-tile board when instantiated
    You can shuffle it using shuffle() to generate a puzzle
    After shuffling, you can use manual moves using ApplyMove()
    '''
    def __init__(me):
        # board is a numpy array
        me.__board = np.array([[1,2,3],[4,5,6],[7,8,0]])
        me.__winner = me.__board.copy() # by default a winning board is givenq
        # keep track of where 0 is, you can also use np.where, but I like it better this way
        me.__x, me.__y = 2, 2 # initially it is at the bottom right corner


    def shuffle(me, n = 1, debugON = False):
        '''
        randomly moves the empty tile, (i.e. the 0 element) around the gameboard
        n times and returns the moves from the initial to the last move
        Input:
            n: number of shuffles to performe, defaults to 1
        Output:
            a list of n entries [ [y1, x2], [y2, x2], ... , [yn, xn]]
            where [yi, xi] is the relative move of the empty tile at step i
            ex: [-1, 0] means that empty tile moved left horizontally
                note that:
                    on the corners there 2 moves
                    on the edges there are 3 moves
                    only at the center there are 4 moves

        Hence if you apply the negative of the returned list to the board
        step by step the puzzle should be solved!
        Check out ApplyMove()
        '''
        # depending on the current index possible moves are listed
        # think of alternative ways of achieving this, without using if conditions
        movez = [[0,1], [-1,0,1], [-1,0]]
        trace = []
        dxold, dyold = 0, 0 # past moves are tracked to be avoided, at first no such history
        for i in range(n):
            # note that move is along either x or y, but not both!
            # also no move at all is not accepted
            # we should also avoid the last state, i.e. an opposite move is not good
            dx, dy = 0, 0 # initial move is initialized to no move at all
            while ( dx**2 + dy**2 != 1 ) or (dx == -dxold and dy == -dyold): # i.e. it is either no move or a diagonal move
                dx = random.choice(movez[me.__x])
                dy = random.choice(movez[me.__y])
            # now that we have the legal moves, we also have the new coordinates
            xn, yn = me.__x+dx, me.__y+dy # record new coordinates
            trace.append([dy, dx]) # just keeping track of the move not the absolute position tomato, tomato
            me.__board[me.__y, me.__x], me.__board[yn, xn] = me.__board[yn, xn], me.__board[me.__y, me.__x]
            # enable print if debug is desired
            if debugON:
                print(f'shuffle[{i}]: {me.__y},{me.__x} --> {yn},{xn}\n{me}\n')
            # finally update positions as well
            me.__x, me.__y = xn, yn

            dxold, dyold = dx, dy # keep track of old moves to avoid oscillations

        # finally return the sequence of shuffles
        # note that if negative of trace is applied to the board in reverse order board should reset!
        return trace

    def ApplyMove(me, move):
        '''
        applies a single move to the board and updates it
        move is a list such that [deltaY, deltaX]
        this is manual usage, so it does not care about the previous moves
        '''
        dy, dx = move[0], move[1]
        xn, yn = me.__x+dx, me.__y+dy # record new coordinates
        if ( dx**2 + dy**2 == 1 and 0<=xn<=2 and 0<=yn<=2 ): # then valid
            me.__board[me.__y, me.__x], me.__board[yn, xn] = me.__board[yn, xn], me.__board[me.__y, me.__x]
            me.__x, me.__y = xn, yn
            return True
        else:
            return False

    def __str__(me):
        '''
        generates a printable version of the board
        note that * is the empty space and in the numpy representation of
        the board it is 0 (zero)
        '''
        return tabulate([[str(x).replace('0', '*') for x in c]  for c in np.ndarray.tolist(me.__board)], tablefmt="grid", stralign="center")

    @property
    def Position(me):
        # returns the position of the empty cell
        return [me.__y, me.__x]

    @property
    def Board(me):
        # returns a numpy array stating the current state of the board
        return me.__board.copy() # return a copy of the numpy array

    @property
    def isWinner(me):
        # returns true, if current board is a winner
        return np.array_equal(me.__winner, me.__board)
    

# Manhattan distance calculation function
def manhattanDistance(board):
    # initialize the distance to 0
    distance = 0
    # loop through the board
    for i in range(3):
        for j in range(3):
            # check if the value is not 0
            if board[i][j] != 0:
                # calculate the distance of the value from its correct position
                distance += abs(i - (board[i][j] - 1) // 3) + abs(j - (board[i][j] - 1) % 3)
    # return the distance
    return distance

# Function to return the possible moves
def possibleMoves(board):
    # initialize the possible moves list
    moves = []
    # get the position of the empty tile
    pos = np.where(board == 0)
    # check if the empty tile is not on the first row
    if pos[0] != 0:
        # add the move to the list
        moves.append([-1, 0])
    # check if the empty tile is not on the last row
    if pos[0] != 2:
        # add the move to the list
        moves.append([1, 0])
    # check if the empty tile is not on the first column
    if pos[1] != 0:
        # add the move to the list
        moves.append([0, -1])
    # check if the empty tile is not on the last column
    if pos[1] != 2:
        # add the move to the list
        moves.append([0, 1])
    # return the list of possible moves
    return moves

# Function to return the next state when a move is applied
def nextState(board, move):
    # get the position of the empty tile
    pos = np.where(board == 0)
    # get the new position of the empty tile
    new_pos = [pos[0][0] + move[0], pos[1][0] + move[1]]
    # create a copy of the board
    new_board = board.copy()
    # swap the empty tile with the new position
    new_board[pos[0][0]][pos[1][0]] = new_board[new_pos[0]][new_pos[1]]
    new_board[new_pos[0]][new_pos[1]] = 0
    # return the new board
    return new_board


# A* algorithm to solve the puzzle and return the path
def aStar(board):
    initial_state = board
    # Check if the initial state is the goal state
    if np.array_equal(initial_state, np.array([[1,2,3],[4,5,6],[7,8,0]])):
        print("The initial state is the goal state")
        return []
    # define the open and closed lists
    # The lists will contain the following information:
    # [state_id, state, parent_id, g, f]
    open_list = []
    closed_list = []
    # define a state id to keep track of the states
    state_id = 0
    # Add the initial state to the open list
    open_list.append([state_id, initial_state, 0, 0, 0])
    # increment the state id
    state_id += 1
    # initialize the iteration
    iteration = 0
    # loop until the open list is empty
    while len(open_list) != 0 and iteration < 1000:
        # sort the open list based on the f value
        open_list.sort(key=lambda x: x[4])
        # get the first state from the open list
        current_state = open_list[0]
        # Check if the current state is the goal state
        if np.array_equal(current_state[1], np.array([[1,2,3],[4,5,6],[7,8,0]])):
            # initialize the path
            path = []
            # loop until the current state is the initial state
            while current_state[2] != 0:
                # add the move to the path
                path.append(current_state[1])
                # find the parent state by looping through the closed list by id
                for state in closed_list:
                    if state[0] == current_state[2]:
                        current_state = state
                        break
                    
 
            # return the reversed path and print the number of iterations
            print("The number of iterations is: ", iteration)
            return path[::-1]
        # remove the current state from the open list
        open_list.pop(0)
        # add the current state to the closed list
        closed_list.append(current_state)
        # record the current state id
        current_state_id = current_state[0]
        # expand the current state
        possible_moves = possibleMoves(current_state[1])
        # loop through the possible moves
        for move in possible_moves:
            # get the next state
            next_state = nextState(current_state[1], move)
            # loop through the closed list to check if the state is already there
            state_in_closed_list = False
            for state in closed_list:
                if np.array_equal(state[1], next_state):
                    state_in_closed_list = True
                    break
            # if the state is in the closed list, skip it
            if state_in_closed_list:
                continue
            #loop through the open list to check if the state is already there
            state_in_open_list = False
            for state in open_list:
                if np.array_equal(state[1], next_state):
                    state_in_open_list = True
                    break
            # if the state is in the open list skip it
            if state_in_open_list:
                continue
            # check if the state is the goal state
            if np.array_equal(next_state, np.array([[1,2,3],[4,5,6],[7,8,0]])):
                # initialize the path
                path = []
                # loop until the current state is the initial state
                while current_state_id != 0:
                    # add the move to the path
                    path.append(current_state[1])
                    # find the parent state by looping through the closed list by id
                    for state in closed_list:
                        if state[0] == current_state[2]:
                            current_state = state
                            break
                    # get the current state id
                    current_state_id = current_state[0]
                # return the reversed path and print the number of iterations
                print("The number of iterations is: ", iteration)
                return path[::-1]
            # calculate the g value
            g = current_state[3] + 1
            # calculate the f value
            f = g + manhattanDistance(next_state)
            # add the state to the open list
            open_list.append([state_id, next_state, current_state_id, g, f])
            # increment the state id
            state_id += 1
        # increment the iteration
        iteration += 1
    # return an empty path if the open list is empty
    print("The open list is empty, no path found")
    return []
















t = EightTile()
movez = t.shuffle(4, debugON=True) # for longer shuffle series consider not printing :)
print(movez)
print(t)
print(manhattanDistance(t.Board))
print("Here is the path found")
foundPath = aStar(t.Board)
print(foundPath)
# Apply found Path
for move in foundPath:
    t.ApplyMove(move)

print(t)




'''
print(possibleMoves(t.Board))
print("Here are the next states:")
for move in possibleMoves(t.Board):
    print(nextState(t.Board, move))
'''
