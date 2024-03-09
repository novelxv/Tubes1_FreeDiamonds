from typing import Tuple
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, position_equals
import math

class Novel(BaseLogic):
    def __init__(self):
        # Initialize attributes necessary
        pass

    def distance(self, bot_position: Position, goal: Position):
        distance = abs(goal.x - bot_position.x) + abs(goal.y - bot_position.y)
        return distance
    
    def get_direction(self, bot_position: Position, goal: Position):
        return get_direction(bot_position.x, bot_position.y, goal.x, goal.y)
    
    def get_nearest_blue(self, bot_position: Position, list_diamonds: list):
        shortest_distance = float('inf')
        nearest_blue = None

        for diamond in list_diamonds:
            distance = self.distance(bot_position, diamond.position)
            if diamond.properties.points == 1 and distance < shortest_distance:
                shortest_distance = distance
                nearest_blue = diamond

        return nearest_blue

    def highest_density(self, bot_position: Position, list_diamonds: list, prefer_low_value=False):
        highest_density = 0
        highest_density_position = None

        if prefer_low_value:
            self.get_nearest_blue(bot_position, list_diamonds)
        else:    
            for diamond in list_diamonds:
                distance = self.distance(bot_position, diamond.position)
                point = diamond.properties.points
                if distance != 0:
                    density = point / distance
                    if density > highest_density:
                        highest_density = density
                        highest_density_position = diamond
                    elif density == highest_density and point > highest_density_position.properties.points:
                        highest_density_position = diamond
        return highest_density_position

    def find_nearest_diamond(self, bot_position: Position, list_diamonds: list, prefer_low_value=False):
        # Cari diamond terdekat
        shortest_distance = float('inf')
        nearest_diamond = None

        for diamond in list_diamonds:
            distance = self.distance(bot_position, diamond.position)
            # Jika prefer_low_value True, cari diamond dengan poin 1
            if prefer_low_value and diamond.properties.points != 1:
                continue
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_diamond = diamond
            elif distance == shortest_distance and diamond.properties.points > nearest_diamond.properties.points:
                nearest_diamond = diamond

        return nearest_diamond

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        inventory_size = board_bot.properties.inventory_size if board_bot.properties.inventory_size else 0
        bot_position = board_bot.position
        list_diamonds = board.diamonds
        collected = board_bot.properties.diamonds if board_bot.properties.diamonds else 0
        milliseconds_left = board_bot.properties.milliseconds_left if board_bot.properties.milliseconds_left else 0
        seconds_left = milliseconds_left / 1000

        base_position = board_bot.properties.base
        distance_to_base = self.distance(bot_position, base_position)

        # Jika waktu tersisa dalam detik sama dengan jarak ke base, kembali ke base
        if math.floor(seconds_left) == distance_to_base or math.floor(seconds_left) == distance_to_base + 1:
            direction_to_base = get_direction(bot_position.x, bot_position.y, base_position.x, base_position.y)
            return direction_to_base

        # Jika inventory hampir penuh, ubah strategi untuk mengumpulkan diamond poin 1
        prefer_low_value_diamond = collected == inventory_size - 1

        get_diamond = self.highest_density(bot_position, list_diamonds, prefer_low_value_diamond)

        if get_diamond and collected < inventory_size:
            direction_to_diamond = self.get_direction(bot_position, get_diamond.position)
            # jika 0, 0
            if direction_to_diamond == (0, 0):
                return 1, 0
            return direction_to_diamond
        else:
            # Kembali ke base jika inventory penuh atau tidak ada diamond terdekat
            if base_position:
                direction_to_base = self.get_direction(bot_position, base_position)
                # jika 0, 0
                if direction_to_base == (0, 0):
                    return 1, 0
                return direction_to_base
            else:
                # Gerakan default jika tidak ada instruksi lain
                return 1, 0
            
# def is_red_button_position(self, current_position: Position, board: Board):
#     red_buttons = [i for i in board.game_objects if i.type == "RedButtonGameObject"]
#     for red_button in red_buttons:
#         if position_equals(red_button.position, current_position):
#             return True
#     return False

# def is_teleporter_position(self, current_position: Position, board: Board):
#     teleporters = [i for i in board.game_objects if i.type == "TeleportGameObject"]
#     for teleporter in teleporters:
#         if position_equals(teleporter.position, current_position):
#             return True
#     return False

# def get_first_teleporter_position(self, board: Board):
#     teleporters = [i for i in board.game_objects if i.type == "TeleportGameObject"]
#     return teleporters[0].position

# def get_second_teleporter_position(self, board: Board):
#     teleporters = [i for i in board.game_objects if i.type == "TeleportGameObject"]
#     return teleporters[1].position

# def to_avoid(self, board: Board):
#     # fungsi ini digunakan untuk menentukan posisi yang harus dihindari oleh bot
#     # misalnya, posisi teleporter, red button, atau bot lain
#     teleporters = [i for i in board.game_objects if i.type == "TeleportGameObject"]
#     red_buttons = [i for i in board.game_objects if i.type == "RedButtonGameObject"]
#     bots = [i for i in board.game_objects if i.type == "BotGameObject"]
#     avoid = []
#     for teleporter in teleporters:
#         avoid.append(teleporter.position)
#     for red_button in red_buttons:
#         avoid.append(red_button.position)
#     for bot in bots:
#         avoid.append(bot.position)
#     return avoid
