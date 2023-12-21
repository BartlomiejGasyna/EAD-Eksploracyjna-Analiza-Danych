import pandas as pd
import requests
import sqlite3
import re
file_path = 'pokedex_history.hdf5'

df_pokedex = pd.read_hdf(file_path)


# Initialize a DataFrame for Pokemon data
df_pokemon = pd.DataFrame(columns=['pokemon', 'hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed'])

base_url = 'https://pokeapi.co/api/v2/pokemon/'


# Get stats for each Pokemon that was already caught

for pokemon_name in df_pokedex['name']:
    pokemon_name = pokemon_name.lower()
    response = requests.get(base_url + pokemon_name)
    if response.status_code == 200:
        pokemon_response = response.json()

        hp              = pokemon_response['stats'][0]['base_stat']
        attack          = pokemon_response['stats'][1]['base_stat']
        defense         = pokemon_response['stats'][2]['base_stat']
        special_attack  = pokemon_response['stats'][3]['base_stat']
        special_defense = pokemon_response['stats'][4]['base_stat']
        speed           = pokemon_response['stats'][5]['base_stat']

        type_1          = pokemon_response['types'][0]['type']['name']
        
        if len(pokemon_response['types']) > 1:
            type_2      = pokemon_response['types'][1]['type']['name']
        else:
            type_2 = None

        new_pokemon_data = pd.DataFrame(data={'pokemon':        [pokemon_name], 
                                            'hp':               [hp], 
                                            'attack':           [attack], 
                                            'defense':          [defense], 
                                            'special_attack':   [special_attack], 
                                            'special_defense':  [special_defense], 
                                            'speed':            [speed],
                                            'type_1':           [type_1],
                                            'type_2':           [type_2]})

        df_pokemon = pd.concat([df_pokemon, new_pokemon_data], ignore_index=True)

# print(df_pokemon.head())

def attack_against(attacker: str, attacked: str, database: pd.DataFrame):
    pd_attacker = database.loc[database['pokemon'] == attacker.lower()].copy()
    pd_attacked = database.loc[database['pokemon'] == attacked.lower()].copy()


    if pd_attacker.loc[:, pd_attacker.columns != 'type_2'].isnull().any().any():
        print('Not enough data about attacker pokemon!')
        return None
    
    if pd_attacked.loc[:, pd_attacked.columns != 'type_2'].isnull().any().any():
        print('Not enough data about attacked pokemon!')
        return None

    conn = sqlite3.connect("pokemon_against.sqlite")  # connection to file-based database
    cursor = conn.cursor()
    pattern = re.compile(r'against_') # fetch only columns with "against_" prefix
    cursor.execute("PRAGMA table_info(against_stats)")
    columns = cursor.fetchall()
    col_name = [column[1] for column in columns if pattern.match(column[1])]

    # fetch against stats for attacker
    query = f'SELECT {", ".join(col_name)} FROM against_stats WHERE name = "{attacker.capitalize()}"'
    against_stats = conn.execute(query)
    for against_stats in conn.execute(query):
        continue
    conn.close()

    # calculate multipliers against types
    idx = [i for i, element in enumerate(col_name) if pd_attacked['type_1'].values[0] in element][0]
    against_type_1 = against_stats[idx]

    if pd_attacked['type_2'].values[0] is not None:
        idx = [i for i, element in enumerate(col_name) if pd_attacked['type_2'].values[0] in element][0]
        against_type_2 = against_stats[idx]
    else:
        against_type_2 = 1

    
    # calculate points
    attacker_points = pd_attacker['attack'].astype(float).values[0]
    attacker_points += ( pd_attacker['special_attack'].astype(float).values[0] * 1.5 )
    attacker_points *= against_type_1
    attacker_points *= against_type_2
    attacker_points *= pd_attacked['defense'].astype(float).values[0] / 100
    attacker_points *= pd_attacked['special_defense'].astype(float).values[0] / 75
    attacker_points *= (pd_attacked['speed'].astype(float).values[0] / 100) + 0.25

    if attacker_points > pd_attacked['hp'].astype(float).values[0]:
        print('Pokemon defeated!')
    else:
        print('Pokemon survived!')

    return attacker_points



attacker = 'yanma'
attacked = 'comfey'
points = attack_against(attacker, attacked, df_pokemon)

print(f'{attacker.capitalize()} attacked {attacked.capitalize()} with {points} points!')