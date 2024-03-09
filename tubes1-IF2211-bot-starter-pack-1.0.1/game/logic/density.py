from typing import Tuple, Optional
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction
import random

class Density(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

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
    
    def redbutton(self, bot_position:Position, highest_density_position:Position, board: Board):
        redbutton = [i for i in board.game_objects if i.type == "DiamondButtonGameObject"]
        print(redbutton)
        diamond_distance = self.distance(bot_position, highest_density_position.position)
        for button in redbutton:
            button_distance = self.distance(bot_position, button.position)
            if (button_distance < diamond_distance):
                print("go to red button")
                return button
            else:
                print("go to diamond")
                return highest_density_position   

    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        inventory_size = board_bot.properties.inventory_size if board_bot.properties.inventory_size else 5 # default 5
        bot_position = board_bot.position
        listdiamonds = board.diamonds
        collected = board_bot.properties.diamonds
        tackle_check = self.isTackle(board_bot, bot_position, board)
        base = board_bot.properties.base

        if (collected == inventory_size):
            self.goal_position = base
        elif (tackle_check[0] != -99):
            delta_x = tackle_check[0]
            delta_y = tackle_check[1]
        else:
            highest_density_position = self.highest_density(bot_position, listdiamonds)
            if (board_bot.properties.milliseconds_left/1000 < 10 and collected > 1):
                self.goal_position = base
            elif (len(listdiamonds) <= 5):
                self.goal_position = self.redbutton(bot_position, highest_density_position, board).position
            elif (collected == 4 and highest_density_position.properties.points == 2):
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