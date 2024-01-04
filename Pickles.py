# Authors: Pickels
import os
import cv2
import numpy as np
import random
from tabulate import tabulate
from IPython.display import clear_output


class Solve8:
    @staticmethod
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

    @staticmethod
    def nextState(board, move):
        givenBoard = board
        # get the position of the empty tile
        pos = np.where(givenBoard == 0)
        # get the new position of the empty tile
        new_pos = [pos[0][0] + move[0], pos[1][0] + move[1]]
        # create a copy of the board
        new_board = givenBoard.copy()
        # swap the empty tile with the new position
        new_board[pos[0][0]][pos[1][0]] = new_board[new_pos[0]][new_pos[1]]
        new_board[new_pos[0]][new_pos[1]] = 0
        # return the new board
        return new_board

    
    def Solve(me, board):
        givenBoard = board.Board
        initial_state = givenBoard
        # Check if the initial state is the goal state
        if np.array_equal(initial_state, np.array([[1,2,3],[4,5,6],[7,8,0]])):
            print("The initial state is the goal state")
            return []
        # define the open and closed lists
        # The lists will contain the following information:
        # [state_id, state, parent_id, g, f, move]
        open_list = []
        closed_list = []
        # define a state id to keep track of the states
        state_id = 0
        # Add the initial state to the open list
        open_list.append([state_id, initial_state, 0, 0, 0, None])
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
                    path.append(current_state[5])
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
            possible_moves = Solve8.possibleMoves(current_state[1])
            # loop through the possible moves
            for move in possible_moves:
                # get the next state
                next_state = Solve8.nextState(current_state[1], move)
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
                    # add the move to the path
                    path.append(move)
                    # loop until the current state is the initial state
                    while current_state_id != 0:
                        # add the move to the path
                        path.append(current_state[5])
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
                f = g + Solve8.manhattanDistance(next_state)
                # add the state to the open list
                open_list.append([state_id, next_state, current_state_id, g, f, move])
                # increment the state id
                state_id += 1
            # increment the iteration
            iteration += 1
        # return an empty path if the open list is empty
        print("The open list is empty, no path found")
        return []
