import pickle


def empty_game_state():

    json_file = 'game_state.json'

    with open(json_file, 'rb') as fp:
        game_state = pickle.load(fp)

    game_state = {
                'username' : None,
                'max_rows_board' : None,
                'max_columns_board' : None,
                'player_board' : None,
                'machine_board' : None,
                'player_empty_board' : None,
                'machine_empty_board' : None
                }
                
    with open('game_state.json', 'wb') as fp:
        pickle.dump(game_state, fp)

game_state = {
            'username' : None,
            'max_rows_board' : None,
            'max_columns_board' : None,
            'player_board' : None,
            'machine_board' : None,
            'player_empty_board' : None,
            'machine_empty_board' : None
            }
            
with open('game_state.json', 'wb') as fp:
    pickle.dump(game_state, fp)


    
