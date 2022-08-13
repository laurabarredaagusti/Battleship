import pickle

with open('game_state.json', 'rb') as fp:
    game_state = pickle.load(fp)

print(game_state)