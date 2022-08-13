from battleship_classes import *
from battleship_variables import *

board_user = Board("player")
board_user_empty = Board ("player_empty")
board_machine = Board("machine")
board_machine_empty = Board("machine_empty")

print("Now the real game starts  \n")
sleep(0.7)

player_shoot = Shoot('player', board_user, board_machine_empty)
machine_shoot = Shoot('machine', board_machine, board_machine_empty)


while True:
    player_shoot.action_shoot()
    print('Im here')
    # shooting_user(board_machine, board_shooting_user)
    # if "\U000026F5" not in board_machine:
    #     print("\nUser wins  \n")
    #     break
    # print("\nMachine's turn  \n")
    # shooting_random(board_user, board_shooting_machine)
    # if "\U000026F5" not in board_user:
    #     print("Machine wins  \n")
    #     break