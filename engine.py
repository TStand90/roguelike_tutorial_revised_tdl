import tdl

from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from game_states import GameStates
from input_handlers import handle_keys
from map_utils import GameMap, make_map
from render_functions import clear_all, render_all, RenderOrder


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 'BASIC'
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3

    colors = {
        'dark_wall': (0, 0, 100),
        'dark_ground': (50, 50, 150),
        'light_wall': (130, 110, 50),
        'light_ground': (200, 180, 50),
        'desaturated_green': (63, 127, 63),
        'darker_green': (0, 127, 0),
        'dark_red': (191, 0, 0)
    }

    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', (255, 255, 255), 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component)
    entities = [player]

    tdl.set_font('arial10x10.png', greyscale=True, altLayout=True)

    root_console = tdl.init(screen_width, screen_height, title='Roguelike Tutorial Revised')
    con = tdl.Console(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities,
             max_monsters_per_room, colors)

    fov_recompute = True

    game_state = GameStates.PLAYERS_TURN

    while not tdl.event.is_window_closed():
        if fov_recompute:
            game_map.compute_fov(player.x, player.y, fov=fov_algorithm, radius=fov_radius, light_walls=fov_light_walls)

        render_all(con, entities, player, game_map, fov_recompute, root_console, screen_width, screen_height, colors)
        tdl.flush()

        clear_all(con, entities)

        fov_recompute = False

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None

        if not user_input:
            continue

        action = handle_keys(user_input)

        move = action.get('move')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if game_map.walkable[destination_x, destination_y]:
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                print(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity, colors)
                else:
                    message = kill_monster(dead_entity, colors)

                print(message)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            print(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity, colors)
                            else:
                                message = kill_monster(dead_entity, colors)

                            print(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
