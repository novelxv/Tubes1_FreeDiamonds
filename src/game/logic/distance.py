from typing import Tuple, Optional
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class Distance(BaseLogic):
    def __init__(self):
        # Initialize attributes necessary
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None

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
        inventory_size = board_bot.properties.inventory_size if board_bot.properties.inventory_size else 5 # default 5
        bot_position = board_bot.position
        listdiamonds = board.diamonds
        collected = board_bot.properties.diamonds

        if (collected == inventory_size):
            base = board_bot.properties.base
            self.goal_position = base
        else:
            nearest_diamond = self.find_nearest_diamond(bot_position, listdiamonds)
            self.goal_position = nearest_diamond.position
        
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                bot_position.x,
                bot_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        return delta_x, delta_y


