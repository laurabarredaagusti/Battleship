from battleship_classes import *
from battleship_variables import *
from battleship_game_state import *

empty_game()

Board("player")
Board ("player_empty")
Board("machine")
Board("machine_empty")

print("Now the real game starts  \n")
sleep(0.7)

player_shoot = Shoot('player', 'machine', 'machine_empty')
machine_shoot = Shoot('machine', 'player', 'player_empty')

while True:
    player_shoot.action_shoot()
    machine_shoot.action_shoot()
#     # shooting_user(board_machine, board_shooting_user)
#     # if "\U000026F5" not in board_machine:
#     #     print("\nUser wins  \n")
#     #     break
#     # print("\nMachine's turn  \n")
#     # shooting_random(board_user, board_shooting_machine)
#     # if "\U000026F5" not in board_user:
#     #     print("Machine wins  \n")
#     #     break