from game.logic.base import BaseLogic
from game.models import Board, GameObject

class Lidya(BaseLogic):
    def _init_(self):
        # Initialize attributes necessary
        self.my_attribute = 0

    def next_move(self, board_bot: GameObject, board: Board):  # Calculate next move
        delta_x = 1
        delta_y = 0
        bot_x, bot_y = board_bot.x, board_bot.y
        diamonds = board.diamonds
        base_x, base_y = board.base.x, board.base.y

        diamond_2 = None
        diamond_1 = None

        for diamond in diamonds:
            diamond_x, diamond_y, poin = diamond.x, diamond.y, diamond.points
            jarak = abs(diamond_x - bot_x) + abs(diamond_y - bot_y)
            if poin == 2:
                if diamond_2 is None or jarak < diamond_2['jarak']:
                    diamond_2 = {'x': diamond_x, 'y': diamond_y, 'jarak': jarak}
            elif poin == 1:
                if diamond_1 is None or jarak < diamond_1['jarak']:
                    diamond_1 = {'x': diamond_x, 'y': diamond_y, 'jarak': jarak}

        if diamond_2:
            target_x, target_y = diamond_2['x'], diamond_2['y']
        elif diamond_1:
            target_x, target_y = diamond_1['x'], diamond_1['y']
        else:
            target_x, target_y = base_x, base_y

        delta_x = 1 if target_x > bot_x else -1 if target_x < bot_x else 0
        delta_y = 1 if target_y > bot_y else -1 if target_y < bot_y else 0

        return delta_x, delta_y