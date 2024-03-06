from typing import Tuple
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, position_equals

class Novel2(BaseLogic):
    def __init__(self):
        # Initialize attributes necessary
        pass

    def find_nearest_diamond(self, bot_position: Position, listdiamonds: list):
        # Find the nearest diamond
        shortest_distance = float('inf')
        nearest_diamond = None

        for diamond in listdiamonds:
            distance = abs(diamond.position.x - bot_position.x) + abs(diamond.position.y - bot_position.y)
            if distance < shortest_distance and distance != 0:
                shortest_distance = distance
                nearest_diamond = diamond
        return nearest_diamond

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        inventory_size = board_bot.properties.inventory_size if board_bot.properties.inventory_size else 0
        bot_position = board_bot.position
        listdiamonds = board.diamonds
        collected = board_bot.properties

        nearest_diamond = self.find_nearest_diamond(bot_position, listdiamonds)

        if (nearest_diamond and (collected.diamonds < inventory_size)):
            direction_to_diamond = get_direction(bot_position.x, bot_position.y, nearest_diamond.position.x, nearest_diamond.position.y)
            return direction_to_diamond
        else:
            # Jika tidak ada diamond atau inventory penuh, kembali ke base
            base_position = board_bot.properties.base
            if base_position:
                direction_to_base = get_direction(bot_position.x, bot_position.y, base_position.x, base_position.y)
                return direction_to_base
            else:
                # Default move jika tidak ada instruksi lain
                return 1, 0   