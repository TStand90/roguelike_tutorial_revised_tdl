import json

import jsonpickle

from map_utils import GameMap


def save_game(player, entities, game_map, message_log, game_state):
    data = {
        'player_index': jsonpickle.encode(entities.index(player)),
        'entities': jsonpickle.encode(entities),
        'game_map': jsonpickle.encode(game_map),
        'message_log': jsonpickle.encode(message_log),
        'game_state': jsonpickle.encode(game_state)
    }

    walkable_list = []
    transparent_list = []

    for y in range(game_map.height):
        walkable_list_row = []
        transparent_list_row = []

        for x in range(game_map.width):
            walkable_list_row.append(game_map.walkable[x, y])
            transparent_list_row.append(game_map.transparent[x, y])

        walkable_list.append(walkable_list_row)
        transparent_list.append(transparent_list_row)

    data['walkable'] = walkable_list
    data['transparent'] = transparent_list

    with open('savegame.json', 'w') as save_file:
        json.dump(data, save_file, indent=4)


def load_game():
    with open('savegame.json', 'r') as save_file:
        data = json.load(save_file)

    player_index = jsonpickle.decode(data['player_index'])
    entities = jsonpickle.decode(data['entities'])
    game_map = jsonpickle.decode(data['game_map'])
    message_log = jsonpickle.decode(data['message_log'])
    game_state = jsonpickle.decode(data['game_state'])

    walkable = data['walkable']
    transparent = data['transparent']

    player = entities[player_index]

    new_game_map = GameMap(game_map.width, game_map.height)
    new_game_map.explored = game_map.explored

    for y in range(new_game_map.height):
        for x in range(new_game_map.width):
            new_game_map.walkable[x, y] = walkable[y][x]
            new_game_map.transparent[x, y] = transparent[y][x]

    return player, entities, new_game_map, message_log, game_state
