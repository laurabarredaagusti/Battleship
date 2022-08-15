import numpy as np
import random
import pygame
import pandas as pd
from time import sleep
import pickle

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
    main_available_boats_list = main_available_boats_list.copy()
    json_file = json_file

    with open(json_file, 'rb') as fp:
        game_state = pickle.load(fp)


    def __init__(self, player, board=None):
        self.board = board
        self.player = player
        self.game_state = {}
        self.board_design()
        self.set_board_elements()
        self.key_names_board()
        self.create_empty_player_board()
        self.update_json_file()


    def board_design(self):
        '''
        This function defines a 10x10 board filled with water
        '''
        if self.board == None:
                    self.board = np.full((10,10), fill_value=self.water_icon)

        self.max_rows_board, self.max_columns_board = self.board.shape
        self.game_state['max_rows_board'] = self.max_rows_board      
        self.game_state['max_columns_board'] = self.max_columns_board   


    def set_board_elements(self):
        '''
        This function calls the other functions to set the username, print the board and place the boats.
        '''
        if self.player == 'player':
            self.set_username()
            self.define_print_board()
            self.define_placing_boats_mode()
        elif self.player == 'machine':
            self.placing_boats_mode = "R"

        self.available_boats_list = self.main_available_boats_list.copy()

        if self.player == 'player' or self.player == 'machine':
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
                    sleep(0.7)
                    print('\nPlacing boats\n')
                    sleep(0.7)
                    self.define_print_board()

            if self.player == 'player':
                print("\nSuper octopus being placed. If you shoot the octopus, it will shoot to all its edges  \n")
                self.place_octopus_random()
                sleep(0.7)
                self.define_print_board()
            elif self.player == 'machine':
                self.place_octopus_random()


    def set_username(self):
        '''
        This function welcomes the player and, if the player is not the machine, requests a username.
        '''
        if self.player == "player":
            print("\nWelcome to the Battleship game \n")
            sleep(0.7)
            self.username = input("Please enter your username: ")
            self.game_state['username'] = self.username
            sleep(0.7)
            print("\nHello" , self.username , ", this is your board  \n")
            sleep(0.3)


    def define_print_board(self):
        '''
        This function prints the board with the username and as a dataframe
        '''
        self.print_board = pd.DataFrame(self.board, columns=list('          '))
        sleep(0.7)
        print(self.username +'\'s board' , self.arrow_icon)
        print(self.print_board, '\n')
        

    def define_placing_boats_mode(self):
        '''
        This function asks if the player wants to place the boats manually or randomly
        '''
        sleep(0.7)
        print("Now you can place your boats \n")
        sleep(0.7)
        print("Would you like to place your boats manually or random? \n")
        sleep(0.7)
        self.placing_boats_mode = input("Enter M for manually or R for random: ").upper()
        while self.placing_boats_mode != 'M' and self.placing_boats_mode != 'R':
            self.placing_boats_mode = input("\nThat was not a valid input. Enter M for manually or R for random: ").upper()

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
        chosen_boat_index = None
        while chosen_boat_index == None:
            try:
                chosen_boat_index = int(input('\nEnter the number of the boat you want to place: '))
            except: 
                print('This was not a valid character, please try again')

        while 0 > chosen_boat_index or (len(self.available_boats_list)-1) < chosen_boat_index:
            chosen_boat_index = int(input('\nWrong number, enter a boat number: '))

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
        self.first_coordinate_row = None
        self.first_coordinate_column = None

        while boat_first_coordinate_defined == False:
            while self.first_coordinate_row == None:
                try:
                    self.first_coordinate_row = int(input('Enter the number of the starting position row: '))
                except:
                    print('Please enter a valid character')
    
            while 0 > self.first_coordinate_row or self.first_coordinate_row > (self.max_rows_board - 1):
                self.first_coordinate_row = int(input("\nWrong number, enter the number of an existing row: "))

            while self.first_coordinate_column == None:
                try:
                    self.first_coordinate_column = int(input('\nEnter the number of the starting position column: '))
                except:
                    print('Please enter a valid character')

            while 0 > self.first_coordinate_column or self.first_coordinate_column > (self.max_columns_board - 1):
                self.first_coordinate_column = int(input("\nWrong number, enter the number of an existing column: "))
        
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
            self.first_coordinate_row = random.randint(0, (self.max_rows_board - 1))
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

        self.boat_direction = input("Choose the direction of your boat: N, S, E or W: ").upper()
        while self.boat_direction != 'N' and self.boat_direction != 'S' and self.boat_direction != 'E' and self.boat_direction != 'W':
            self.boat_direction = input("Please enter a valid direction: N, S, E or W: ").upper()


    def choose_direction_random(self):
        '''
        This function defines randomly the direction of the boat
        '''
        direction_list = ["N", "S", "E", "W"]

        self.first_coordinate_row = int(self.first_coordinate_row)
        self.first_coordinate_column = int(self.first_coordinate_column)
        self.lenght_chosen_boat = len(str(self.chosen_boat))
        self.boat_direction = random.choice(direction_list)


    def define_boat_position(self):
        '''
        This function defines the whole position of the boat
        '''
        self.boat_coordinates = [(self.boat_first_coordinate)]
        coordinates_row = self.first_coordinate_row
        coordinates_column = self.first_coordinate_column

        while len(self.boat_coordinates) < self.lenght_chosen_boat:

            if self.boat_direction == "N":
                coordinates_row = coordinates_row - 1 

            elif self.boat_direction == "S":
                coordinates_row = coordinates_row + 1

            elif self.boat_direction == "E":
                coordinates_column = coordinates_column + 1

            elif self.boat_direction == "W":
                coordinates_column = coordinates_column - 1

            self.boat_coordinates.append((coordinates_row, coordinates_column))


    def place_boat(self):
        '''
        This functions checks if there's another boat crossing the new position and places the boat if there is not
        '''
        try:
            boat_positions_list = []

            for coordinate in self.boat_coordinates:

                if coordinate in boat_positions_list:
                    self.boat_coordinates.pop[0]

            if len(self.boat_coordinates) == self.lenght_chosen_boat:
                boat_positions_list.append(self.boat_coordinates)

                for coordinate in self.boat_coordinates:
                    self.board[coordinate] = self.boat_icon
                if self.placing_boats_mode == "M":
                    self.define_print_board()

            else:
                if self.placing_boats_mode == "M":
                    print("There is already a bot in this position, please choose a different one")
        except:
            if self.player == 'player' and self.placing_boats_mode == 'M':
                print('You can\'t place a boat in this direction, please choose a different one')
                self.choose_direction_manual()
                self.define_boat_position()
                self.place_boat()

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


    def key_names_board(self):
        key_name = self.player + '_board'
        self.game_state[key_name] = self.board

    
    def create_empty_player_board(self):
        if self.player == 'player':
            self.game_state['player_empty_board'] = self.game_state['player_board']


    def update_json_file(self):
        with open(self.json_file, 'rb') as fp:
            game_state_main = pickle.load(fp)
        game_state_main.update(self.game_state)
        with open('game_state.json', 'wb') as fp:
            pickle.dump(game_state_main, fp)


