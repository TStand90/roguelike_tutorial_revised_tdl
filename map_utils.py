def make_map(game_map):
    for x, y in game_map:
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True

    game_map.walkable[30, 22] = False
    game_map.transparent[30, 22] = False
    game_map.walkable[31, 22] = False
    game_map.transparent[31, 22] = False
    game_map.walkable[32, 22] = False
    game_map.transparent[32, 22] = False
