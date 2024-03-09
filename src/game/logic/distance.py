from typing import Tuple
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, position_equals

class Distance(BaseLogic):
    def __init__(self):
        # Initialize attributes necessary
        pass

    def find_nearest_diamond(self, bot_position: Position, list_diamonds: list, prefer_low_value=False):
        # Cari diamond terdekat, dengan opsi untuk memprioritaskan diamond nilai rendah
        shortest_distance = float('inf')
        nearest_diamond = None

        for diamond in list_diamonds:
            distance = abs(diamond.position.x - bot_position.x) + abs(diamond.position.y - bot_position.y)
            # Jika prefer_low_value True, cari diamond dengan poin 1
            if prefer_low_value and diamond.properties.points != 1:
                continue
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_diamond = diamond

        return nearest_diamond

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        inventory_size = board_bot.properties.inventory_size if board_bot.properties.inventory_size else 0
        bot_position = board_bot.position
        list_diamonds = board.diamonds
        collected = board_bot.properties.diamonds if board_bot.properties.diamonds else 0

        # Jika inventory hampir penuh, ubah strategi untuk mengumpulkan diamond poin 1
        prefer_low_value_diamond = collected == inventory_size - 1

        nearest_diamond = self.find_nearest_diamond(bot_position, list_diamonds, prefer_low_value_diamond)

        if nearest_diamond and collected < inventory_size:
            direction_to_diamond = get_direction(bot_position.x, bot_position.y, nearest_diamond.position.x, nearest_diamond.position.y)
            return direction_to_diamond
        else:
            # Kembali ke base jika inventory penuh atau tidak ada diamond terdekat
            base_position = board_bot.properties.base
            if base_position:
                direction_to_base = get_direction(bot_position.x, bot_position.y, base_position.x, base_position.y)
                return direction_to_base
            else:
                # Gerakan default jika tidak ada instruksi lain
                return 1, 0