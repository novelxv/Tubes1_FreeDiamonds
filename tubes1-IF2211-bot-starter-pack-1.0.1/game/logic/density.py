from typing import Tuple, Optional
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class Density(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None

    def distance(self, bot_position: Position, goals: Position):
        distance = abs(goals.x - bot_position.x) + abs(goals.y - bot_position.y)
        return distance
    
    def highest_density(self, bot_position: Position, listdiamonds: list):
        highest_density = 0
        highest_density_position = None

        for diamond in listdiamonds:
            distance = self.distance(bot_position, diamond.position)
            point = diamond.properties.points
            density = point / distance
            if density > highest_density:
                highest_density = density
                highest_density_position = diamond
        return highest_density_position

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        inventory_size = board_bot.properties.inventory_size if board_bot.properties.inventory_size else 5 # default 5
        bot_position = board_bot.position
        listdiamonds = board.diamonds
        collected = board_bot.properties.diamonds

        if (collected == inventory_size):
            base = board_bot.properties.base
            self.goal_position = base
        else:
            highest_density_position = self.highest_density(bot_position, listdiamonds)
            self.goal_position = highest_density_position.position
        
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                bot_position.x,
                bot_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        return delta_x, delta_y