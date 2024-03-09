from typing import Tuple, Optional
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction
import random

class Density(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None

    def distance(self, bot_position: Position, goals: Position):
        distance = abs(goals.x - bot_position.x) + abs(goals.y - bot_position.y)
        return distance
    
    def teleport_position (self, bot_position: Position, board: Board):
        listPortal = [i for i in board.game_objects if i.type == "TeleportGameObject"]

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
    
    def isTackle(self, board_bot: GameObject, bot_position: Position, board: Board):
        enemy = [i for i in board.bots if (i.position != bot_position)]
        move = [-99, -99]
        for target in enemy:
            if ((target.properties.diamonds > 0) and (board_bot.properties.diamonds < board_bot.properties.inventory_size) and (board_bot.properties.milliseconds_left < target.properties.milliseconds_left)):
                if (bot_position.x == target.position.x) and (abs(bot_position.y - target.position.y) == 1):
                    move = [0, target.position.y - bot_position.y]
                elif (bot_position.y == target.position.y) and (abs(bot_position.x - target.position.x) == 1):
                    move = [target.position.x - bot_position.x, 0]
        return move
    

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        inventory_size = board_bot.properties.inventory_size if board_bot.properties.inventory_size else 5 # default 5
        bot_position = board_bot.position
        listdiamonds = board.diamonds
        collected = board_bot.properties.diamonds
        tackle_check = self.isTackle(board_bot, bot_position, board)

        if (collected == inventory_size):
            base = board_bot.properties.base
            self.goal_position = base
        elif (tackle_check[0] != -99):
            delta_x = tackle_check[0]
            delta_y = tackle_check[1]
        else:
            highest_density_position = self.highest_density(bot_position, listdiamonds)
            if (collected == 4 and highest_density_position.properties.points == 2):
                base = board_bot.properties.base
                self.goal_position = base
            else:
                self.goal_position = highest_density_position.position
        
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                bot_position.x,
                bot_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            delta = self.directions[self.current_direction]
            delta_x = delta[0]
            delta_y = delta[1]
            if random.random() > 0.6:
                self.current_direction = (self.current_direction + 1) % len(
                    self.directions
                )
        if (delta_x == delta_y):
            delta_x = 0
            delta_y = 1

        return delta_x, delta_y