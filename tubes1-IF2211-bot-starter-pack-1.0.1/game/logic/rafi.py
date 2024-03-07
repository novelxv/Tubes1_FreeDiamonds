from typing import Tuple
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction, position_equals

class Rafi(BaseLogic):
    def __init__(self):
        # Initialize attributes necessary
        self.collected_diamonds = 0

    def find_nearest(self, bot_position: Position, targets: list) -> Tuple[Position, float]:
        # Find the nearest target and its distance
        shortest_distance = float('inf')
        nearest_target = None

        for target in targets:
            distance = abs(target.position.x - bot_position.x) + abs(target.position.y - bot_position.y)
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_target = target

        return nearest_target, shortest_distance

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        bot_position = board_bot.position
        diamonds = board.diamonds
        red_buttons = board.red_buttons
        teleports = board.teleports
        base = board_bot.properties.base
        inventory_size = board_bot.properties.inventory_size

        nearest_diamond, diamond_distance = self.find_nearest(bot_position, diamonds)
        nearest_red_button, red_button_distance = self.find_nearest(bot_position, red_buttons)
        nearest_teleport, teleport_distance = self.find_nearest(bot_position, teleports)
        base_distance = abs(base.x - bot_position.x) + abs(base.y - bot_position.y)

        if diamond_distance < 7 and self.collected_diamonds < inventory_size:
            # Move towards the nearest diamond
            self.collected_diamonds += 1
            return get_direction(bot_position.x, bot_position.y, nearest_diamond.position.x, nearest_diamond.position.y)
        elif red_button_distance < diamond_distance and red_button_distance < teleport_distance:
            return get_direction(bot_position.x, bot_position.y, nearest_red_button.position.x, nearest_red_button.position.y)
        elif teleport_distance < diamond_distance:
            return get_direction(bot_position.x, bot_position.y, nearest_teleport.position.x, nearest_teleport.position.y)
        elif self.collected_diamonds >= 3 and base_distance < diamond_distance:
            self.collected_diamonds = 0  # Reset collected diamonds when returning to base
            return get_direction(bot_position.x, bot_position.y, base.x, base.y)
        else:
            return 1, 0  # Default move if no other instructions
