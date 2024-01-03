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
    




t = EightTile()
movez = t.shuffle(3, debugON=True) # for longer shuffle series consider not printing :)
print(movez)