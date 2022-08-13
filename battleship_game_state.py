import pickle

game_state = {
            'username' : None,
            'max_rows_board' : None,
            'max_columns_board' : None
            }
            
with open('game_state.json', 'wb') as fp:
    pickle.dump(game_state, fp)

    
