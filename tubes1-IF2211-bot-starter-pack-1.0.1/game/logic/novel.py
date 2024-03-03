from typing import Tuple
from game.logic.base import BaseLogic
from game.models import Board, GameObject

class Novel(BaseLogic):
    def __init__(self):
        # Initialize attributes necessary
        self.my_attribute = 0
    
    def next_move(self, board_bot: GameObject, board: Board):
        # Calculate next move
        # Cuma bisa (1, 0), (0, 1), (-1, 0), (0, -1)
        delta_x = 1
        delta_y = 0
        return delta_x, delta_y