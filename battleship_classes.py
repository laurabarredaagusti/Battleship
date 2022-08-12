import numpy as np
import random
# import os
# import pygame
# from emoji import emojize
import pandas as pd
from time import sleep

from battleship_variables import *

class Board:
    '''
    This class contains the board and it's necessary elements to start the game.
    '''
    arrow_icon = arrow_icon
    water_icon = water_icon
    boat_icon = boat_icon
    octopus_icon = octopus_icon
    first_coordinate_icon = first_coordinate_icon

    available_boats_list = available_boats_list.copy()

    def __init__(self, player, board=None):
        self.board = board
        self.player = player

        self.board_design()
        self.set_board_elements()


    def board_design(self):
        '''
        This function defines a 10x10 board filled with water
        '''
        if self.board == None:
                    self.board = np.full((10,10), fill_value=self.water_icon)

        self.max_rows_board, self.max_columns_board = self.board.shape


    def set_board_elements(self):
        '''
        This function calls the other functions to set the username, print the board and place the boats.
        '''
        if self.player == 'player':
            self.set_username()
            self.define_print_board()
            self.define_placing_boats_mode_manual()
        elif self.player == 'machine':
            self.define_placing_boats_mode_random()

        if self.placing_boats_mode == "M":    
            while len(self.available_boats_list) > 0:
                self.choose_boat_manual()
                self.define_boat_first_coordinate_manual()
                self.choose_direction_manual()
                self.define_boat_position()
                self.place_boat()
        elif self.placing_boats_mode == "R":
            while len(self.available_boats_list) > 0:
                self.choose_boat_random()
                self.define_boat_first_coordinate_random()
                self.choose_direction_random()
                self.define_boat_position()
                self.place_boat()
            if self.player == 'player':
                self.define_print_board()

        print("\nSuper octopus being placed. If you shoot the octopus, it will shoot to all its edges  \n")
        self.place_octopus_random()
        if self.player == 'player':
            self.define_print_board()


    def set_username(self):
        '''
        This function welcomes the player and, if the player is not the machine, requests a username.
        '''
        if self.player == "player":
            print("\nWelcome to the Battleship game \n")
            sleep(0.7)
            self.username = input("Please enter your username: ")
            sleep(0.7)
            print("\nHello" , self.username , ", this is your board  \n")


    def define_print_board(self):
        '''
        This function prints the board with the username and as a dataframe
        '''
        self.print_board = pd.DataFrame(self.board, columns=list('          '))
        sleep(0.7)
        print(self.username +'\'s board' , self.arrow_icon)
        print(self.print_board, '\n')
        

    def define_placing_boats_mode_manual(self):
        '''
        This function asks if the player wants to place the boats manually or randomly
        '''
        sleep(0.7)
        print("Now you can place your boats \n")
        sleep(0.7)
        print("Would you like to place your boats manually or random? \n")
        sleep(0.7)
        self.placing_boats_mode = input("Enter M for manually or R for random: ")


    def define_placing_boats_mode_random(self):
        '''
        This function sets the placing boats mode as random
        '''
        self.placing_boats_mode = 'R'

    
    def choose_boat_manual(self):
        '''
        This functions allows the user to choose the boats to place manually, and it returns the chosen boat
        It will show all the available boats with their indexes, and let the user enter the index of the boat to place.
        '''
        sleep(0.7)
        print('\n')
        
        for available_boat_index, available_boat in enumerate(self.available_boats_list):
            print(available_boat_index, available_boat)
            sleep(0.05)

        sleep(0.7)
        chosen_boat_index = int(input('\nEnter the number of the boat you want to place: '))
        while 0 > chosen_boat_index or (len(self.available_boats_list)-1) < chosen_boat_index:
            chosen_boat_index = int(input('\nWrong number, enter a valid number: '))

        sleep(0.7)
        self.chosen_boat = self.available_boats_list[chosen_boat_index]
        self.available_boats_list.pop(chosen_boat_index)
        
        print('\nBoat:' , self.chosen_boat, '\n')
        sleep(0.7)
        self.define_print_board()
        sleep(0.7)

    
    def choose_boat_random(self):
        '''
        This function randomly chooses a boat from the list of available boats list, and it returns the chosen boat
        It will show all the available boats with their indexes, and let the user enter the index of the boat to place.
        '''
        if len(self.available_boats_list) == 1:
            self.chosen_boat = self.available_boats_list[0]
            self.available_boats_list.pop(0)
        else: 
            index = random.randint(0,(len(self.available_boats_list)-1))
            self.chosen_boat = self.available_boats_list[index]
            self.available_boats_list.pop(index)


    def define_boat_first_coordinate_manual(self):
        '''
        This function lets the user define the starting coordinates of the chosen boat
        ''' 
        boat_first_coordinate_defined = False

        while boat_first_coordinate_defined == False:

            self.first_coordinate_row = int(input('Enter the number of the starting position row: '))
            while 0 > self.first_coordinate_row or self.first_coordinate_row > self.max_rows_board:
                self.first_coordinate_row = int(input("\nWrong number, enter a number from 0 to 9"))

            self.first_coordinate_column = int(input('\nEnter the number of the starting position column: '))
            while 0 > self.first_coordinate_column or self.first_coordinate_column > self.max_columns_board:
                self.first_coordinate_column = int(input("\nWrong number, enter a number from 0 to 9"))
        
            self.boat_first_coordinate = (self.first_coordinate_row, self.first_coordinate_column)

            if self.board[self.boat_first_coordinate] != self.boat_icon:
                self.board[self.boat_first_coordinate] = self.first_coordinate_icon
                sleep(0.7)
                print("\n")
                self.define_print_board()
                boat_first_coordinate_defined = True

            else:
                print("There is already a boat in this cell, please pick a different one \n")

    
    def define_boat_first_coordinate_random(self):
        '''
        This functions defines randomly the starting position of the boat
        '''
        boat_first_coordinate_defined = False

        while boat_first_coordinate_defined == False:
            self.first_coordinate_row= random.randint(0, (self.max_rows_board - 1))
            while 0 > self.first_coordinate_row or self.first_coordinate_row > (self.max_rows_board - 1):
                self.first_coordinate_row = random.randint(0, (self.max_rows_board - 1))

            self.first_coordinate_column = random.randint(0, (self.max_columns_board - 1))
            while 0 > self.first_coordinate_column or self.first_coordinate_column > (self.max_columns_board - 1):
                self.first_coordinate_column = random.randint(0, (self.max_columns_board - 1))

            self.boat_first_coordinate = (self.first_coordinate_row, self.first_coordinate_column)

            if self.board[self.boat_first_coordinate] != self.boat_icon:
                boat_first_coordinate_defined = True


    def choose_direction_manual(self):
        '''
        This function lets the user define the direction of the boat
        '''
        self.first_coordinate_row = int(self.first_coordinate_row)
        self.first_coordinate_column = int(self.first_coordinate_column)

        self.lenght_chosen_boat = len(str(self.chosen_boat))

        self.boat_direction = input("Choose the direction of your boat: N, S, E or W: ")


    def choose_direction_random(self):
        '''
        This function defines randomly the direction of the boat
        '''
        direction_list = ["N", "S", "E", "W"]

        self.first_coordinate_row = int(self.first_coordinate_row)
        self.first_coordinate_column = int(self.first_coordinate_column)

        self.lenght_chosen_boat = len(str(self.chosen_boat))
        if (self.max_columns_board - self.first_coordinate_column) < self.lenght_chosen_boat:
            if (self.max_rows_board - self.first_coordinate_row) < self.lenght_chosen_boat:
                direction_list.remove("S")
                direction_list.remove("E")
                self.boat_direction = random.choice(direction_list)

            elif self.first_coordinate_row < self.lenght_chosen_boat: 
                direction_list.remove("N")
                direction_list.remove("E")
                self.boat_direction = random.choice(direction_list)

            else:
                direction_list.remove("E")
                self.boat_direction = random.choice(direction_list)
    
        elif self.first_coordinate_column < self.lenght_chosen_boat:
            if self.first_coordinate_column < self.lenght_chosen_boat:
                direction_list.remove("N")
                direction_list.remove("W")
                self.boat_direction = random.choice(direction_list)

            elif (self.max_rows_board - self.first_coordinate_row) < self.lenght_chosen_boat:
                direction_list.remove("S")
                direction_list.remove("E")
                self.boat_direction = random.choice(direction_list)
                
            else: 
                direction_list.remove("W")
                self.boat_direction = random.choice(direction_list)

        elif (self.max_rows_board - self.first_coordinate_row) < self.lenght_chosen_boat: 
            direction_list.remove("S")
            self.boat_direction = random.choice(direction_list)

        elif self.first_coordinate_row < self.lenght_chosen_boat: 
            direction_list.remove("N")
            self.boat_direction = random.choice(direction_list)

        else:
            self.boat_direction = random.choice(direction_list)


    def define_boat_position(self):
        '''
        This function defines the whole position of the boat
        '''
        self.boat_first_coordinate = [(self.boat_first_coordinate)]

        while len(self.boat_first_coordinate) < self.lenght_chosen_boat:

            if self.boat_direction == "N":
                self.first_coordinate_row = self.first_coordinate_row - 1 

            elif self.boat_direction == "S":
                self.first_coordinate_row = self.first_coordinate_row + 1

            elif self.boat_direction == "E":
                self.first_coordinate_column = self. first_coordinate_column + 1

            elif self.boat_direction == "W":
                self.first_coordinate_column = self.first_coordinate_column - 1

            self.boat_first_coordinate.append((self.first_coordinate_row, self.first_coordinate_column))


    def place_boat(self):
        '''
        This functions checks if there's another boat crossing the new position and places the boat if there is not
        '''
        boat_positions_list = []

        for coordinate in self.boat_first_coordinate:

            if coordinate in boat_positions_list:
                self.boat_first_coordinate.pop[0]

        if len(self.boat_first_coordinate) == self.lenght_chosen_boat:
            boat_positions_list.append(self.boat_first_coordinate)

            for coordinate in self.boat_first_coordinate:
                self.board[coordinate] = self.boat_icon
            if self.placing_boats_mode == "M":
                self.define_print_board()

        else:
            if self.placing_boats_mode == "M":
                print("There is already a bot in this position, please choose a different one")


    def place_octopus_random(self):
        '''
        This function places the octopus in a random position on the board
        If in the chosen position there is a boat, it will choose another random one
        '''
        self.octopus_positioned = False
        while self.octopus_positioned == False:
            octopus_column = random.randint(0, 9)
            octopus_row = random.randint(0, 9)
            octopus_position = (octopus_row, octopus_column)
            if self.board[octopus_position] != boat_icon:
                self.board[octopus_position] = self.octopus_icon
                self.octopus_positioned = True
