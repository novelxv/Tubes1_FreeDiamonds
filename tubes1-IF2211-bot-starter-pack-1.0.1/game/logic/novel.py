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
    
    def teleporter_distance(self, bot_position: Position, target_position: Position, teleporters: list):
        if len(teleporters) < 2:
            return float('inf'), None  # Return infinite distance jika jumlah teleporter < 2

        teleporter_positions = [teleporter.position for teleporter in teleporters]
        teleporter1, teleporter2 = teleporter_positions

        # Distance ke teleporter 1 + distance dari teleporter 2 ke target
        distance_via_teleporter1 = self.distance(bot_position, teleporter1) + self.distance(teleporter2, target_position)

        # Distance ke teleporter 2 + distance dari teleporter 1 ke target
        distance_via_teleporter2 = self.distance(bot_position, teleporter2) + self.distance(teleporter1, target_position)

        if distance_via_teleporter1 < distance_via_teleporter2:
            return distance_via_teleporter1, teleporter1
        else:
            return distance_via_teleporter2, teleporter2

    def get_direction(self, bot_position: Position, goal: Position):
        return get_direction(bot_position.x, bot_position.y, goal.x, goal.y)
    
    def get_nearest_blue(self, bot_position: Position, board: Board, list_diamonds: list):
        shortest_distance = float('inf')
        nearest_blue = None
        teleporters = [i for i in board.game_objects if i.type == "TeleportGameObject"]
        lewat_teleporter = False
        teleporter_used = None

        for diamond in list_diamonds:
            distance = self.distance(bot_position, diamond.position)
            teleport_distance = self.teleporter_distance(bot_position, diamond.position, teleporters)
            use_teleporter = teleport_distance[0] < distance

            if diamond.properties.points == 1 and (use_teleporter or distance < shortest_distance):
                shortest_distance = distance
                nearest_blue = diamond
                lewat_teleporter = use_teleporter
                if lewat_teleporter:
                    teleporter_used = teleport_distance[1]

        if lewat_teleporter:
            print("TELEPORTER USED, ", teleporter_used.x, teleporter_used.y) # debug
            print("ambil biru") # debug
            return teleporter_used
        else:
            return nearest_blue

    def highest_density(self, bot_position: Position, board: Board, list_diamonds: list, prefer_low_value=False):
        highest_density = 0
        highest_density_position = None
        teleporters = [i for i in board.game_objects if i.type == "TeleportGameObject"]
        lewat_teleporter = False
        teleporter_used = None

        if prefer_low_value:
            highest_density_position = self.get_nearest_blue(bot_position, board, list_diamonds)
        else:    
            for diamond in list_diamonds:
                distance = self.distance(bot_position, diamond.position)
                teleporters_distance = self.teleporter_distance(bot_position, diamond.position, teleporters)
                use_teleporter = teleporters_distance[0] < distance

                point = diamond.properties.points
                if distance != 0:
                    density = point / distance
                    if density > highest_density or (density == highest_density and point > highest_density_position.properties.points):
                        highest_density = density
                        highest_density_position = diamond
                        lewat_teleporter = use_teleporter
                        if lewat_teleporter:
                            teleporter_used = teleporters_distance[1]

        if lewat_teleporter:
            print("TELEPORTER USED, ", teleporter_used.x, teleporter_used.y) # debug
            print("ambil diamond") # debug
            return teleporter_used
        else:
            return highest_density_position.position

    # def find_nearest_diamond(self, bot_position: Position, list_diamonds: list, prefer_low_value=False):
    #     # Cari diamond terdekat
    #     shortest_distance = float('inf')
    #     nearest_diamond = None

    #     for diamond in list_diamonds:
    #         distance = self.distance(bot_position, diamond.position)
    #         # Jika prefer_low_value True, cari diamond dengan poin 1
    #         if prefer_low_value and diamond.properties.points != 1:
    #             continue
    #         if distance < shortest_distance:
    #             shortest_distance = distance
    #             nearest_diamond = diamond
    #         elif distance == shortest_distance and diamond.properties.points > nearest_diamond.properties.points:
    #             nearest_diamond = diamond

    #     return nearest_diamond
    
    def to_avoid(self, board: Board):
        # fungsi ini digunakan untuk menentukan posisi yang harus dihindari oleh bot
        # misalnya, posisi teleporter, red button, atau bot lain
        teleporters = [i for i in board.game_objects if i.type == "TeleportGameObject"]
        red_buttons = [i for i in board.game_objects if i.type == "RedButtonGameObject"]
        bots = [i for i in board.game_objects if i.type == "BotGameObject"]
        avoid = []
        for teleporter in teleporters:
            avoid.append(teleporter.position)
        for red_button in red_buttons:
            avoid.append(red_button.position)
        for bot in bots:
            avoid.append(bot.position)
        return avoid
    
    def next_position(self, current_position, direction):
        return Position(current_position.x + direction[0], current_position.y + direction[1])

    def is_position_in_list(self, position, list_positions):
        return any(position_equals(position, list_position) for list_position in list_positions)

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        inventory_size = board_bot.properties.inventory_size if board_bot.properties.inventory_size else 0
        bot_position = board_bot.position
        list_diamonds = board.diamonds
        collected = board_bot.properties.diamonds if board_bot.properties.diamonds else 0
        milliseconds_left = board_bot.properties.milliseconds_left if board_bot.properties.milliseconds_left else 0
        seconds_left = milliseconds_left / 1000
        to_avoid = self.to_avoid(board)
        print("to avoid: ", to_avoid) # debug
        teleporters = [i for i in board.game_objects if i.type == "TeleportGameObject"]
        lewat_teleporter = False

        base_position = board_bot.properties.base
        distance_to_base = self.distance(bot_position, base_position)
        teleporter_distance_to_base = self.teleporter_distance(bot_position, base_position, teleporters)
        if teleporter_distance_to_base[0] < distance_to_base:
            distance_to_base = teleporter_distance_to_base[0]
            lewat_teleporter = True

        # Jika waktu tersisa dalam detik sama dengan jarak ke base, kembali ke base
        if seconds_left - 1.8 <= distance_to_base:
            direction_to_base = get_direction(bot_position.x, bot_position.y, base_position.x, base_position.y)
            if lewat_teleporter:
                print("TELEPORTER USED, ", teleporter_distance_to_base[1].x, teleporter_distance_to_base[1].y) # debug
                print("kembali ke base") # debug
                return self.get_direction(bot_position, teleporter_distance_to_base[1])
            else:
                return direction_to_base

        # Jika inventory hampir penuh, ubah strategi untuk mengumpulkan diamond poin 1
        prefer_low_value_diamond = collected == inventory_size - 1

        get_diamond = self.highest_density(bot_position, board, list_diamonds, prefer_low_value_diamond)

        if get_diamond and collected < inventory_size:
            direction_to_diamond = self.get_direction(bot_position, get_diamond)
            next_position_diamond = self.next_position(bot_position, direction_to_diamond)
            # jika 0, 0 atau posisi berikutnya ada dalam daftar to_avoid
            if self.is_position_in_list(next_position_diamond, to_avoid) or direction_to_diamond == (0, 0):
                return 1, 0
            return direction_to_diamond
        else:
            # Kembali ke base jika inventory penuh atau tidak ada diamond terdekat
            if base_position:
                direction_to_base = self.get_direction(bot_position, base_position)
                next_position_base = self.next_position(bot_position, direction_to_base)
                if self.is_position_in_list(next_position_base, to_avoid) or direction_to_base == (0, 0):
                    return 1, 0
                if lewat_teleporter:
                    print("TELEPORTER USED, ", teleporter_distance_to_base[1].x, teleporter_distance_to_base[1].y) # debug
                    return self.get_direction(bot_position, teleporter_distance_to_base[1])
                else:
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

def is_teleporter_position(self, current_position: Position, board: Board):
    teleporters = [i for i in board.game_objects if i.type == "TeleportGameObject"]
    for teleporter in teleporters:
        if position_equals(teleporter.position, current_position):
            return True
    return False

def get_first_teleporter_position(self, board: Board):
    teleporters = [i for i in board.game_objects if i.type == "TeleportGameObject"]
    return teleporters[0].position

def get_second_teleporter_position(self, board: Board):
    teleporters = [i for i in board.game_objects if i.type == "TeleportGameObject"]
    return teleporters[1].position
