from typing import Tuple
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, position_equals

class Novel(BaseLogic):
    def __init__(self):
        # Initialize attributes necessary
        self.collected_diamonds = 0

    def find_nearest_diamond(self, bot_position: Position, diamonds: list, board: Board):
        # Find the nearest diamond
        shortest_distance = float('inf')
        nearest_diamond = None

        for diamond in diamonds:
            distance = abs(diamond.position.x - bot_position.x) + abs(diamond.position.y - bot_position.y)
            if distance < shortest_distance and distance != 0:
                shortest_distance = distance
                nearest_diamond = diamond
        return nearest_diamond

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        inventory_size = board_bot.properties.inventory_size if board_bot.properties.inventory_size else 0
        bot_position = board_bot.position
        diamonds = board.diamonds

        if self.collected_diamonds < inventory_size:
            nearest_diamond = self.find_nearest_diamond(bot_position, diamonds, board)
            if nearest_diamond:
                direction_to_diamond = get_direction(bot_position.x, bot_position.y, nearest_diamond.position.x, nearest_diamond.position.y)
                self.collected_diamonds += 1
                return direction_to_diamond
        # If no diamonds are found or inventory is full, return to base
        elif self.collected_diamonds == inventory_size:
            base_position = board_bot.properties.base
            if base_position:
                direction_to_base = get_direction(bot_position.x, bot_position.y, base_position.x, base_position.y)
                self.collected_diamonds = 0  # Reset collected diamonds when returning to base
                return direction_to_base
            else:
                # Default move if no other instructions
                return 1, 0