class Shoot:
    '''
    This class contains all the necessary functions to choose
    '''
    water_icon = water_icon
    boat_icon = boat_icon
    octopus_icon = octopus_icon
    arrow_icon = arrow_icon
    touched_icon = touched_icon
    shoot_water_icon = shoot_water_icon
    shoot_octopus_icon = shoot_octopus_icon
    target_icon = first_coordinate_icon
    json_file = json_file

    with open(json_file, 'rb') as fp:
        game_state = pickle.load(fp)

    pygame.init()
    pygame.mixer.init()

    def __init__(self, player, target, empty_target):

        key_target_board = target + '_board'
        key_empty_target_board = empty_target + '_board'

        self.player = player
        self.target_board = self.game_state[key_target_board]
        self.empty_target_board = self.game_state[key_empty_target_board]

        if player == 'player':
            self.define_shooting_mode()
        elif player == 'machine':
            self.shooting_mode = 'R'

    def play_boat_sound(self):
        '''
        This function plays the sound for a boat shoot
        '''
        pygame.mixer.Sound.play(pygame.mixer.Sound("../sound/boat_sound.wav"))


    def play_water_sound(self):
        '''
        This function plays the sound for a water shoot
        '''
        pygame.mixer.Sound.play(pygame.mixer.Sound("../sound/water_sound.wav"))
        

    def play_octopus_sound(self):
        '''
        This functions plays the sound for an octopus shoot
        '''
        pygame.mixer.Sound.play(pygame.mixer.Sound("../sound/octopus_sound.wav"))


    def define_shooting_mode(self):
        '''
        This function let's the player decide if he wants to choose his shooting targets or he wants random targets
        '''
        print("Would you like to choose your target or do you want a random target? \n")
        sleep(0.7)
        self.shooting_mode = input("Enter M for manual or R for random: ").upper()
        print('\n')
        while self.shooting_mode != 'M' and self.shooting_mode != 'R':
            self.shooting_mode = input("That was not a valid input. Enter M for manually or R for random: ").upper()


    def set_username(self):
        if self.player == 'machine':
            self.username = self.game_state['username']
        elif self.player == 'player':
            self.username = 'Machine'


    def define_print_target_board(self):
        '''
        This functions prints the target's board
        '''
        sleep(0.7)
        self.print_target_board = pd.DataFrame(self.target_board, columns=list('          '))
        sleep(0.7)
        print('\n', self.username, '\'s board' , self.arrow_icon)
        print(self.print_target_board, '\n')

    
    def define_shooting_target_random(self):
        '''
        This function randomly chooses the target coordinates
        '''
        self.target_row = random.randint(0, 9)
        self.target_column = random.randint(0, 9)
        self.target = (self.target_row, self.target_column)
        self.target_octopus = [(self.target)]


    def define_shooting_target_manual(self):
        '''
        This function let's the user set manual target coordinates
        '''
        self.target = False
        self.target_row = False
        self.target_column = False

        while self.target == False:
            while self.target_row == None:
                try:
                    self.target_row = int(input('Enter the number of the target row: '))
                except:
                    print('Please enter a valid character')
    
            while 0 > self.target_row or self.target_row > (self.game_state['max_rows_board'] - 1):
                self.target_row = int(input("\nWrong number, enter the number of an existing row: "))

            while self.target_column == None:
                try:
                    self.target_column = int(input('\nEnter the number of the starting position column: '))
                except:
                    print('Please enter a valid character')

            while 0 > self.target_column or self.target_column > (self.game_state['max_columns_board'] - 1):
                self.target_column = int(input("\nWrong number, enter the number of an existing column: "))
        
            self.target = (self.target_row, self.target_column)

    
    # def icon_target_changed(self):
    #     # self.empty_target_board[self.target] = self.target_icon
    #     print('This is my empty target board')
    #     print(self.empty_target_board)
    #     print('This is my regular board')
    #     print(self.target_board)
    #     sleep(5)
    #     self.target_board[self.target] = self.target_icon
    #     print('This is my empty target board')
    #     print(self.empty_target_board)
    #     print('This is my regular board')
    #     print(self.target_board)
    #     sleep(5)


    def result_shoot_touched(self):
        '''
        Función que activa el sonido del disparo y cambia el icono a 'tocado'
        '''
        print("Touched")
        self.target_board[self.target] = self.touched_icon
        self.empty_target_board[self.target] = self.touched_icon

    
    def result_shoot_water(self):
        '''
        Función que activa el sonido del agua y cambia el icono a 'agua'
        ''' 
        print("Water")
        self.target_board[self.target] = self.shoot_water_icon
        self.empty_target_board[self.target] = self.shoot_water_icon


    def result_shoot_octopus(self):
        '''
        Funución que activa el sonido del pulpo y cambia el icono a pulpo disparado
        '''
        print("Octopus")
        self.target_row = self.target_row - 1
        self.target_octopus.append((self.target_row, self.target_column))
        self.target_column = self.target_column - 1
        self.target_octopus.append((self.target_row, self.target_column))
        self.target_row = self.target_row + 1
        self.target_octopus.append((self.target_row, self.target_column))
        self.target_row = self.target_row + 1
        self.target_octopus.append((self.target_row, self.target_column))
        self.target_column = self.target_column + 1
        self.target_octopus.append((self.target_row, self.target_column))
        self.target_column = self.target_column + 1
        self.target_octopus.append((self.target_row, self.target_column))
        self.target_row = self.target_row - 1
        self.target_octopus.append((self.target_row, self.target_column))
        self.target_row = self.target_row - 1
        self.target_octopus.append((self.target_row, self.target_column))
        
        for elem in self.target_octopus:
            try:
                self.target_board[elem] = shoot_octopus_icon
                self.empty_target_board[elem] = shoot_octopus_icon
            except:
                continue


    def action_shoot(self):
        '''
        Función que realiza disparos hasta que el target es agua
        '''
        sleep(0.7)
        if self.player == 'player':
            print("Your turn")
        elif self.player == 'machine':
            print('Machine\'s turn')
        sleep(0.7)
        self.set_username()
        self.define_print_target_board()

        if self.shooting_mode == 'R':
            self.define_shooting_target_random()
        else:
            self.define_shooting_target_manual()

        sleep(0.7)
        # self.icon_target_changed()
        # self.define_print_target_board()
        print(self.target_board[self.target])
        print('estoy aqui')
        self.result_shoot()
        self.update_json_file()

    
    def result_shoot(self):

        while self.target_board[self.target] != self.shoot_water_icon:
            print('Shooting\n')
            sleep(0.7)
            print(self.target_board[self.target])
            if self.target_board[self.target] != self.touched_icon and self.target_board[self.target] != self.shoot_water_icon:
                print('no he disparado aqui')
                if self.target_board[self.target] == self.boat_icon:
                    self.result_shoot_touched()
                    # self.play_boat_sound()
                    self.define_print_target_board()
                    sleep(0.7)
                    print('There is another turn\n')

                elif self.target_board[self.target] == self.octopus_icon:
                    self.result_shoot_octopus()
                    # self.play_octopus_sound()
                    self.define_print_target_board()
                    sleep(0.7)
                    print('There is another turn\n')
                
                else:
                    self.result_shoot_water()
                    # self.play_water_sound()
                    self.define_print_target_board()
            else:
                print('he disparado aqui')
                if self.shooting_mode == 'R':
                    self.define_shooting_target_random()
                    print('voy a volver a disparar')
                    self.result_shoot()
                else:
                    print("You have already shoot to this position, please choose your cell again, \n")
                    self.define_shooting_target_manual()
                    self.result_shoot()


    def update_json_file(self):
        with open(self.json_file, 'rb') as fp:
            game_state_main = pickle.load(fp)
        game_state_main.update(self.game_state)
        with open('game_state.json', 'wb') as fp:
            pickle.dump(game_state_main, fp)

