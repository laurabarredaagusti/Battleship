import json
from battleship_classes import *
from battleship_variables import *
from battleship_game_state import *

empty_game_state()

Board("player")
Board("machine")
Board("machine_empty")

print("Now the real game starts  \n")
sleep(0.7)

player_shoot = Shoot('player', 'machine', 'machine_empty')
machine_shoot = Shoot('machine', 'player', 'player_empty')

while True:

    with open(json_file, 'rb') as fp:
            game_state = pickle.load(fp)

    machine_board = game_state['machine_board']
    player_board = game_state['player_board']
    username = game_state['username']

    player_shoot.action_shoot()
    if boat_icon not in machine_board:
        print(username, ' WON')
        break

    machine_shoot.action_shoot()
    if boat_icon not in player_board:
        print('MACHINE WON')
        break