from typing import Optional
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class BotOne(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def find_nearest_diamond(self, bot_position: Position,diamonds: list, board: Board, inventory_size: int):
        # Find the nearest diamond
        shortest_distance = float('inf')
        nearest_diamond = None
        collected_diamonds = 0

        for diamond in diamonds:
            if collected_diamonds >= inventory_size:
                break
            distance = abs(diamond.position.x - bot_position.x) + abs(diamond.position.y - bot_position.y)
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_diamond = diamond
                collected_diamonds += 1
        return nearest_diamond

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        if props.diamonds == 5:
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # Just roam around
            self.goal_position = closestdiamond(board_bot, board)

        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        return delta_x, delta_y


