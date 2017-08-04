import math

from components.fighter import Fighter
from components.ai import BasicMonster, ConfusedMonster
from components.item import Item
from components.inventory import Inventory

from render_functions import RenderOrder


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None, inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        path = game_map.compute_path(self.x, self.y, target_x, target_y)

        if path:
            dx = path[0][0] - self.x
            dy = path[0][1] - self.y

            if game_map.walkable[path[0][0], path[0][1]] and not get_blocking_entities_at_location(entities, self.x + dx,
                                                                                                   self.y + dy):
                self.move(dx, dy)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def to_json(self):
        if self.fighter:
            fighter_data = self.fighter.to_json()
        else:
            fighter_data = None

        if self.ai:
            ai_data = self.ai.to_json()
        else:
            ai_data = None

        if self.item:
            item_data = self.item.to_json()
        else:
            item_data = None

        if self.inventory:
            inventory_data = self.inventory.to_json()
        else:
            inventory_data = None

        json_data = {
            'x': self.x,
            'y': self.y,
            'char': self.char,
            'color': self.color,
            'name': self.name,
            'blocks': self.blocks,
            'render_order': self.render_order.value,
            'fighter': fighter_data,
            'ai': ai_data,
            'item': item_data,
            'inventory': inventory_data
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        x = json_data.get('x')
        y = json_data.get('y')
        char = json_data.get('char')
        color = json_data.get('color')
        name = json_data.get('name')
        blocks = json_data.get('blocks', False)
        render_order = RenderOrder(json_data.get('render_order'))
        fighter_json = json_data.get('fighter')
        ai_json = json_data.get('ai')
        item_json = json_data.get('item')
        inventory_json = json_data.get('inventory')

        entity = Entity(x, y, char, color, name, blocks, render_order)

        if fighter_json:
            entity.fighter = Fighter.from_json(fighter_json)
            entity.fighter.owner = entity

        if ai_json:
            name = ai_json.get('name')

            if name == BasicMonster.__name__:
                ai = BasicMonster.from_json()
            elif name == ConfusedMonster.__name__:
                ai = ConfusedMonster.from_json(ai_json, entity)
            else:
                ai = None

            if ai:
                entity.ai = ai
                entity.ai.owner = entity

        if item_json:
            entity.item = Item.from_json(item_json)
            entity.item.owner = entity

        if inventory_json:
            entity.inventory = Inventory.from_json(inventory_json)
            entity.inventory.owner = entity

        return entity


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
