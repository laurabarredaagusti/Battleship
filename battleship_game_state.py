import pickle

game_state = {
            'username' : None
            }
            
with open('game_state.json', 'wb') as fp:
    pickle.dump(game_state, fp)

    
